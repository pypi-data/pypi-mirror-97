# -*- coding: utf-8 -*-

class Serializer(object):
    def __init__(self):
        self.result = None
        self.dispatch_methods = {}

    def dispatch(self, value):
        if isinstance(value, (str, int, float, type(None), bool)):
            self.from_atoms(value)
        elif isinstance(value, (tuple, list)):
            self.from_array(value)
        elif isinstance(value, dict):
            self.from_dict(value)
        elif hasattr(value, '__awdb_repr__'):
            self.from_awdb_type(value)
        elif type(value) in self.dispatch_methods:
            self.dispatch_methods[type(value)](self, value)
        else:
            self.from_any(value)

    def define_dispatch(self, type, callable):
        self.dispatch_methods[type] = callable

    def from_awdb_type(self, data):
        self.result = data.__awdb_repr__()

    def from_dict(self, data):
        res = {}

        for key, value in data.items():
            self.dispatch(key)
            key2 = self.result

            if not isinstance(key2, str):
                key2 = repr(key2)

            self.dispatch(value)
            value2 = self.result

            res[key2] = value2

        self.result = res

    def from_atoms(self, data):
        self.result = data

    def from_any(self, data):
        self.result = repr(data)

    def from_array(self, data):
        accum = []

        for value in data:
            self.dispatch(value)
            accum.append(self.result)

        self.result = accum

    def serialize(self, value):
        self.dispatch(value)
        return self.result
