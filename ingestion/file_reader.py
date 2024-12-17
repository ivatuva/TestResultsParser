import os

class FileReader:
    def __init__(self, file_path, tech):
        self.file_path = file_path
        self.tech = tech

    def read_file(self):

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file at {self.file_path} does not exist.")
        
        if not os.path.isfile(self.file_path):
            raise ValueError(f"The path {self.file_path} is not a file.")
        
        with open(self.file_path, 'r') as file:
            content = file.read()
        
        return content