from dataclasses import dataclass
from typistry.protos.typed_dict import TypedDict

@dataclass
class ValidDict:
    typed_dict: TypedDict
    schema: dict
    
    def attributes(self) -> dict:
        return self.typed_dict.attrs

    def type(self) -> str:
        return self.typed_dict.type

