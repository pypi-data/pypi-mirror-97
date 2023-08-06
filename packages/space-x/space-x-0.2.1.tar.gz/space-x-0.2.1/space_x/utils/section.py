class Section:
    def __init__(self, name, **kwargs):
        self.name = name
        self.parameters = kwargs

    def get_parameters(self):
        return [(f"{self.name}:{k}", v) for k, v in self.parameters.items()]
