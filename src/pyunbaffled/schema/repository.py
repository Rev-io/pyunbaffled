import os
import json


class Repository:
    def __init__(self, base_path, type):
        self.data = {}
        self.type = type
        self.base_path = base_path

    def get_schema(self, key):
        file_path = os.path.join(self.base_path, "schema", self.type,
                                 f"{key}.json")
        if key not in self.data:
            if os.path.exists(file_path):
                with open(file_path) as f:
                    jsonSchema = json.load(f)
                    self.data[key] = {
                        field['name']: {
                            'has_sign': field['has_sign'],
                            'table_number': field['table_number'],
                            'length': field['length']
                        }
                        for field in jsonSchema['fields']
                    }
            else:
                self.data[key] = None

        return self.data[key]
