class StructureCode:
    def __init__(self, line_number, record_descriptor_word,
                 hexadecimal_identifier, structure_code):
        self.fields = {
            'record_descriptor_word': record_descriptor_word,
            'hexadecimal_identifier': hexadecimal_identifier,
            'structure_code': structure_code
        }
        self.length = int(record_descriptor_word['value'][:4], 16)
        self.remaining_characters = self.length
        self.remaining_characters -= record_descriptor_word['length']
        self.remaining_characters -= structure_code['length']
        self.remaining_characters -= hexadecimal_identifier['length']
        self.structure_code = structure_code['value'][1:]
        self.hexadecimal_identifier = hexadecimal_identifier['value']
        self.line_number = line_number
        self.modules = []
        self.invalid = False

    def addField(self, fieldName, field):
        self.fields[fieldName] = field
        self.remaining_characters -= field['length']

    def addModule(self, module):
        self.modules.append(module)
        self.remaining_characters -= module.length

    def markInvalid(self):
        self.invalid = True
