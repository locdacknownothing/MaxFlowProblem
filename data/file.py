import json


def dump_json(file, data):
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        print(str(e))


def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.dump(f)
            return data
    except Exception as e:
        print(str(e))
