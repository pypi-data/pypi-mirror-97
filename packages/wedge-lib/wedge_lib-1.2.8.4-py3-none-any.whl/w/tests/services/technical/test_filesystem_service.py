import os
from pathlib import Path
import pytest

from w.services.technical.filesystem_service import FilesystemService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestFilesystemService(TestCaseMixin):
    """Test unit suite for FilesystemService"""

    def setup_method(self):
        FilesystemService.clear()
        self.clean_sandbox()

    """
    check_dir_exits
    """

    def test_check_dir_exists_with_unknown_dir_raise_runtime_error(self):
        """ Ensure check dir raise RuntimeError if dir does not exists """
        with pytest.raises(RuntimeError, match="unknown-dir does not exists"):
            FilesystemService.check_dir_exists("unknown-dir")

    def test_check_dir_exists_with_success_return_none(self):
        """ Ensure check dir succeed """
        assert not FilesystemService.check_dir_exists(
            self.get_datasets_dir("filesystem")
        )

    """
    check_file_exits
    """

    def test_check_file_exists_with_unknown_file_raise_runtime_error(self):
        """ Ensure check file raise RuntimeError if file does not exists """
        with pytest.raises(RuntimeError, match="unknown-file does not exists"):
            FilesystemService.check_file_exists("unknown-file")

    def test_check_file_exists_with_success_return_none(self):
        """ Ensure check file succeed """
        assert not FilesystemService.check_file_exists(
            self.get_datasets_dir("filesystem/dir1/file1.txt")
        )

    """
    copy_dir
    """

    def test_copy_dir_with_unknown_source_raise_runtime_error(self):
        """ Ensure copy dir raise RuntimeError if dir does not exists """
        with pytest.raises(RuntimeError, match="unknown-dir does not exists"):
            FilesystemService.copy_dir("unknown-dir", "dest")

    def test_copy_dir_with_success_return_none(self):
        """ Ensure copy dir succeed """
        assert not FilesystemService.copy_dir(
            self.get_datasets_dir("filesystem"), self.get_sandbox_dir()
        )
        self.assert_equals_resultset(
            sorted(
                [
                    str(i).replace(self.get_sandbox_dir(), ".")
                    for i in Path(self.get_sandbox_dir()).glob("**/*")
                ]
            )
        )

    """
    empty_dir
    """

    def test_empty_dir_with_unknown_dir_raise_runtime_error(self):
        """ Ensure empty dir raise RuntimeError if dir does not exists """
        with pytest.raises(RuntimeError, match="unknown-dir does not exists"):
            FilesystemService.empty_dir("unknown-dir")

    def test_empty_dir_with_success_return_none(self):
        """ Ensure empty dir succeed """
        FilesystemService.copy_dir(
            self.get_datasets_dir("filesystem"), self.get_sandbox_dir()
        )
        assert FilesystemService.empty_dir(self.get_sandbox_dir()) is None
        assert FilesystemService.is_dir_exists(self.get_sandbox_dir())
        assert not FilesystemService.is_dir_exists(self.get_sandbox_dir("dir1"))

    """
    write_file
    """

    def test_write_file_with_unknown_dir_raise_runtime_error(self):
        """ Ensure writing file raise RuntimeError if dest dir does not exists """
        with pytest.raises(RuntimeError, match="unknown-dir does not exists"):
            FilesystemService.write_file("unknown-dir/file.txt", "raise error")

    def test_write_file_with_success_return_none(self):
        """ Ensure writing file succeed """
        self.clean_sandbox()
        filename = self.get_sandbox_dir("writing_success.txt")
        FilesystemService.write_file(filename, "so successfull !!")
        assert os.path.exists(filename)
        with open(filename) as f:
            assert "so successfull !!" == f.read()

    """
    read_file
    """

    def test_read_file_with_unknown_dir_raise_runtime_error(self):
        """ Ensure reading file raise RuntimeError if file does not exists """
        filename = self.get_datasets_dir("filesystem/dir1/fileUnknown.txt")
        with pytest.raises(RuntimeError, match=f"{filename} does not exists"):
            FilesystemService.read_file(filename)

    def test_read_file_with_success_return_none(self):
        """ Ensure reading file succeed """
        self.clean_sandbox()
        filename = self.get_datasets_dir("filesystem/dir1/file1.txt")
        actual = FilesystemService.read_file(filename)
        assert actual == "file1"

    """
    check_file_can_be_created
    """

    def test_check_file_can_be_created_with_success_return_none(self):
        """ Ensure missing directories will be created """
        self.clean_sandbox()
        filename = self.get_sandbox_dir("filesystem/dir1/file1.txt")
        assert FilesystemService.check_file_can_be_created(filename) is None
        assert FilesystemService.is_dir_exists(self.get_sandbox_dir("filesystem/dir1"))
