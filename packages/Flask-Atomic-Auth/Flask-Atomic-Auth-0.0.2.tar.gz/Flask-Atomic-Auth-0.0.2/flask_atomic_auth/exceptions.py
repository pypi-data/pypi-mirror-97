class MissingSettingsFile(IOError):
    def __init__(self, msg='Missing extension configuration keys'):
        super().__init__(msg)
