from dataclasses import dataclass

@dataclass
class TypedDict:
    attrs: dict
    type: str
    
    def attributes(self):
        return self.attrs
    
    def all_attributes(self):
        atts = self.attrs.copy()
        atts["type"] = self.type
        return atts
