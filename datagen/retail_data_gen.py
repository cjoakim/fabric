"""
Usage:
    python retail_data_gen.py generate 
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "March 2024"

import json
import os
import random
import sys
import time
import traceback

from docopt import docopt

from pysrc.retail_data_gen import RetailDataGenerator

def generate():

    rdg = RetailDataGenerator()

    json_lines = rdg.generate_stores(100)
    write_lines("../data/retail/stores.json", json_lines)
    
    json_lines = rdg.generate_products(1000)
    write_lines("../data/retail/products.json", json_lines)

    json_lines = rdg.generate_customers(2000)
    write_lines("../data/retail/customers.json", json_lines)

    for year in "2023,2024".split(","):
        for month in "01,02,03,04,05,06,07,08,09,10,11,12".split(","):
            json_lines = rdg.generate_sales(year, month)
            outfile = "../data/retail/sales_{}_{}.json".format(year, month)
            write_lines(outfile, json_lines)

    md = rdg.markdown_doc()
    write("../data/retail/sample_data.md", md)


def read_json_objects(infile):
    objects = list()
    it = text_file_iterator(infile)
    for i, line in enumerate(it):
        s = line.strip()
        if len(s) > 3:
            obj = json.loads(line.strip())
            objects.append(obj)        
    return objects

def text_file_iterator(infile):
    # return a line generator that can be iterated with iterate()
    with open(infile, 'rt') as f:
        for line in f:
            yield line.strip()

def write_lines(outfile, lines):
    with open(outfile, 'wt') as out:
        for line in lines:
            out.write(line.strip())
            out.write(os.linesep)
    print('file_written: {}'.format(outfile))

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

def write_obj_as_json_file(outfile, obj):
    txt = json.dumps(obj, sort_keys=False, indent=2)
    with open(outfile, 'wt') as f:
        f.write(txt)
    print("file written: " + outfile)

def write(outfile: str, string_value: str, verbose=True) -> None:
    """Write the given string to the given file."""
    if outfile is not None:
        if string_value is not None:
            with open(file=outfile, encoding="utf-8", mode="w") as file:
                file.write(string_value)
                if verbose is True:
                    print(f"file written: {outfile}")
                    
def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        if func == 'generate':
            generate()
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
