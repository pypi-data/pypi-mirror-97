from typing import Optional

import yaml
from returns.result import Result, Success, Failure

from typistry.protos.invalid_object import InvalidObject, IgnorableObject

from typistry.protos.typed_dict import TypedDict

def safe_parse_yaml(file: str, include_file: bool = False, filter_type: Optional[str] = None) -> Result[TypedDict, InvalidObject]:
    try:
        with open(file, 'r') as stream:
            try:
                yaml_load = yaml.safe_load(stream)
                if isinstance(yaml_load, dict):
                    to_type = yaml_load.get("type")
                    if isinstance(to_type, str):
                        if (filter_type == None) or (to_type == filter_type):
                            yaml_load.pop("type")
                            if include_file:
                                yaml_load["source"] = file
                            return Success(TypedDict(yaml_load, type=to_type))
                        else:
                            return Failure(IgnorableObject(f"Parsed object type: {to_type} does not match specified filter_type {filter_type}", file))
                    else:
                        return Failure(IgnorableObject("Invalid YAML {file}: {yaml_load}.  Parsed object must contain 'type'", file))
                else:
                    return Failure(InvalidObject(f"\nInvalid YAML {file}: {yaml_load}.  Parsed object must be a dict", file))
            except yaml.YAMLError as exc:
                return Failure(InvalidObject(f"\nInvalid YAML {file}: {exc}\n", file))
    except FileNotFoundError as e:
        return Failure(InvalidObject(f"Specified YAML does not exist: {e}", file))

