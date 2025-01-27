import os

class FileReader:
    def __init__(self, path, tech):
        self.path = path
        self.tech = tech

    def read_file(self):
        contents = []
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"The file at {self.path} does not exist.")
        
        if os.path.isfile(self.path):
            with open(self.path, 'r') as file:
                contents.append(file.read())
        else:
            for filename in os.listdir(self.path):
                f = os.path.join(self.path, filename)
                if os.path.isfile(f):
                    with open(f, 'r') as file:
                        contents.append(file.read())
        return contents