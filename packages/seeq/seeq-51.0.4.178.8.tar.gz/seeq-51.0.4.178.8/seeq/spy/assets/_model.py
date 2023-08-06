import math
import string

from deprecated import deprecated

import pandas as pd

from .. import _common
from .. import _pull
from .. import _push

from seeq.spy.workbooks import Analysis, AnalysisWorksheet, Topic, TopicDocument, DateRange


class DependenciesNotBuilt(Exception):
    def __init__(self, descriptors):
        self.descriptors = descriptors


class WorkbookNotBuilt(Exception):
    def __init__(self, workbook_type, workbook, worksheet=None):
        self.workbook_type = workbook_type
        self.workbook = workbook
        self.worksheet = worksheet


class BuildContext:
    def __init__(self):
        self.workbooks = dict()
        self.cache = dict()
        self.push_df = None
        self.status = None


class PlotRenderInfo:
    def __init__(self, image_format, render_function):
        self.image_format = image_format
        self.render_function = render_function


class _AssetBase:
    DEFAULT_WORKBOOK_NEEDED = '__DEFAULT_WORKBOOK_NEEDED__'

    def __init__(self, context, definition=None, *, parent=None):
        """
        Instantiates an Asset or Mixin.

        :param definition: A dictionary of property-value pairs that make up the definition of the Asset. Typically
        you will want to supply 'Name' at minimum.
        :type definition: dict, pd.DataFrame, pd.Series
        :param parent: An instance of either an Asset or Mixin that represents the parent of this instance. Typically
        this is supplied when @Asset.Component is used to define child assets.
        :type parent: Asset, Mixin
        """
        self.definition = dict()

        if isinstance(definition, _AssetBase):
            self.definition = definition.definition
        elif isinstance(definition, pd.DataFrame):
            if len(definition) != 1:
                raise ValueError('DataFrame must be exactly one row')
            self.definition = definition.iloc[0].to_dict()
        elif isinstance(definition, pd.Series):
            self.definition = definition.to_dict()
        elif definition is not None:
            self.definition = definition

        self.definition['Type'] = 'Asset'
        if 'Name' in self.definition:
            # For an Asset, its name and the Asset column are made identical for clarity
            self.definition['Asset'] = self.definition['Name']

        self.parent = parent  # type: _AssetBase
        self.context = context  # type: BuildContext

        if self.parent is not None:
            # Passing in a parent will relieve the user from having to construct the right path
            if _common.present(self.parent.definition, 'Path'):
                self.definition['Path'] = self.parent.definition['Path'] + ' >> ' + self.parent.definition['Name']
            else:
                self.definition['Path'] = self.parent.definition['Name']

        self.initialize()

    def initialize(self):
        # This is for users to override so they don't have to know about the "crazy" __init__ function and its arguments
        pass

    def __contains__(self, key):
        return _common.present(self.definition, key)

    def __getitem__(self, key):
        return _common.get(self.definition, key)

    def __setitem__(self, key, val):
        self.definition[key] = val

    def __delitem__(self, key):
        del self.definition[key]

    def __repr__(self):
        return '%s >> %s' % (_common.get(self, 'Path'), _common.get(self, 'Name'))

    @property
    @deprecated(reason="Use self.definition instead")
    def asset_definition(self):
        return self.definition

    @property
    @deprecated(reason="Use self.parent.definition instead")
    def parent_definition(self):
        return self.parent.definition if self.parent is not None else None

    def build(self, metadata):
        definitions = list()

        # Filter out deprecated members so that the Deprecated library doesn't produce warnings as we iterate over them
        method_names = [m for m in dir(self) if m not in ['asset_definition', 'parent_definition']]

        # Assemble a list of all functions on this object instance that are callable so that we can iterate over them
        # and find @Asset.Attribute() and @Asset.Component() functions
        object_methods = [getattr(self, method_name) for method_name in method_names
                          if callable(getattr(self, method_name))]

        # The "spy_model" attribute is added to any @Asset.Attribute() and @Asset.Component() decorated
        # functions so that they are processed during build
        remaining_methods = [func for func in object_methods if hasattr(func, 'spy_model')]

        while len(remaining_methods) > 0:
            at_least_one_built = False
            dependencies_not_built = list()
            workbooks_not_built = list()
            for func in remaining_methods.copy():
                func_type = getattr(func, 'spy_model')

                try:
                    attribute = func(metadata)

                except DependenciesNotBuilt as e:
                    dependencies_not_built.extend(e.descriptors)
                    continue

                except WorkbookNotBuilt as e:
                    workbooks_not_built.append(e)
                    continue

                at_least_one_built = True
                remaining_methods.remove(func)

                if attribute is None or func_type not in ['attribute', 'component']:
                    continue

                if isinstance(attribute, list):
                    # This is the @Asset.Component case
                    definitions.extend(attribute)
                else:
                    # This is the @Asset.Attribute case
                    definitions.append(attribute)

            if not at_least_one_built:
                if len(workbooks_not_built) > 0:
                    for not_built in workbooks_not_built:
                        if (not_built.workbook_type, not_built.workbook) not in self.context.workbooks:
                            if not_built.workbook_type == 'analysis':
                                workbook = Analysis({'Name': not_built.workbook})
                            else:
                                workbook = Topic({'Name': not_built.workbook})
                            self.context.workbooks[(not_built.workbook_type, not_built.workbook)] = workbook

                    at_least_one_built = True

            if not at_least_one_built:
                raise DependenciesNotBuilt(dependencies_not_built)

        return definitions

    def build_component(self, template, metadata, component_name):
        instance = template(self.context, {
            'Name': component_name,
        }, parent=self)
        return instance.build(metadata)

    def build_components(self, template, metadata, column_name):
        """
        Builds a set of components by identifying the unique values in the
        column specified by column_name and then instantiating the supplied
        template for each one and building it with the subset of metadata
        for that column value.

        Useful when constructing a rich model whereby a root asset is composed
        of unique components, possibly with further sub-components. For
        example, you may have a Plant asset that contains eight Refigerator
        units that each have two associated Compressor units.

        Parameters
        ----------
        template : {Asset, Mixin}
            A DataFrame or Series containing ID and Type columns that can be
            used to identify the items to pull. This is usually created via a
            call to spy.search().

        metadata : pd.DataFrame
            The metadata DataFrame containing all rows relevant to all
            (sub-)components of this asset. The DataFrame must contain the
            column specified by column_name.

        column_name : str
            The name of the column that will be used to discover the unique
            (sub-)components of this asset. For example, if column_name=
            'Compressor', then there might be values of 'Compressor A12' and
            'Compressor B74' in the 'Compressor' column of the metadata
            DataFrame.

        Returns
        -------
        list(dict)
            A list of definitions for each component.

        Examples
        --------
        Define a Refrigerator template that has Compressor subcomponents.

        >>> class Refrigerator(Asset):
        >>>     @Asset.Attribute()
        >>>     def Temperature(self, metadata):
        >>>         return metadata[metadata['Name'].str.endswith('Temperature')]
        >>>
        >>>     @Asset.Component()
        >>>     def Compressor(self, metadata):
        >>>         return self.build_components(Compressor, metadata, 'Compressor')
        >>>
        >>> class Compressor(Asset):
        >>>
        >>>     @Asset.Attribute()
        >>>     def Power(self, metadata):
        >>>         return metadata[metadata['Name'].str.endswith('Power')]
        """
        component_names = metadata[column_name].dropna().drop_duplicates().tolist()
        component_definitions = ItemGroup()
        for component_name in component_names:
            instance = template(self.context, {
                'Name': component_name,
            }, parent=self)
            component_definition = instance.build(metadata[metadata[column_name] == component_name])
            component_definitions.extend(component_definition)
        return component_definitions

    def pull(self, items, *, start=None, end=None, grid='15min', header='__auto__', group_by=None,
             shape='auto', capsule_properties=None, tz_convert=None, calculation=None, bounding_values=False,
             errors='raise'):

        if isinstance(items, list):
            items = pd.DataFrame(items)

        for index, item in items.iterrows():
            if not _common.present(item, 'ID') or _common.get(item, 'Reference', False):
                pushed_item = _push.get_from_push_df(item, self.context.push_df)
                items.at[index, 'ID'] = pushed_item['ID']

        return _pull.pull(pd.DataFrame(items), start=start, end=end, grid=grid, header=header, group_by=group_by,
                          shape=shape, capsule_properties=capsule_properties, tz_convert=tz_convert,
                          calculation=calculation, bounding_values=bounding_values, errors=errors,
                          status=self.context.status)


class Asset(_AssetBase):
    """
    A class derived from Asset can have @Asset.Attribute and @Asset.Component decorated functions that are executed
    as part of the call to build() which returns a list of definition dicts for the asset.
    """

    def __init__(self, context, definition=None, *, parent=None):
        super().__init__(context, definition, parent=parent)
        self.definition['Asset Object'] = self

        # 'Template' is set on the asset with the hope that, in the future, we will be able to search for items in
        # the asset tree that are derived from a particular template.
        self.definition['Template'] = self.__class__.__name__.replace('_', ' ')

    def build(self, metadata):
        definitions = super().build(metadata)
        definitions.append(self.definition)
        self.definition['Build Result'] = 'Success'
        return definitions

    @staticmethod
    def _add_asset_metadata(asset, attribute_definition, error):
        if _common.present(asset.definition, 'Path') and not _common.present(attribute_definition, 'Path'):
            attribute_definition['Path'] = asset.definition['Path']

        if _common.present(asset.definition, 'Asset') and not _common.present(attribute_definition, 'Asset'):
            attribute_definition['Asset'] = asset.definition['Asset']

        if _common.present(asset.definition, 'Template') and not _common.present(attribute_definition, 'Template'):
            attribute_definition['Template'] = asset.__class__.__name__.replace('_', ' ')

        attribute_definition['Build Result'] = 'Success' if error is None else error

    # noinspection PyPep8Naming
    @classmethod
    def Attribute(cls):
        """
        This decorator appears as @Asset.Attribute on a function with a class that derives from Asset.
        """

        def attribute_decorator(func):
            def attribute_wrapper(self, metadata=None):
                # type: (Asset, pd.DataFrame) -> dict
                if (self, func.__name__) in self.context.cache:
                    return self.context.cache[(self, func.__name__)]

                if metadata is None:
                    raise DependenciesNotBuilt(['"%s" attribute for class "%s" and instance %s' % (
                        func.__name__, self.__class__.__name__, _common.safe_json_dumps(self.definition))])

                func_results = func(self, metadata)

                attribute_definition = dict()

                error = None

                if func_results is None:
                    error = 'None returned by Attribute function'

                def _preserve_originals():
                    for key in ['Name', 'Path', 'Asset', 'Datasource Class', 'Datasource ID', 'Data ID',
                                'Source Number Format', 'Source Maximum Interpolation', 'Source Value Unit Of Measure']:
                        if _common.present(attribute_definition, key):
                            attribute_definition['Referenced ' + key] = attribute_definition[key]
                            del attribute_definition[key]

                if isinstance(func_results, pd.DataFrame):
                    if len(func_results) == 1:
                        attribute_definition.update(func_results.iloc[0].to_dict())
                        _preserve_originals()
                        attribute_definition['Reference'] = True
                    elif len(func_results) > 1:
                        error = 'Multiple attributes returned by "%s":\n%s' % (func.__name__, func_results)
                    else:
                        error = 'No matching metadata row found for "%s"' % func.__name__

                elif isinstance(func_results, dict):
                    attribute_definition.update(func_results)
                    if _common.present(func_results, 'ID'):
                        # If the user is supplying an identifier, they must intend it to be a reference, otherwise
                        # it can't be in the tree.
                        attribute_definition['Reference'] = True

                if not _common.present(attribute_definition, 'Name'):
                    attribute_definition['Name'] = func.__name__.replace('_', ' ')

                attribute_definition['Asset'] = self.definition['Name']
                attribute_definition['Asset Object'] = self

                Asset._add_asset_metadata(self, attribute_definition, error)

                self.context.cache[(self, func.__name__)] = attribute_definition

                return attribute_definition

            # Setting this attribute on the function itself makes it discoverable during build()
            setattr(attribute_wrapper, 'spy_model', 'attribute')

            return attribute_wrapper

        return attribute_decorator

    # noinspection PyPep8Naming
    @classmethod
    def Component(cls):
        """
        This decorator appears as @Asset.Component on a function with a class that derives from Asset.
        """

        def component_decorator(func):
            def component_wrapper(self, metadata=None):
                # type: (Asset, pd.DataFrame) -> ItemGroup
                if (self, func.__name__) in self.context.cache:
                    return self.context.cache[(self, func.__name__)]

                if metadata is None:
                    raise DependenciesNotBuilt(['"%s" component for class "%s" and instance %s' % (
                        func.__name__, self.__class__.__name__, _common.safe_json_dumps(self.definition))])

                func_results = func(self, metadata)

                component_definitions = ItemGroup(list(), self)
                if func_results is None:
                    return component_definitions

                if not isinstance(func_results, list):
                    func_results = [func_results]

                for func_result in func_results:
                    if isinstance(func_result, _AssetBase):
                        _asset_obj = func_result  # type: _AssetBase
                        if not _common.present(_asset_obj.definition, 'Name'):
                            _asset_obj.definition['Name'] = func.__name__.replace('_', ' ')
                        build_results = _asset_obj.build(metadata)
                        component_definitions.extend(build_results)
                    elif isinstance(func_result, dict):
                        component_definition = func_result  # type: dict
                        Asset._add_asset_metadata(self, component_definition, None)
                        component_definitions.append(component_definition)

                self.context.cache[(self, func.__name__)] = component_definitions

                return component_definitions

            # Setting this attribute on the function itself makes it discoverable during build()
            setattr(component_wrapper, 'spy_model', 'component')

            return component_wrapper

        return component_decorator

    # noinspection PyPep8Naming
    @classmethod
    def Display(cls, analysis=None):
        def display_decorator(func):

            # noinspection PyUnusedLocal
            def display_wrapper(self, metadata=None):
                if (self, func.__name__) in self.context.cache:
                    # We've already built this
                    return self.context.cache[(self, func.__name__)]

                if ('analysis', analysis) not in self.context.workbooks:
                    raise WorkbookNotBuilt('analysis', analysis)

                worksheet_object = self.context.workbooks[('analysis', analysis)]  # type: AnalysisWorksheet

                # noinspection PyBroadException
                workstep_object = func(self, metadata, worksheet_object)

                self.context.cache[(self, func.__name__)] = workstep_object

                return workstep_object

            # Setting this attribute on the function itself makes it discoverable during build()
            setattr(display_wrapper, 'spy_model', 'display')

            return display_wrapper

        return display_decorator

    # noinspection PyPep8Naming
    @classmethod
    def DateRange(cls):
        def date_range_decorator(func):
            # noinspection PyUnusedLocal
            def date_range_wrapper(self, metadata=None):
                if (self, func.__name__) in self.context.cache:
                    # We've already built this
                    return self.context.cache[(self, func.__name__)]

                date_range_spec = func(self, metadata)
                date_range_object = DateRange(date_range_spec, None)

                if 'Name' not in date_range_spec:
                    date_range_spec['Name'] = func.__name__.replace('_', ' ')

                self.context.cache[(self, func.__name__)] = date_range_object

                return date_range_object

            # Setting this attribute on the function itself makes it discoverable during build()
            setattr(date_range_wrapper, 'spy_model', 'date_range')

            return date_range_wrapper

        return date_range_decorator

    # noinspection PyPep8Naming
    @classmethod
    def Document(cls, topic=None):
        def document_decorator(func):
            # noinspection PyUnusedLocal
            def document_wrapper(self, metadata=None):
                # type: (_AssetBase, pd.DataFrame) -> TopicDocument

                if (self, func.__name__) in self.context.cache:
                    # We've already built this
                    return self.context.cache[(self, func.__name__)]

                if ('topic', topic) not in self.context.workbooks:
                    raise WorkbookNotBuilt('topic', topic)

                topic_object = self.context.workbooks[('topic', topic)]  # type: Topic

                document_object = func(self, metadata, topic_object)

                self.context.cache[(self, func.__name__)] = document_object

                return document_object

            # Setting this attribute on the function itself makes it discoverable during build()
            setattr(document_wrapper, 'spy_model', 'document')

            return document_wrapper

        return document_decorator

    # noinspection PyPep8Naming
    @classmethod
    def Plot(cls, image_format):
        def plot_decorator(func):
            # noinspection PyUnusedLocal
            def plot_wrapper(self, metadata=None):
                if (self, func.__name__) in self.context.cache:
                    # We've already built this
                    return self.context.cache[(self, func.__name__)]

                def _plot_function(date_range):
                    return func(self, metadata, date_range)

                plot_render_info = PlotRenderInfo(image_format, _plot_function)
                self.context.cache[(self, func.__name__)] = plot_render_info

                return plot_render_info

            # Setting this attribute on the function itself makes it discoverable during build()
            setattr(plot_wrapper, 'spy_model', 'plot')

            return plot_wrapper

        return plot_decorator


class Mixin(_AssetBase):
    """
    A Mixin is nearly identical to an Asset, but it adds attributes/components to an otherwise-defined Asset. The
    definition argument that is passed into the constructor should be the definition of the otherwise-defined Asset.

    This allows asset tree designers to add a set of "special" attributes to a particular instance of an asset
    without "polluting" the main asset definition with attributes that most of the instances shouldn't have.
    """

    def __init__(self, context, definition, parent):
        super().__init__(context, definition, parent=parent.parent)

        # Adopt the "parent" asset's definition since this is a mixin
        self.definition = parent.definition
        self.definition['Asset Object'] = self
        self.definition['Template'] = self.__class__.__name__.replace('_', ' ')

    def build(self, metadata):
        definitions = super().build(metadata)
        return definitions


def do_paths_match_criteria(criteria, names):
    return do_lists_match_criteria(_common.path_string_to_list(criteria), _common.path_string_to_list(names))


def do_lists_match_criteria(criteria, names):
    end = max(len(criteria), len(names))
    for i in range(0, end):
        if i > len(criteria) - 1:
            return False

        criterion = criteria[i]
        if criterion == '**':
            remaining_criteria = criteria[i + 1:]
            for j in range(i, len(names) + 1):
                remaining_names = names[j:]
                if do_lists_match_criteria(remaining_criteria, remaining_names):
                    return True

        if i > len(names) - 1:
            return False

        name = names[i]
        if not _common.does_query_fragment_match(criterion, name, contains=False):
            return False

    return True


class ItemGroup(list):
    def __init__(self, _list=None, relative_to=None):
        super().__init__(list(ItemGroup.flatten(_list) if _list else list()))
        self.relative_to = relative_to

    @staticmethod
    def flatten(l):
        for el in l:
            if isinstance(el, list):
                yield from ItemGroup.flatten(el)
            else:
                yield el

    def pick(self, criteria):
        picked = ItemGroup()

        if not isinstance(criteria, dict):
            raise ValueError('pick(criteria) argument must be a dict')

        for definition in self:
            good = True
            for prop, criterion in criteria.items():
                if prop not in definition:
                    good = False
                    break

                val = definition[prop]

                # If they didn't specify Calculated vs Stored, match on both
                if criterion in ['Signal', 'Condition', 'Scalar']:
                    criterion = f'*{criterion}'

                if prop == 'Path':
                    if not do_paths_match_criteria(criterion, val):
                        good = False
                        break
                elif not _common.does_query_fragment_match(criterion, val, contains=False):
                    good = False
                    break

            if good:
                picked.append(definition)

        return picked

    def assets(self):
        picked = list()
        for definition in self:
            if 'Asset Object' in definition and definition['Asset Object'] not in picked:
                picked.append(definition['Asset Object'])

        return picked

    def as_parameters(self):
        parameters = dict()
        zero_padding = int(math.log10(len(self))) + 1 if len(self) > 0 else 1
        for i in range(len(self)):
            definition = self[i]
            string_spec = '$p{0:0%dd}' % zero_padding
            parameters[string_spec.format(i)] = definition

        return parameters

    def roll_up(self, statistic):
        parameters = self.as_parameters()

        if len(parameters) > 0:
            types = {p['Type'] for p in parameters.values()}
            if len(types) == 0:
                return None

            if len(types) > 1:
                debug_string = '\n'.join(
                    [_common.safe_json_dumps(p) for p in parameters.values()])
                raise RuntimeError('Cannot compute statistics across different types of items:\n%s' % debug_string)

            _type = types.pop().replace('Stored', '').replace('Calculated', '')
            fns = {fn.statistic: fn for fn in _common.ROLL_UP_FUNCTIONS if fn.input_type == _type}

            if statistic.lower() not in fns:
                raise ValueError('Statistic "%s" not recognized for type %s. Valid statistics:\n%s' %
                                 (statistic, _type, '\n'.join([string.capwords(s) for s in fns.keys()])))
        else:
            fns = {fn.statistic: fn for fn in _common.ROLL_UP_FUNCTIONS}
            if statistic.lower() not in fns:
                raise ValueError('Statistic "%s" not recognized. Valid statistics:\n%s' %
                                 (statistic, '\n'.join([string.capwords(s) for s in fns.keys()])))

        fn = fns[statistic.lower()]  # type: _common.RollUpFunction

        param_list = list(parameters.keys())
        if len(parameters) > 1:
            if fn.style == 'union':
                formula = ' or '.join(param_list)
            elif fn.style == 'intersect':
                formula = ' and '.join(param_list)
            elif fn.style == 'fluent':
                formula = param_list[0]
                for p in param_list[1:]:
                    formula += f'.{fn.function}({p})'
            else:
                formula = f'{fn.function}({", ".join(param_list)})'
        elif len(parameters) == 1:
            parameter = param_list[0]
            if fn.function.startswith('count'):
                formula = f'{fn.function}({parameter})'
            elif fn.function == 'range':
                formula = '0.toSignal()'
            else:
                formula = parameter
        else:
            if fn.output_type == 'Signal':
                formula = 'SCALAR.INVALID.toSignal()'
            elif fn.output_type == 'Condition':
                formula = "condition(40d, capsule('1970-01-01T00:00:00Z', '1970-01-01T00:00:00Z'))"
            else:
                formula = 'SCALAR.INVALID'

        return {
            'Type': fn.output_type,
            'Formula': formula,
            'Formula Parameters': parameters
        }
