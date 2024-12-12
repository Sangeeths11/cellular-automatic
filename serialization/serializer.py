import json

from serialization.serializable import Serializable


class Serializer:
    def __init__(self):
        pass

    def gather_data(self, data: Serializable):
        data = data.get_serialization_data()
        if type(data) is dict:
            for key, value in data.items():
                if isinstance(value, Serializable):
                    data[key] = self.serialize(value)

        elif type(data) is list:
            for index, value in enumerate(data):
                if isinstance(value, Serializable):
                    data[index] = self.serialize(value)

        elif isinstance(data, Serializable):
            data = self.serialize(data)

        return data

    def serialize (self, data: Serializable) -> str:
        return json.dumps(self.gather_data(data))