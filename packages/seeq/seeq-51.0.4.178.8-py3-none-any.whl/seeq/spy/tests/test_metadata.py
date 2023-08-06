import pytest

from . import test_common

from .. import _common
from .. import _metadata

from seeq.sdk import *


def setup_module():
    test_common.login()


def assert_datasource_properties(datasource_output, name, datasource_class, datasource_id):
    assert datasource_output.datasource_class == datasource_class
    assert datasource_output.datasource_id == datasource_id
    assert datasource_output.name == name
    assert not datasource_output.is_archived
    assert datasource_output.stored_in_seeq
    assert not datasource_output.cache_enabled
    assert datasource_output.description == _common.DEFAULT_DATASOURCE_DESCRIPTION
    assert len(datasource_output.additional_properties) == 1
    filtered_properties = filter(lambda x: x.name == 'Expect Duplicates During Indexing', datasource_output.additional_properties)
    additional_property = list(filtered_properties)[0]
    assert additional_property.value


@pytest.mark.system
def test_create_datasource():
    datasources_api = DatasourcesApi(test_common.get_client())

    with pytest.raises(ValueError):
        _metadata.create_datasource(1)

    _metadata.create_datasource('test_datasource_name_1')

    datasource_output_list = datasources_api.get_datasources()  # type: DatasourceOutputListV1
    datasource_output = list(filter(lambda d: d.name == 'test_datasource_name_1',
                                    datasource_output_list.datasources))[0]  # type: DatasourceOutputV1

    assert_datasource_properties(datasource_output,
                                 'test_datasource_name_1',
                                 _common.DEFAULT_DATASOURCE_CLASS,
                                 'test_datasource_name_1')

    with pytest.raises(ValueError, match='"Datasource Name" required for datasource'):
        _metadata.create_datasource({
            'Blah': 'test_datasource_name_2'
        })

    datasource_output = _metadata.create_datasource({
        'Datasource Name': 'test_datasource_name_2'
    })
    assert_datasource_properties(datasource_output,
                                 'test_datasource_name_2',
                                 _common.DEFAULT_DATASOURCE_CLASS,
                                 'test_datasource_name_2')

    datasource_output = _metadata.create_datasource({
        'Datasource Name': 'test_datasource_name_3',
        'Datasource ID': 'test_datasource_id_3'
    })
    assert_datasource_properties(datasource_output,
                                 'test_datasource_name_3',
                                 _common.DEFAULT_DATASOURCE_CLASS,
                                 'test_datasource_id_3')

    with pytest.raises(ValueError):
        datasource_output = _metadata.create_datasource({
            'Datasource Class': 'test_datasource_class_4',
            'Datasource Name': 'test_datasource_name_4',
            'Datasource ID': 'test_datasource_id_4'
        })
