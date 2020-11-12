from ..parsers.structure_code import StructureCode
from ..parsers.module import Module


def createField(rawValue, schema):
    hexRawValue = rawValue.hex()
    return {
        'raw': hexRawValue,
        'table_number': schema["table_number"],
        'has_sign': schema["has_sign"],
        'length': schema["length"],
        'value':
        hexRawValue[:-1] if schema["has_sign"] == True else hexRawValue
    }


def createInvalidField(rawValue, length):
    hexRawValue = rawValue.hex()
    return {
        'raw': hexRawValue,
        'table_number': None,
        'has_sign': None,
        'length': length,
        'value': hexRawValue
    }


class FileParser:
    def __init__(self, file_name, mode, structureCodeRepository,
                 moduleRepository):
        self.file_name = file_name
        self.mode = mode
        self.structureCodeRepository = structureCodeRepository
        self.moduleRepository = moduleRepository
        self.structureCodeMetadataSchema = structureCodeRepository.get_schema(
            "metadata")
        self.moduleCodeMetadataSchema = moduleRepository.get_schema("metadata")
        self.recordDescriptorWordSchema = self.structureCodeMetadataSchema[
            'record_descriptor_word']
        self.hexadecimalIdentifierSchema = self.structureCodeMetadataSchema[
            'hexadecimal_identifier']
        self.structureCodeSchema = self.structureCodeMetadataSchema[
            'structure_code']
        self.moduleCodeLength = self.moduleCodeMetadataSchema[
            "module_code_identification"]["length"]
        self.line_number = 0

    def __enter__(self):
        self.fd = open(self.file_name, self.mode)
        return self

    def __exit__(self, type, value, tb):
        self.fd.close()

    def __iter__(self):
        return self

    def __next__(self):
        self.line_number += 1
        rdw = self.fd.read(self.recordDescriptorWordSchema['length'])
        if rdw == b'':
            raise StopIteration()

        structure_code = StructureCode(
            self.line_number,
            createField(rdw, self.recordDescriptorWordSchema),
            createField(
                self.fd.read(self.hexadecimalIdentifierSchema['length']),
                self.hexadecimalIdentifierSchema),
            createField(self.fd.read(self.structureCodeSchema['length']),
                        self.structureCodeSchema),
        )

        structure_code_schema = self.structureCodeRepository.get_schema(
            structure_code.structure_code)

        if structure_code_schema == None:
            structure_code.markInvalid()
            structure_code.addField(
                "invalid",
                createInvalidField(
                    self.fd.read(structure_code.remaining_characters),
                    structure_code.remaining_characters))
        else:
            for (name, fieldSchema) in structure_code_schema.items():
                structure_code.addField(
                    name,
                    createField(self.fd.read(fieldSchema['length']),
                                fieldSchema))

            while structure_code.remaining_characters > 0:
                module_code = createField(
                    self.fd.read(self.moduleCodeLength), self.
                    moduleCodeMetadataSchema["module_code_identification"])

                module_schema = self.moduleRepository.get_schema(
                    module_code['value'])
                module = Module(module_code)

                if module_schema == None:
                    module.markInvalid()
                    remaining_characters = structure_code.remaining_characters - module.length
                    module.addField(
                        "invalid",
                        createInvalidField(self.fd.read(remaining_characters),
                                           remaining_characters))
                    structure_code.addModule(module)
                else:
                    for (name, fieldSchema) in module_schema.items():
                        module.addField(
                            name,
                            createField(self.fd.read(fieldSchema['length']),
                                        fieldSchema))

                    structure_code.addModule(module)

        return structure_code