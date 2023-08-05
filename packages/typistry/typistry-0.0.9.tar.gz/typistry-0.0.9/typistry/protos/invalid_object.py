from dataclasses import dataclass
from typing import Union

from typistry.protos.typed_dict import TypedDict
from typistry.protos.valid_dict import ValidDict

@dataclass
class InvalidObject:
    message: str
    reference: Union[str, dict, TypedDict, ValidDict]
    
@dataclass
class IgnorableObject(InvalidObject):
    pass


