from importlib.util import spec_from_file_location, module_from_spec 
from os import path, walk
from typing import TypeVar, Type, List, Optional, Union, Any

from jsonschema import SchemaError, validate, ValidationError
from returns.result import Failure, Result, Success

from typistry.protos.invalid_object import InvalidObject, IgnorableObject
from typistry.protos.typed_dict import TypedDict
from typistry.protos.valid_dict import ValidDict
from typistry.util.json import parse_json
from typistry.validators.yaml import safe_parse_yaml
from typistry.util.list import sequence as list_sequence
from typistry.util.exception import message
from typistry.protos.proto_object import ProtoObject

R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T', bound='ProtoObject')

def filter_type(objects: List[Any], cls: Type[R]) -> List[R]:
    return [x for x in objects if isinstance(x, cls)]

def sequence(objects: List[Union[R, InvalidObject]], cls: Type[R]):
    return list_sequence(objects, cls, InvalidObject)

def validate_files(file_path: str, schema_path: Optional[str] = None, to_class: Optional[Type[R]] = None, proto_class: Optional[Type[T]] = None, include_source: bool = False) -> List[Union[R, InvalidObject]]:
    all_paths: List[str] = []
    
    if path.isdir(file_path):
        for r, d, f in walk(file_path):
            for file in f:
                all_paths.append(path.join(r, file))
    elif path.isfile(file_path):
        all_paths.append(file_path)
    else:
        raise Exception("Invalid file_path.  Is not file or directory.")
    
    all: List[Union[R, InvalidObject]] = list(map(lambda p: validate_file(p, schema_path, to_class, proto_class, include_source)._inner_value, all_paths))
    result = [x for x in all if not isinstance(x, IgnorableObject)]
    
    return result
    
def validate_file(file: str, schema_path: Optional[str], to_class: Optional[Type[R]] = None, proto_class: Optional[Type[T]] = None, include_source: bool = False) -> Result[R, InvalidObject]:
    schema_source: str = schema_path or "validations/"

    return parse_file(file, include_source) \
        .bind(lambda d: validate_dict(d, schema_source)) \
        .bind(lambda d: build_object(d, schema_source, to_class, proto_class))

def parse_file(file_path: str, include_source: bool = False) -> Result[TypedDict, InvalidObject]:
    if '.yaml' in file_path or '.yml' in file_path:  # TODO: Improve file type checking
        return safe_parse_yaml(file_path, include_source)
    else:
        return Failure(IgnorableObject("File type not supported", file_path))

def validate_dict(data: TypedDict, schema_source: str) -> Result[ValidDict, InvalidObject]:
    schema_file = schema_source + f"{data.type}/" + "schema.json"
    try:
        schema = parse_json(schema_file)
        validate(data.all_attributes(), schema)
        return Success(ValidDict(typed_dict=data, schema=schema))
    except SchemaError as e:
        return Failure(InvalidObject(f"Schema error {schema_file}: {e.message}", data))
    except ValidationError as e:
        return Failure(InvalidObject(f"Schema error {schema_file}: {e.message}", data))
    except FileNotFoundError as e:
        return Failure(InvalidObject(f"Schema not found: {e.filename}", data))


def build_object(dict: ValidDict, schema_source: Optional[str] = None, to_class: Optional[Type[R]] = None, protoclass: Optional[Type[T]] = None) -> Result[R, InvalidObject]:
    built: Result[R, InvalidObject]
    if to_class:
        if (to_class.__name__) == to_class_case(dict.type()): # TODO: Allow type to be optional which would skip this check
            built = build_object_from_class(dict, to_class)
            return built
        else:
            return Failure(InvalidObject(f"InvalidObject, to_class : {to_class.__name__} does not match data class {dict.type()}", dict))
    else:
        protocls: Type[T]
        if not protoclass:
            if not schema_source:
                return Failure(InvalidObject("At least one of schema_source, to_class or protoclass must be provided", dict))
            else:
                type_name = dict.type()
                init_path = schema_source + f"{type_name}/" + "__init__.py"
                protocls = get_protoclass(type_name, init_path)
        else:
            protocls = protoclass
                
        if "build" in dir(protocls):
            return build_object_from_protoclass(dict, protocls)
        else:
            build_class: Type[R] = get_build_class(dict, protocls)
            return build_object_from_class(dict, build_class)
    
def build_object_from_protoclass(dict: ValidDict, protocls: Type[T]) -> Result[R, InvalidObject]:
    try:
        obj = protocls(dict).build() # type: ignore
        return Success(obj)
    except Exception as e:
        return Failure(InvalidObject(f"Error building from protoclass, check json schema matches protoclass build definition: {message(e)}", dict))

def build_object_from_class(dict: ValidDict, cls: Type[R]) -> Result[R, InvalidObject]:
    try:
        obj = cls(**dict.attributes()) # type: ignore
        return Success(obj)
    except Exception as e:
        return Failure(InvalidObject(f"Error building class, check json schema matches class definition: {message(e)}", dict))
    
def to_class_case(s: str) -> str:
    return "".join(list(map(lambda c: c.capitalize(), s.split("_"))))

def get_proto(dict: ValidDict, cls: Type[T]) -> T:
    return cls(dict)

def get_build_class(dict: ValidDict, protoclass: Type[T]) -> R:
    proto = get_proto(dict, protoclass)
    return proto.build_class()

def get_protoclass(type_name: str, init_path: str) -> Type[T]:
    proto_class_name = to_class_case(type_name) + "Proto"
    spec = spec_from_file_location("module.name", init_path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return getattr(mod, proto_class_name)
