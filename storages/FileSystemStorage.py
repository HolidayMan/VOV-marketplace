import os


class FileSystemStorage:
    def __init__(self, path: str, base_url: str):
        self.path = path
        self.base_url = base_url

    def save(self, filename, content):
        with open(os.path.join(self.path, filename), 'wb') as f:
            f.write(content)

    def delete(self, filename):
        os.remove(os.path.join(self.path, filename))

    def exists(self, filename):
        return os.path.exists(os.path.join(self.path, filename))

    def list(self):
        return os.listdir(self.path)

    def url(self, filename):
        return os.path.join(self.base_url, filename)
