#!/usr/bin/python
#
# This script injects a weights definition (given as a json file) into a cred graph definition (also given as json
# file). The cred graph term refers to the graph created by the cli graph command
#
# Author: Javier Canovas (me@jlcanovas.es)
#

import getopt
import json
import sys

"""
Usage of this script
Main options:
-w   - The path of the weight definition
-g   - The path of the cred graph
-o   - The path of the resulting graph
"""
USAGE = 'inject_weights_to_graph.py -w WEIGHTS_JSON_FILE -g GRAPH_JSON_FILE -o OUTPUT_GRAPH'

def main(argv):
    if len(argv) == 0:
        sys.exit(0)

    try:
        opts, args = getopt.getopt(argv, "hw:g:o:", [])
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(USAGE)
            sys.exit()
        elif opt in ('-w'):
            input_weights = arg
        elif opt in ('-g'):
            input_graph = arg
        elif opt in ('-o'):
            output_graph = arg

    with open(input_weights, encoding="utf8") as f:
        weights = json.load(f)

    with open(input_graph, encoding="utf8") as f:
        cred = json.load(f)

    cred[1]['weightsJSON'] = weights

    with open(output_graph, "w", encoding="utf8") as f:
        json.dump(cred, f)


if __name__ == "__main__":
    main(sys.argv[1:])