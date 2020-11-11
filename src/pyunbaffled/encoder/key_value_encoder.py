from parsers.structure_code import StructureCode
import json


class KeyValueEncoder(json.JSONEncoder):
    def default(self, record):
        if isinstance(record, StructureCode):
            structureCode = {
                name: field['value']
                for (name, field) in record.fields.items()
            }
            structureCode['modules'] = [{
                name: field['value']
            } for module in record.modules
                                        for (name,
                                             field) in module.fields.items()]
            return structureCode
        else:
            return super().default(record)