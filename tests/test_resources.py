import os
import pytest

from hypatia.resources import ResourcePack
from hypatia.resources.filesystem import FilesystemResourcePack
from hypatia.resources.exceptions import *


class PopulatedResourcePack(ResourcePack):
    def __init__(self):
        super().__init__()

        self.content = {
            "type": "dir",
            "content": {
                "testfile": {
                    "type": "file",
                    "content": b"Hello world!"
                },
                "testdir": {
                    "type": "dir",
                    "content": {
                        "subfile": {
                            "type": "file",
                            "content": b"Hello again!"
                        }
                    }
                }
            }
        }

class TestResourcePack:
    def test_path_normalization(self):
        teststr = "/..//1/2/../2//3/4/./5//"
        result = "/1/2/3/4/5"

        assert ResourcePack.normalize(teststr) == result

    def test_parse_tree_for_entry_root_file(self):
        f = PopulatedResourcePack()
        out = f._parse_tree_for_entry("/testfile")
        assert out["type"] == "file"
        assert out["content"] == b"Hello world!"

    def test_parse_tree_for_entry_nested_file(self):
        f = PopulatedResourcePack()
        out = f._parse_tree_for_entry("/testdir/subfile")
        assert out["type"] == "file"
        assert out["content"] == b"Hello again!"

    def test_parse_tree_for_entry_nonexistant_file(self):
        f = PopulatedResourcePack()
        with pytest.raises(FileNotFound): 
            f._parse_tree_for_entry("/404_file_not_found")

    def test_parse_tree_for_entry_fail_on_using_file_as_directory(self):
        f = PopulatedResourcePack()
        with pytest.raises(NotADirectory):
            f._parse_tree_for_entry("/testfile/blah")

    def test_mkdir_creates_new_directory_in_root(self):
        f = PopulatedResourcePack()
        f.mkdir('/testdirtwo')

        entry = f._parse_tree_for_entry('/testdirtwo')
        assert entry['type'] == 'dir'

    def test_mkdir_creates_new_directory_in_subdir(self):
        f = PopulatedResourcePack()
        f.mkdir('/testdir/testdirtwo')

        entry = f._parse_tree_for_entry('/testdir/testdirtwo')
        assert entry['type'] == 'dir'

    def test_open_existing_file(self):
        f = PopulatedResourcePack()
        handle = f.open("/testfile")

        assert handle._respack == f
        assert handle._path_in_respack == '/testfile'

    def test_open_nonexisting_file(self):
        f = PopulatedResourcePack()

        with pytest.raises(FileNotFound):
            handle = f.open("/404_file_not_found")

    def test_open_directory(self):
        f = PopulatedResourcePack()

        with pytest.raises(NotAFile):
            handle = f.open("/testdir")

    def test_write_to_file(self):
        f = PopulatedResourcePack()
        handle = f.open("/testfile")

        handle.write(b'test!')
        handle.flush()

        entry = f._parse_tree_for_entry('/testfile')
        assert entry['content'] == b'test! world!'

class TestFilesystemResourcePack:
    def test_load_from_fs(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        f = FilesystemResourcePack(dir_path)

        assert f.content['content']['maps']['type'] == 'dir'
        assert f.content['content']['maps']['content']['testmap.json']['type'] == 'file'
