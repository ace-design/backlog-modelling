#!/usr/bin/env python3
import json

""" 
    ##############################################################################
    # Transform the global JSON file obtained out of visual narrator into chunks #
    ############################################################################## 
    This is a standalone script used to transform a data format into another    
"""

INPUT_FILE = "./data.json"
OUTPUT_DIR = "./../cases/"


def transform(path):
    """Transform VN output into a JSON representation"""
    raw_json = load(path)
    extracted = process(raw_json)
    for case_id in extracted:
        export(case_id, extracted[case_id])


def load(path):
    """load the input (global) file"""
    with open(path) as f:
        raw = json.load(f)
    return raw


def process(json_data):
    """organize the data into a case-based dictionary"""
    result = dict()
    for entry in json_data:
        try:
            data = dict()
            data['identifier'] = entry['case'] + "_" + entry['id']
            data['text'] = entry['userstory']
            data['entities'] = entry['entity']
            data['personas'] = entry['actor']
            data['actions'] = entry['control']
            if result.get(entry["case"]) is None:
                result[entry["case"]] = list()
            result[entry["case"]].append(data)
        except KeyError:
            continue
    return result


def export(case_id, contents):
    """Pretty print the collected data as JSON files"""
    data = dict()
    data['case'] = case_id
    data['stories'] = contents
    with open(f"{OUTPUT_DIR}/{case_id}.json", 'w') as outfile:
        json.dump(data, outfile, indent=2)


# Start the transformation process when invoked
if __name__ == "__main__":
    transform(INPUT_FILE)
