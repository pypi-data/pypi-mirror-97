from abc import abstractmethod

from typistry.protos.valid_dict import ValidDict

class ProtoObject:

    def __init__(self, valid_dict: ValidDict):
        self.dict: ValidDict = valid_dict

    @abstractmethod
    def build_class(self):
        raise Exception("Build Class not implemented")
