class Module:
    def __init__(self, moduleCode):
        self.fields = {'module_code_identification': moduleCode}
        self.module_code_identification = moduleCode['value']
        self.invalid = False
        self.length = moduleCode['length']

    def addField(self, fieldName, field):
        self.fields[fieldName] = field
        self.length += field['length']

    def markInvalid(self):
        self.invalid = True
