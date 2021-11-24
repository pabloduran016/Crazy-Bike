import json
import os.path
from typing import Dict


class JsonManager:
    f: str

    def __init__(self, file: str):
        self.f = file

    def load(self) -> Dict:
        if not os.path.exists(self.f):
            return {
                "coins": 0, "highscore": 0, "costumes": {
                    "frontwheel": "bike",
                    "backwheel": "bike",
                    "board": "bike",
                }
            }
        with open(self.f, 'r') as f:
            loaded_data = json.load(f)
        return loaded_data

    def update(self, data: Dict) -> None:
        with open(self.f, 'w') as f:
            json.dump(data, f, indent=4)
