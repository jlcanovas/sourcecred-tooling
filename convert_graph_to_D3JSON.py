#!/usr/bin/python
#
# Simple script to convert graphs (formats supported by igraph-python library into a D3-comaptible JSON
#
# Author: Javier Canovas (me@jlcanovas.es)
#

import getopt
import json
import sys

from igraph import Graph

"""
Usage of this script
Main options:
-i   - The path of the igraph-compatible graph file
-o   - The path for the JSON file 
"""
USAGE = 'convert_graph_to_D3JSON.py -i CRED_GRAPH_PATH -o OUTPUT_GRAPH'

def convert_to_JSON(graph):
    """Converts an igraph into a D3-compatible json file
    :returns a json Object
    """

    nodes = []
    for node in graph.vs:
        nodes.append({'id': node['index'],
                      'label': node['label'],
                      'size': node['totalCred'],
                      'type': node['type']
                      })

    edges = []
    for edge in graph.es:
        edges.append({'source': edge.source,
                      'target': edge.target,
                      'width': edge['forwardFlow'],
                      'id': str(edge.source) + "+" + str(edge.target)})

    json_g = {
        'nodes': nodes,
        'edges': edges
    }

    return json_g


def main(argv):
    if len(argv) == 0:
        sys.exit(0)

    try:
        opts, args = getopt.getopt(argv, "hi:o:", [])
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(USAGE)
            sys.exit()
        elif opt in ('-i'):
            input_graph_path = arg
        elif opt in ('-o'):
            output_path = arg

    g = Graph.Load(input_graph_path)
    json_g = convert_to_JSON(g)
    with open(output_path, 'w') as f:
        json.dump(json_g, f)


if __name__ == "__main__":
    main(sys.argv[1:])
