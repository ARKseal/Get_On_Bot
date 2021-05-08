import json as _json
import threading as _threading
import time as _time

from Task_List import *


class Json_Handler(_threading.Thread):
    
    def __init__(self, file='data.json'):
        super().__init__()
        self._FILE_NAME = file
        with open(self._FILE_NAME, 'r') as f:
            self.VALUES = _json.load(f)
        _time.sleep(10)
        self.start()

    def __getitem__(self, key):
        if key in self.VALUES:
            return self.VALUES[key]
        raise KeyError("Key '{}' is not found".format(key))
    
    def __setitem__(self, key, value):
        self.VALUES[key] = value

    def __delitem___(self, key):
        raise TypeError("'Json_Handler' object does not support item deletion")

    def run(self):
        while True:
            with open(self._FILE_NAME, 'w') as f:
                _json.dump(self.VALUES, f)
            _time.sleep(5)

    def getData(self):
        return self.VALUES