from os import path
from shutil import copytree, rmtree
from typing import List, Union, Any, Tuple

from test.support.types.source_class import SourceClass
from typistry.test.support.types.other_class import OtherClass

from typistry.protos.invalid_object import InvalidObject
from typistry.test.support.types.test_class import TestClass
from typistry.util.path import from_root
from typistry.validators.base import validate_files, filter_type

class TestValidations:

    def schemas_path(self) -> str:
        return from_root("/test/support/validations/")

    def yaml_path(self) -> str:
        return from_root("/test/support/yaml/")

    def all_protos(self) -> List[Union[Any, InvalidObject]]:
        return validate_files(self.yaml_path(), self.schemas_path())
    
    def filter_by_types(self, all: List[Any]) -> Tuple[List[TestClass], List[OtherClass], List[InvalidObject]]:
        test_class = filter_type(all, TestClass)
        other_class = filter_type(all, OtherClass)
        invalid = filter_type(all, InvalidObject)
        return (test_class, other_class, invalid)

    def test_single_file(self):
        yaml_path = from_root("/test/support/yaml/test_class/good_1.yaml")
        obj = validate_files(yaml_path, self.schemas_path())
        assert(len(obj) == 1)
        assert(isinstance(obj[0], TestClass))

    def test_directory(self):
        all = self.all_protos()
        test_class, other_class, invalid = self.filter_by_types(all)

        assert(len(test_class) == 2)
        assert(len(other_class) == 1)
        # Tests protoclass build definition adds 10, otherwise would be 2
        assert(other_class[0].test == 12)
        assert(len(invalid) == 4)

    def test_default_schema_path(self):
        default_path = "validations/"
        if not path.exists(default_path):
            copytree(self.schemas_path(), default_path)

        all = validate_files(self.yaml_path())
        assert(len(all) == 7)
        test_class, other_class, invalid = self.filter_by_types(all)

        assert(len(test_class) == 2)
        assert(len(other_class) == 1)
        assert(len(invalid) == 4)

        if path.exists(default_path):
            rmtree(default_path)

    def test_to_class(self):
        test_class_all = validate_files(self.yaml_path(), self.schemas_path(), to_class = TestClass)
        test_class, other_class, invalid = self.filter_by_types(test_class_all)
        assert(len(test_class) == 2)
        assert(len(other_class) == 0)
        assert(len(invalid) == 5)

        other_class_all = validate_files(self.yaml_path(), self.schemas_path(), to_class = OtherClass)
        test_class, other_class, invalid = self.filter_by_types(other_class_all)
        assert(len(test_class) == 0)
        assert(len(other_class) == 1)
        assert(len(invalid) == 6)
        
    def test_include_source(self):
        source_class = validate_files(self.yaml_path() + "/source_class/good_1.yaml", self.schemas_path(), include_source=True)
        assert(len(source_class) == 1)
        assert(isinstance(source_class[0], SourceClass))


