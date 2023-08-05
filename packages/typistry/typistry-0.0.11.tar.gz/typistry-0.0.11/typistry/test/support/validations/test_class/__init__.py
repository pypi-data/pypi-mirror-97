from typistry.protos.proto_object import ProtoObject
from typistry.test.support.types.test_class import TestClass

class TestClassProto(ProtoObject):

    def build_class(self):
        return TestClass
