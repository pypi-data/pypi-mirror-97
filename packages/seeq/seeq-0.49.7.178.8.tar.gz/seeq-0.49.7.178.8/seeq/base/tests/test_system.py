import os
import tempfile

from pathlib import Path

import configuration.helpers as conf
import pytest

from seeq.base.system import human_readable_byte_count
from seeq.base import system


@pytest.mark.unit
def test_human_readable_byte_count_base_ten():
    '''
    Make sure we get the same results as SystemInfoTest#testHumanReadableByteCountBaseTen
    '''
    assert human_readable_byte_count(0, False, False) == '0 B'
    assert human_readable_byte_count(10, False, False) == '10 B'
    assert human_readable_byte_count(900, False, False) == '900 B'
    assert human_readable_byte_count(999, False, False) == '999 B'

    assert human_readable_byte_count(1000, False, False) == '1.00 KB'
    assert human_readable_byte_count(2000, False, False) == '2.00 KB'
    assert human_readable_byte_count(1000 * 1000 - 10, False, False) == '999.99 KB'

    assert human_readable_byte_count(1000 * 1000, False, False) == '1.00 MB'
    assert human_readable_byte_count(50 * 1000 * 1000, False, False) == '50.00 MB'
    assert human_readable_byte_count(1000 * 1000 * 1000 - 10000, False, False) == '999.99 MB'

    assert human_readable_byte_count(1000 * 1000 * 1000, False, False) == '1.00 GB'
    assert human_readable_byte_count(50 * 1000 * 1000 * 1000, False, False) == '50.00 GB'
    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 - 10000000, False, False) == '999.99 GB'

    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000, False, False) == '1.00 TB'
    assert human_readable_byte_count(50 * 1000 * 1000 * 1000 * 1000, False, False) == '50.00 TB'
    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 * 1000 - 1e10, False, False) == '999.99 TB'

    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 * 1000, False, False) == '1.00 PB'
    assert human_readable_byte_count(50 * 1000 * 1000 * 1000 * 1000 * 1000, False, False) == '50.00 PB'
    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 * 1000 * 1000 - 1e13, False, False) == '999.99 PB'

    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 * 1000 * 1000, False, False) == '1.00 EB'
    assert human_readable_byte_count(50 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000, False, False) == '50.00 EB'
    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 - 1e16, False, False) == '999.99 EB'


@pytest.mark.unit
def test_calculate_default_optimal_heap_sizes():
    # 64-bit, 8 cpu cores for screenshot purposes
    test_64_bit_values_8_cores = [
        # physical, appserver, cassandra, jmvLink, postgres, netLink, renderer, reverse proxy, supervisor, os
        [4000, 1200, 500, 250, 500, 250, 500, 250, 300, 250],
        [8000, 2700, 1000, 500, 1000, 500, 1000, 500, 300, 500],
        [12000, 4200, 1500, 750, 1500, 750, 1500, 750, 300, 750],
        [16000, 5700, 2000, 1000, 2000, 1000, 2000, 1000, 300, 1000],
        [32000, 11700, 4000, 2000, 4000, 2000, 4000, 2000, 300, 2000],
        [64000, 27700, 8000, 4000, 8000, 4000, 4000, 4000, 300, 4000],
        [128000, 67700, 8000, 8000, 16000, 8000, 4000, 8000, 300, 8000],
        [256000, 147700, 8000, 16000, 32000, 16000, 4000, 16000, 300, 16000]
    ]

    conf.set_option('Cpu/Count', 8, '')

    for test_set in test_64_bit_values_8_cores:
        conf.set_option('Memory/System/Total', test_set[0], '')

        assert conf.get_option('Memory/Appserver/Size') == test_set[1]
        assert conf.get_option('Memory/Cassandra/Size') == test_set[2]
        assert conf.get_option('Memory/JvmLink/Size') == test_set[3]
        assert conf.get_option('Memory/Postgres/Size') == test_set[4]
        assert conf.get_option('Memory/NetLink/Size') == test_set[5]
        assert conf.get_option('Memory/Renderer/Size') == test_set[6]
        assert conf.get_option('Memory/ReverseProxy/Size') == test_set[7]
        assert conf.get_option('Memory/Supervisor/Size') == test_set[8]
        assert conf.get_option('Memory/OperatingSystem/Size') == test_set[9]
        # Uncomment the following when needing to update the test
        # print(test_set[0], end=",")
        # print(conf.get_option('Memory/Appserver/Size'), end=",")
        # print(conf.get_option('Memory/Cassandra/Size'), end=",")
        # print(conf.get_option('Memory/JvmLink/Size'), end=",")
        # print(conf.get_option('Memory/Postgres/Size'), end=",")
        # print(conf.get_option('Memory/NetLink/Size'), end=",")
        # print(conf.get_option('Memory/Renderer/Size'), end=",")
        # print(conf.get_option('Memory/ReverseProxy/Size'), end=",")
        # print(conf.get_option('Memory/Supervisor/Size'), end=",")
        # print(conf.get_option('Memory/OperatingSystem/Size'), end=",")
        # print("")

    # 64-bit, 64 cpu cores for screenshot purposes
    test_64_bit_values_64_cores = [
        # physical, appserver, cassandra, jmvLink, postgres, netLink, renderer, reverse proxy, supervisor, os
        [4000, 1200, 500, 250, 500, 250, 500, 250, 300, 250],
        [8000, 2700, 1000, 500, 1000, 500, 1000, 500, 300, 500],
        [12000, 4200, 1500, 750, 1500, 750, 1500, 750, 300, 750],
        [16000, 5700, 2000, 1000, 2000, 1000, 2000, 1000, 300, 1000],
        [32000, 11700, 4000, 2000, 4000, 2000, 4000, 2000, 300, 2000],
        [64000, 23700, 8000, 4000, 8000, 4000, 8000, 4000, 300, 4000],
        [128000, 55700, 8000, 8000, 16000, 8000, 16000, 8000, 300, 8000],
        [256000, 119700, 8000, 16000, 32000, 16000, 32000, 16000, 300, 16000],
        [512000, 279700, 8000, 32000, 64000, 32000, 32000, 32000, 300, 32000],
    ]
    conf.set_option('Cpu/Count', 64, '')
    for test_set in test_64_bit_values_64_cores:
        conf.set_option('Memory/System/Total', test_set[0], '')

        assert conf.get_option('Memory/Appserver/Size') == test_set[1]
        assert conf.get_option('Memory/Cassandra/Size') == test_set[2]
        assert conf.get_option('Memory/JvmLink/Size') == test_set[3]
        assert conf.get_option('Memory/Postgres/Size') == test_set[4]
        assert conf.get_option('Memory/NetLink/Size') == test_set[5]
        assert conf.get_option('Memory/Renderer/Size') == test_set[6]
        assert conf.get_option('Memory/ReverseProxy/Size') == test_set[7]
        assert conf.get_option('Memory/Supervisor/Size') == test_set[8]
        assert conf.get_option('Memory/OperatingSystem/Size') == test_set[9]
        # Uncomment the following when needing to update the test
        # print(test_set[0], end=",")
        # print(conf.get_option('Memory/Appserver/Size'), end=",")
        # print(conf.get_option('Memory/Cassandra/Size'), end=",")
        # print(conf.get_option('Memory/JvmLink/Size'), end=",")
        # print(conf.get_option('Memory/Postgres/Size'), end=",")
        # print(conf.get_option('Memory/NetLink/Size'), end=",")
        # print(conf.get_option('Memory/Renderer/Size'), end=",")
        # print(conf.get_option('Memory/ReverseProxy/Size'), end=",")
        # print(conf.get_option('Memory/Supervisor/Size'), end=",")
        # print(conf.get_option('Memory/OperatingSystem/Size'), end=",")
        # print("")

    conf.unset_option('Cpu/Count')
    conf.unset_option('Memory/System/Total')
    # Uncomment the following when needing to update the test
    # assert False


@pytest.mark.unit
def test_copy_tree_exclude_folder_relative_path():
    # It was discovered in CRAB-20621 that robocopy's /XD flag to exclude directories wasn't working for relative
    # paths to subdirectories. This tests system#copy_tree to be compatible with non-Windows systems.
    # See https://superuser.com/a/690842 and follow-up comments
    with tempfile.TemporaryDirectory() as src:
        tree = TestDirectoryTree(src)
        with tempfile.TemporaryDirectory() as dest:
            system.copytree(src, dest, exclude=tree.exclude)

            all_root_contents = os.listdir(dest)
            # Destination should only have KeepParent and KeepMe.txt
            assert len(all_root_contents) == 2
            assert str(tree.keep_parent_dir_relative) in all_root_contents
            assert tree.root_keep_file_name in all_root_contents

            # Destination should have only KeepParent/KeepMe subdir
            all_subdirs = os.listdir(dest / tree.keep_parent_dir_relative)
            assert len(all_subdirs) == 1
            assert tree.keep_subdir_name in all_subdirs


class TestDirectoryTree():
    def __init__(self, root):
        self.root = root
        self.keep_parent_dir_relative = Path('KeepParent')
        self.keep_subdir_name = 'KeepMe'
        self.exclude_subdir_name = 'ExcludeMe'
        self.exclude_parent_dir_relative = Path('ExcludeParent')

        self.root_keep_file_name = 'KeepMe.txt'
        self.root_exclude_file_name = 'ExcludeMe.txt'

        self.keep_subdir_relative = self.keep_parent_dir_relative / self.keep_subdir_name
        self.exclude_subdir_relative = self.keep_parent_dir_relative / self.exclude_subdir_name

        self.exclude = [str(self.exclude_parent_dir_relative), str(self.exclude_subdir_relative),
                        self.root_exclude_file_name]

        self._create_tree()

    def _create_tree(self):
        # tmpDir
        # |
        # ---- KeepMe.txt
        # -----ExcludeMe.txt
        # ---- ExcludeParent
        # ---- KeepParent
        #          |
        #          ----- KeepMe
        #          |
        #          ----- ExcludeMe
        os.makedirs(self.root / self.keep_subdir_relative)
        os.makedirs(self.root / self.exclude_parent_dir_relative)
        os.makedirs(self.root / self.exclude_subdir_relative)

        open(Path(self.root) / self.root_keep_file_name, 'a').close()
        open(Path(self.root) / self.root_exclude_file_name, 'a').close()