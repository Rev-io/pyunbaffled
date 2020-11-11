class StructureCode:
    def __init__(self, recordDescriptorWord, hexadecimalIdentifier,
                 structureCode):
        self.fields = {
            'record_descriptor_word': recordDescriptorWord,
            'hexadecimal_identifier': hexadecimalIdentifier,
            'structure_code': structureCode
        }
        self.length = int(recordDescriptorWord['value'][:4], 16)
        self.content_length = self.length - recordDescriptorWord[
            'length'] - structureCode['length'] - hexadecimalIdentifier[
                'length']
        self.structureCode = structureCode['value'][1:]
        self.hexadecimalIdentifier = hexadecimalIdentifier['value']
        self.modules = []
        self.invalid = False

    def addField(self, fieldName, field):
        self.fields[fieldName] = field

    def addModule(self, module):
        self.modules.append(module)

    def markInvalid(self):
        self.invalid = True
