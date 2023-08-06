import copy
import re

from seeq.sdk import *
from seeq.spy import _login, _common
from ._item import Item


class Content(Item):
    """
    The SPy representation of a Seeq Content Item. Content can be created with a number of different sizing
    parameters defined in the display() function within an HTML template.

    If no size, shape, width, or height are specified in the display() function, size and shape will default to medium
    and rectangle, respectively. If a height and width are specified, they will take precedence over size and shape.
    A height must be specified with a width and vice-versa.

    ===================== ==================================================
    Input Column          Content Size Attribute
    ===================== ==================================================
    Size                  The size of the content. Can be 'small', 'medium',
                          or 'large'. Defaults to 'medium'
    Shape                 The content's shape. Can be 'strip', 'rectangle',
                          or 'square'. Defaults to 'rectangle'
    Height                The height of the content. Takes precedence over
                          the size/shape parameter, if specified
    Width                 The width of the content. Takes precedence over
                          the size/shape parameter, if specified
    Scale                 The content's desired scale. A value greater than
                          1 will increase the size of elements within the
                          screenshot. A value less than 1 will shrink the
                          size of elements within the screenshot

    """
    CONTENT_SHAPE = {'strip': {'width': 16, 'height': 4},
                     'rectangle': {'width': 16, 'height': 9},
                     'square': {'width': 15, 'height': 15}}

    CONTENT_SIZE = {'small': 350, 'medium': 700, 'large': 1050}

    def __init__(self, definition, report=None):
        super().__init__(definition)
        self.report = report

    @property
    def name(self):
        # Since we don't have a way of uniquely identifying a piece of Content that results from a display()
        # declaration in an HTML report template, we instead hash some state for Content items and use that
        # as the name. Then we can use that name to match up content from an HTML template with an in-memory
        # object.
        return self.definition_hash

    @property
    def definition_hash(self):
        definition_copy = copy.deepcopy(self.definition)
        for key in ['ID', 'Name']:
            if key in definition_copy:
                del definition_copy[key]
        return Item.digest_hash(definition_copy)

    def push(self, item_map: dict, existing_contents: dict):
        content_input = self._create_content_input(item_map)

        content_to_push = self.apply_map(item_map)
        existing_content = existing_contents.get(content_to_push.id)

        if not existing_content:
            existing_content = existing_contents.get(content_to_push.name)

        content_api = ContentApi(_login.client)
        if not existing_content:
            content_output = content_api.create_content(body=content_input)  # type: ContentOutputV1
        else:
            content_output = content_api.update_content(
                id=existing_content.id, body=content_input)  # type: ContentOutputV1

        item_map[self.id.upper()] = content_output.id.upper()

        return content_output

    def _create_content_input(self, item_map=None):
        self._validate_fields_before_push()

        date_range_id = None
        if _common.present(self.definition, 'Date Range ID'):
            if self.definition['Date Range ID'].upper() not in item_map:
                raise _common.DependencyNotFound(
                    f'Date Range {self.definition["Date Range ID"].upper()} for {self} not found')

            date_range_id = item_map[self.definition['Date Range ID'].upper()]

        if self.definition['Worksheet ID'] not in item_map:
            raise _common.DependencyNotFound(f'Worksheet {self.definition["Worksheet ID"]} not found')

        if self.definition['Workstep ID'] not in item_map:
            raise _common.DependencyNotFound(f'Workstep {self.definition["Workstep ID"]} not found')

        # Report has definitely already been pushed by this time
        report_id = item_map[self.report.id.upper()]

        scale = self.definition['Scale'] if 'Scale' in self.definition else None

        return ContentInputV1(name=self.definition['Name'],
                              width=self.definition['Width'],
                              height=self.definition['Height'],
                              worksheet_id=item_map[self.definition['Worksheet ID']],
                              workstep_id=item_map[self.definition['Workstep ID']],
                              date_range_id=date_range_id,
                              report_id=report_id,
                              scale=scale,
                              archived=_common.get(self.definition, 'Archived', False))

    def _validate_fields_before_push(self):
        if 'Name' not in self.definition:
            raise RuntimeError('Unable to push Content: missing "Name" field')
        if 'Width' not in self.definition:
            raise RuntimeError('Unable to push Content: missing "Width" field')
        if 'Height' not in self.definition:
            raise RuntimeError('Unable to push Content: missing "Height" field')
        if 'Worksheet ID' not in self.definition:
            raise RuntimeError('Unable to push Content: missing "Worksheet ID" field')
        if 'Workstep ID' not in self.definition:
            raise RuntimeError('Unable to push Content: missing "Workstep ID" field')

    @staticmethod
    def pull(item_id, *, allowed_types=None, report=None):
        content_api = ContentApi(_login.client)
        content_output = content_api.get_content(id=item_id)  # type: ContentOutputV1

        new_content_definition = {'Name': content_output.name,
                                  'ID': content_output.id,
                                  'Width': content_output.width,
                                  'Height': content_output.height,
                                  'Worksheet ID': content_output.source_worksheet,
                                  'Workstep ID': content_output.source_workstep,
                                  'Workbook ID': content_output.source_workbook,
                                  'Scale': content_output.scale}

        if content_output.date_range is not None:
            new_content_definition['Date Range ID'] = content_output.date_range.id

        return Content(new_content_definition, report)

    def construct_data_id(self, label):
        return self._construct_data_id(label)

    @property
    def date_range(self):
        if 'Date Range ID' not in self.definition:
            return None

        return self.report.date_ranges[self.definition['Date Range ID']]

    @date_range.setter
    def date_range(self, value):
        if value is None:
            self.definition['Date Range ID'] = None
        else:
            self.definition['Date Range ID'] = value['ID']


class DateRange(Item):
    """
    The SPy representation of a Seeq date range. Date ranges can be created with a number of different input
    properties that a user can define when creating a Date Range asset. Date ranges can either be static,
    specified with just a Name, Start, and End, or they can be live, denoted by including Auto Enabled,
    Auto Duration, Auto offset, and Auto Offset Direction values.

    ===================== =============================================
    Input Column          Date Range Attribute
    ===================== =============================================
    ID                    The id of the date range. If not provided one
                          will be generated
    Name                  The name of the date range. Eg "Date Range 1"
    Start                 The ISO 8601 string or datetime object start
                          of the date range
    End                   The ISO 8601 string or datetime object end of
                          the date range
    Auto Enabled          Boolean if automatic update is enabled
    Auto Duration         The duration of the automatic update sliding
                          window. Eg, 10min, 1hr, 1d, etc
    Auto Offset           The offset of the automatic update sliding
                          window. Eg, 10min, 1day, etc
    Auto Offset Direction The direction of the offset. Either 'Past' or
                          'Future'. Default 'Past'
    """

    DATE_RANGE_COLUMN_NAMES = ['ID', 'Name', 'Start', 'End', 'Auto Enabled', 'Auto Duration', 'Auto Offset',
                               'Auto Offset Direction', 'Condition ID', 'Type']

    def __init__(self, definition, report):
        super().__init__(definition)
        self.report = report

    def push(self, item_map: dict, existing_date_ranges: dict):
        date_range_input = self._create_date_range_input(item_map)

        existing_date_range = existing_date_ranges.get(self.id)
        if not existing_date_range:
            existing_date_range = existing_date_ranges.get(self.name)

        content_api = ContentApi(_login.client)
        if not existing_date_range:
            date_range_output = content_api.create_date_range(body=date_range_input)  # type: DateRangeOutputV1
        else:
            date_range_output = content_api.update_date_range(
                id=existing_date_range.id, body=date_range_input)  # type: DateRangeOutputV1

        item_map[self.id.upper()] = date_range_output.id.upper()

        return date_range_output

    STATIC_DATE_RANGE_REGEX = r'capsule\(\d+.*\d+.*\)'
    AUTO_DATE_RANGE_REGEX = r'capsule\(\$now\s*(?P<dir>[\-+])\s*(?P<offset>[\d\w\.]+)\s*-\s*(?P<dur>[\d\.]+)ms,.*\)'

    @staticmethod
    def pull(item_id, *, allowed_types=None, report=None):
        if isinstance(item_id, DateRangeOutputV1):
            # This is an optimization because get_contents_with_all_metadata returns both the content and date range
            date_range_output = item_id
        else:
            content_api = ContentApi(_login.client)
            date_range_output = content_api.get_date_range(id=item_id)

        date_range_dict = dict()
        date_range_dict['Name'] = date_range_output.name
        date_range_dict['ID'] = date_range_output.id
        date_range_dict['Enabled'] = date_range_output.enabled
        date_range_dict['Archived'] = date_range_output.archived

        is_static_date_range = False

        if re.search(DateRange.STATIC_DATE_RANGE_REGEX, date_range_output.formula):
            is_static_date_range = True

        if is_static_date_range:
            date_range_dict['Start'] = \
                _login.parse_datetime_with_timezone(date_range_output.date_range.start).isoformat()
            date_range_dict['End'] = \
                _login.parse_datetime_with_timezone(date_range_output.date_range.end).isoformat()
        else:
            match = re.search(DateRange.AUTO_DATE_RANGE_REGEX, date_range_output.formula)
            if not match:
                raise RuntimeError(f'DateRange formula not recognized: {date_range_output.formula}')
            date_range_dict['Auto Enabled'] = True
            date_range_dict['Auto Offset Direction'] = 'Past' if match.group('dir') else 'Future'
            date_range_dict['Auto Offset'] = match.group('offset')
            date_range_dict['Auto Duration'] = str(int(match.group('dur')) / 1000) + 's'

        return DateRange(date_range_dict, report)

    def _create_date_range_input(self, item_map):
        self._validate_fields_before_push()

        # We put a dummy cron schedule here so that we can create a live date range prior to creating a report with a
        # schedule
        cron_schedule = ['59 59 23 31 12 ? 2099'] if self._is_date_range_live() else None

        return DateRangeInputV1(name=self.definition['Name'],
                                formula=self.formula,
                                cron_schedule=cron_schedule,
                                report_id=item_map[self.report.id],
                                enabled=_common.get(self.definition, 'Enabled', True),
                                archived=_common.get(self.definition, 'Archived', False))

    def _validate_fields_before_push(self):
        if 'Name' not in self.definition:
            raise RuntimeError('Unable to push Date Range: missing "name"')

    def _is_date_range_live(self):
        return '$now' in self.formula

    @staticmethod
    def _validate_user_date_range(date_range):
        errors = list()

        for k in date_range.keys():
            if k not in DateRange.DATE_RANGE_COLUMN_NAMES:
                errors.append(
                    f'Unrecognized Date Range property "{k}". Valid properties:\n'
                    f'{DateRange.DATE_RANGE_COLUMN_NAMES}')

        if 'Name' not in date_range:
            errors.append('All date ranges require a "Name"')

        if 'Start' in date_range and 'End' not in date_range:
            errors.append('Date Range "End" must be supplied with Date Range "Start"')
        elif 'End' in date_range and 'Start' not in date_range:
            errors.append('Date Range "Start" must be supplied with Date Range "End"')

        # if auto enabled is defined, all the other auto fields must be defined.
        if 'Auto Enabled' in date_range:
            if 'Auto Offset' not in date_range:
                errors.append('"Auto Offset" is required if "Auto Enabled" is True')
            if 'Auto Duration' not in date_range:
                errors.append('"Auto Duration" is required if "Auto Enabled" is True')
            if 'Auto Offset Direction' not in date_range:
                errors.append('"Auto Offset Direction" is required if "Auto Enabled" is True')

        if errors:
            msg = f'There was 1 error ' if len(errors) == 1 else f'There were {len(errors)} errors '
            msg += f'detected in date range "{date_range["Name"]}": {errors}'
            raise RuntimeError(msg)

    def construct_data_id(self, label):
        return self._construct_data_id(label)

    @property
    def start(self):
        return _login.parse_datetime_with_timezone(_common.get(self.definition, 'Start'))

    @property
    def end(self):
        return _login.parse_datetime_with_timezone(_common.get(self.definition, 'End'))

    @property
    def formula(self):
        if 'Start' in self and 'End' in self:
            start = self.start
            end = self.end

            return f'capsule({int(start.value / 1_000_000)}ms,{int(end.value / 1_000_000)}ms)'
        else:
            offset_direction = '-' if self['Auto Offset Direction'] == 'past' else '+'
            offset_value = _common.parse_str_time_to_ms(self['Auto Offset'])[0]
            offset_units = _common.parse_str_time_to_ms(self['Auto Offset'])[1]
            offset_duration = int(_common.parse_str_time_to_ms(self['Auto Duration'])[2])

            return f'capsule($now {offset_direction} {offset_value}{offset_units} - {offset_duration}ms, ' \
                   f'$now {offset_direction} {offset_value}{offset_units})'
