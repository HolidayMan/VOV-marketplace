import os


class FileSystemStorage:
    def __init__(self, path):
        self.path = path

    def save(self, filename, content):
        with open(os.path.join(self.path, filename), 'wb') as f:
            f.write(content)

    def delete(self, filename):
        os.remove(os.path.join(self.path, filename))

    def exists(self, filename):
        return os.path.exists(os.path.join(self.path, filename))

    def list(self):
        return os.listdir(self.path)
