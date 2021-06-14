import json
from typing import Dict


class JsonManager:
    f: str

    def __init__(self, file: str):
        self.f = file

    def load(self) -> Dict:
        with open(self.f, 'r') as f:
            loaded_data = json.load(f)
        return loaded_data

    def update(self, data: Dict) -> None:
        with open(self.f, 'w') as f:
            json.dump(data, f)
