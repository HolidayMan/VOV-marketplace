import os


class FileSystemStorage:
    def __init__(self, path: str, base_url: str):
        self.path = path
        self.base_url = base_url

    def save(self, filename, content):
        path = os.path.join(self.path, filename)
        if os.path.exists(path):
            return
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(path, 'wb') as f:
            f.write(content)

    def delete(self, filename):
        os.remove(os.path.join(self.path, filename))

    def exists(self, filename):
        return os.path.exists(os.path.join(self.path, filename))

    def url(self, filename):
        if filename.startswith('/'):
            filename = filename[1:]
        return os.path.join(self.base_url, filename)
