import json


def parse_json(file_path: str):
    with open(file_path) as f:
        return json.load(f)
