import argparse
import csv
import json
import os

import jsonschema
from icecream import ic
from jsonschema import validate


def get_schema():
    with open('our_schema.json', 'r') as file:
        schema = json.load(file)
    return schema


def validate_json(json_data):
    execute_api_schema = get_schema()
    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        ic(err)
        print(type(err))
        return False, err
    message = "Given JSON data is Valid"
    return True, message


def is_valid(dir_path):
    total = 0
    valid_cnt = 0

    with open(f'results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "json_file", "error message"])
        for folder in sorted(os.listdir(dir_path)):
            path = f"{dir_path}/{folder}"
            for files in sorted(os.listdir(path)):
                if files.endswith(".json"):
                    total += 1
                    f = open(f"{path}/{files}")
                    json_data = json.load(f)
                    is_valid, message = validate_json(json_data)
                    if is_valid:
                        valid_cnt += 1
                    else:
                        print(f"{files} : {message}")
                        writer.writerow([folder, files, message])
        writer.writerow(
            ["", "Score", f"{valid_cnt}/{total}={valid_cnt / total}"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_path", type=str)
    args = parser.parse_args()

    is_valid(args.dir_path)
