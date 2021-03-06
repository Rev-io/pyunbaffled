from ..parsers.structure_code import StructureCode
import json
import urllib.parse


class KeyValueEncoder(json.JSONEncoder):
    def default(self, record):
        if isinstance(record, StructureCode):
            structureCode = {
                name: field['value']
                for (name, field) in record.fields.items()
            }
            structureCode['file_name'] = urllib.parse.unquote(
                record.file_name.rsplit('/', 1)[-1])
            structureCode['line_number'] = record.line_number
            structureCode['modules'] = []

            for module in record.modules:
                processed_module = {}
                for (name, field) in module.fields.items():
                    processed_module[name] = field['value']
                structureCode['modules'].append(processed_module)

            return structureCode
        else:
            return super().default(record)