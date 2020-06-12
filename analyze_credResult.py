#!/usr/bin/python
##
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
USAGE = 'analyze_credResult.py -g GRAPH_JSON_FILE'


def extract_node_name(node):
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

    with open(input_graph, encoding="utf8") as f:
        cred = json.load(f)

    #print(f'Cred data for {len(cred[1]["credData"]["nodeSummaries"])} nodes and {len(cred[1]["credData"]["edgeSummaries"])} edges')
    #print(f'Graph has {len(cred[1]["weightedGraph"][1]["graphJSON"][1]["nodes"])} nodes, {len(cred[1]["weightedGraph"][1]["graphJSON"][1]["edges"])} edges and {len(cred[1]["weightedGraph"][1]["graphJSON"][1]["sortedNodeAddresses"])} node addresses')

    graph_nodes = cred[1]["weightedGraph"][1]["graphJSON"][1]["nodes"]
    graph_node_addresses = cred[1]["weightedGraph"][1]["graphJSON"][1]["sortedNodeAddresses"]
    cred_nodes = cred[1]["credData"]["nodeSummaries"]

    print(f'id,cred,type,name')
    for [n, graph_node] in enumerate(graph_nodes):
        cred_node = cred_nodes[n]["cred"]
        node_address = graph_node_addresses[graph_node["index"]]
        node_name = extract_node_name(node_address)
        print(f'{str(n)},{cred_node},{str(node_address[2])},{str(node_name)}')


if __name__ == "__main__":
    main(sys.argv[1:])