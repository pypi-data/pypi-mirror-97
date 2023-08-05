from protos.proto_object import ProtoObject
from test.support.types.source_class import SourceClass


class SourceClassProto(ProtoObject):

    def build_class(self):
        return SourceClass