import numpy as np

from common import HostNode, get_property_value
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from config import DEBUG


class FileWriterNode(HostNode):
    def __init__(self, name):
        super(FileWriterNode, self).__init__(name)
        self.data = self.createInputPin('data', 'AnyPin')
        self.file_path = self.createInputPin('file_path', 'StringPin')
        self.file_path.setInputWidgetVariant("FilePathWidget")
        self.file_mode = self.createInputPin('file_mode', 'StringPin', defaultValue="wb")
        self.file_mode.setValueList(["w", "wb"])
        self.data.enableOptions(PinOptions.AllowAny)
        self.data.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addInputDataType('StringPin')
        helper.addInputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Files'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def run(self, device):
        if not get_property_value(self, "file_path"):
            raise RuntimeError(f"No file path specified in {self.name} node!")
        with open(get_property_value(self, "file_path"), get_property_value(self, "file_mode")) as file:
            while self._running:
                in_data = self.queue.get()
                if in_data is not None:
                    if hasattr(in_data, 'getData'):
                        data = in_data['data'].getData()
                    else:
                        data = in_data['data']
                    data.tofile(file)
