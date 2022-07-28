#!/usr/bin/env python

import json
import yaml
import os


def load_config(filename):
    """Load configuration from a yaml file"""
    with open(filename) as f:
        return yaml.safe_load(f)


def save_config(config, filename):
    """Save configuration to a yaml file"""
    with open(filename, "w+") as f:
        yaml.safe_dump(config, f, default_flow_style=False)


def pretty_print_json(data):
    print(json.dumps(data, indent=4, sort_keys=True))

def write_json2file(data, destination):
    if os.path.isdir('.test_data') == False:
        os.mkdir('.test_data')
    j = json.dumps(data, indent=4)
    with open(".test_data/"+destination, "w") as outfile:
        outfile.write(j)