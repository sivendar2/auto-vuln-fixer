import json

def load_cwe_map(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def map_sonar_to_cwe(rule, mapping):
    return mapping.get(rule)