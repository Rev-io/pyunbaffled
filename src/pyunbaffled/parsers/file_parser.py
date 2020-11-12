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

    def __enter__(self):
        self.fd = open(self.file_name, self.mode)
        return self

    def __exit__(self, type, value, tb):
        self.fd.close()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            print('Read record')
            current_length = 0
            current_length += self.recordDescriptorWordSchema['length']
            rdw = self.fd.read(self.recordDescriptorWordSchema['length'])
            if rdw == b'':
                raise StopIteration()

            current_length += self.hexadecimalIdentifierSchema['length']
            current_length += self.structureCodeSchema['length']
            structureCode = StructureCode(
                createField(rdw, self.recordDescriptorWordSchema),
                createField(
                    self.fd.read(self.hexadecimalIdentifierSchema['length']),
                    self.hexadecimalIdentifierSchema),
                createField(self.fd.read(self.structureCodeSchema['length']),
                            self.structureCodeSchema),
            )

            structureCodeSchema = self.structureCodeRepository.get_schema(
                structureCode.structureCode)

            if structureCodeSchema == None:
                structureCode.markInvalid()
                structureCode.addField(
                    "invalid",
                    createInvalidField(
                        self.fd.read(structureCode.content_length),
                        structureCode.content_length))
            else:
                for (name, fieldSchema) in structureCodeSchema.items():
                    current_length += fieldSchema['length']
                    structureCode.addField(
                        name,
                        createField(self.fd.read(fieldSchema['length']),
                                    fieldSchema))
                while current_length < structureCode.length:
                    current_length += self.moduleCodeLength
                    moduleCode = createField(
                        self.fd.read(self.moduleCodeLength), self.
                        moduleCodeMetadataSchema["module_code_identification"])
                    moduleSchema = self.moduleRepository.get_schema(
                        moduleCode['value'])
                    module = Module(moduleCode)
                    if moduleSchema == None:
                        module.markInvalid()
                        print(
                            f"structureCode.content_length: {structureCode.content_length}, current_length: {current_length}"
                        )
                        module.addField(
                            "invalid",
                            createInvalidField(
                                self.fd.read(structureCode.content_length -
                                             current_length),
                                structureCode.content_length - current_length))
                        structureCode.addModule(moduleCode['value'], module)
                    else:
                        for (name, fieldSchema) in moduleSchema.items():
                            current_length += fieldSchema['length']
                            module.addField(
                                name,
                                createField(
                                    self.fd.read(fieldSchema['length']),
                                    fieldSchema))
                            structureCode.addModule(module)

            print(
                f'structureCode: {structureCode.structureCode}, length: {structureCode.length}'
            )
            return structureCode