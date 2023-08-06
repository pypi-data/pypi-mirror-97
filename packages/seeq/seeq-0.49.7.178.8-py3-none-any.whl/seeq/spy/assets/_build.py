from types import ModuleType

import pandas as pd

from .. import _common

from ._model import _AssetBase, DependenciesNotBuilt, BuildContext

from seeq.spy.workbooks import Workbook


def build(model, metadata):
    """
    Utilizes a Python Class-based asset model specification to produce a set
    of item definitions as a metadata DataFrame.

    Parameters
    ----------
    model : {ModuleType, type}
        A Python module, a spy.assets.Asset or a spy.assets.Mixin that
        describes the asset tree to be produced. Follow the spy.assets.ipynb
        Tutorial to understand the structure of your module/classes.

    metadata : {pandas.DataFrame}
        The metadata DataFrame, usually produced from calls to spy.search(),
        that will be used as the "ingredients" for the asset tree and passed
        into all Asset.Attribute() and Asset.Component() decorated class
        functions.
    """

    _common.validate_argument_types([
        (model, 'model', (ModuleType, type)),
        (metadata, 'metadata', pd.DataFrame)
    ])

    return pd.DataFrame(_build(model, metadata))


def _build(model, metadata):
    results = list()

    if isinstance(model, ModuleType):
        if 'Build Path' not in metadata or 'Build Asset' not in metadata or 'Build Template' not in metadata:
            raise ValueError('"Build Path", "Build Asset", "Build Template" are required columns')
        unique_assets = metadata[['Build Path', 'Build Asset', 'Build Template']].drop_duplicates().dropna()
        columns_to_drop = ['Build Path', 'Build Asset', 'Build Template']
    elif issubclass(model, _AssetBase):
        if 'Build Path' not in metadata or 'Build Asset' not in metadata:
            raise ValueError('"Build Path", "Build Asset" are required columns')
        if 'Build Template' in metadata:
            raise ValueError('"Build Template" not allowed when "model" parameter is Asset/Mixin class '
                             'declaration')
        unique_assets = metadata[['Build Path', 'Build Asset']].drop_duplicates().dropna(subset=['Build Asset'])
        columns_to_drop = ['Build Path', 'Build Asset']
    else:
        raise TypeError('"model" parameter must be a Python module (with Assets/Mixins) or an Asset/Mixin class '
                        'declaration')

    context = BuildContext()

    for index, row in unique_assets.iterrows():
        if isinstance(model, ModuleType):
            template = getattr(model, row['Build Template'].replace(' ', '_'))
        else:
            template = model

        instance = template(context, {
            'Name': row['Build Asset'],
            'Asset': row['Build Asset'],
            'Path': row['Build Path']
        })

        if pd.isna(row['Build Path']):
            instance_metadata = metadata[(metadata['Build Asset'] == row['Build Asset']) &
                                         (metadata['Build Path'].isna())]
        else:
            instance_metadata = metadata[(metadata['Build Asset'] == row['Build Asset']) &
                                         (metadata['Build Path'] == row['Build Path'])]

        try:
            results.extend(instance.build(instance_metadata))
        except DependenciesNotBuilt as e:
            raise RuntimeError('The following references/dependencies could not be resolved. Check to see if you have '
                               'circular references in your classes.\n%s' % '\n'.join(e.descriptors))

    results.extend([{
        'Type': 'Workbook',
        'Workbook Type': workbook['Workbook Type'],
        'Name': workbook.name,
        'Object': workbook
    } for workbook in context.workbooks.values() if isinstance(workbook, Workbook)])

    results_df = pd.DataFrame(results)

    return results_df.drop(columns=columns_to_drop, errors='ignore')
