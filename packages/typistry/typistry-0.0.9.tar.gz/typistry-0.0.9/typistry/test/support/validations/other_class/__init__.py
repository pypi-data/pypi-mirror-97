from typistry.protos.proto_object import ProtoObject
from typistry.test.support.types.other_class import OtherClass

class OtherClassProto(ProtoObject):

    def build_class(self):
        return OtherClass

    def build(self):
        return OtherClass(self.dict.attributes()["test"] + 10)
