#!/usr/bin/python
#
# Generates a CSV file from credResult graphs. The CSV is printed in STDOUT. Useful for further analysis in other tools
#
# The CSV file follows this format (example):
#    id,cred,type,name
#    12,21.2,COMMIT,ssjw22
#    17,12.4,ISSUE,2
#
# Author: Javier Canovas (me@jlcanovas.es)
#

import getopt
import json
import sys

"""
Usage of this script
Main options:
-g   - The path of the cred graph
"""
USAGE = 'analyze_credResult_cred.py -g GRAPH_JSON_FILE'


def extract_node_name(node_address):
    """Given a graph node address, returns the label. For the sake of clarity, COMMENT node addresses return empty.
    :param node_address: The node address
    :return: The label
    """
    node_type = node[2]
    if node_type == "COMMIT":
        return node[3][-7:]
    elif node_type == "REPO":
        return node[3] + '/' + node[4]
    elif node_type == "USERLIKE":
        return node[4]
    elif node_type == "ISSUE":
        return node[5]
    elif node_type == "REPO":
        return node[5]
    elif node_type == "COMMENT":
        return ""


def main(argv):
    if len(argv) == 0:
        print(USAGE)
        sys.exit(0)

    try:
        opts, args = getopt.getopt(argv, "hg:", [])
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(USAGE)
            sys.exit()
        elif opt in '-g':
            input_graph = arg

    # Let's go directly to the point (no need for helper functions)
    with open(input_graph, encoding="utf8") as f:
        cred = json.load(f)

    # Useful locations in the graph
    graph_nodes = cred[1]["weightedGraph"][1]["graphJSON"][1]["nodes"]
    graph_node_addresses = cred[1]["weightedGraph"][1]["graphJSON"][1]["sortedNodeAddresses"]
    cred_nodes = cred[1]["credData"]["nodeSummaries"]

    # Printing the CSV
    print(f'id,cred,type,name')
    for [n, graph_node] in enumerate(graph_nodes):
        cred_node = cred_nodes[n]["cred"]
        node_address = graph_node_addresses[graph_node["index"]]
        node_name = extract_node_name(node_address)
        print(f'{str(n)},{cred_node},{str(node_address[2])},{str(node_name)}')


if __name__ == "__main__":
    main(sys.argv[1:])