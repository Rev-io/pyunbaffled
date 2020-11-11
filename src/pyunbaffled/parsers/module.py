class Module:
    def __init__(self, moduleCode):
        self.fields = {'module_code_identification': moduleCode}
        self.invalid = False

    def addField(self, fieldName, field):
        self.fields[fieldName] = field

    def markInvalid(self):
        self.invalid = True
