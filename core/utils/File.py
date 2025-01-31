class File:
    def __init__(self, file: str) -> None:
        self.filePath = file

    @property
    def file(self):
        return self.filePath

    @file.setter
    def file(self, value):
        self.filePath = value