import json


class JsonManager:
    f: str

    def __init__(self, file):
        self.f = file

    def load(self):
        with open(self.f, 'r') as f:
            loaded_data = json.load(f)
        return loaded_data

    def update(self, data):
        with open(self.f, 'w') as f:
            json.dump(data, f)
