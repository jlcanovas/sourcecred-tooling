#!/usr/bin/python
#
# This script converts CRED graphs into other kind of graphs using the igraph-python library. The format of the input
# CRED graph must follow the credResult.js type definition:
# https://github.com/sourcecred/sourcecred/blob/2fd32dd78547a101c33d2c0112962b8b9f2503fb/src/analysis/credResult.js#L30-L42
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
"""
USAGE = ''


def convert_graph(input_path):
    """
    :param input_path:
    """

    with open(input_path, encoding="utf8") as f:
        cred_file = json.load(f)

    cred_data = cred_file[1]['credData']
    graph = cred_file[1]['weightedGraph'][1]['graphJSON'][1]

    print(f'Found cred summary data for {len(cred_data["nodeSummaries"])} nodes and {len(cred_data["edgeSummaries"])} edges')
    print(f'Found cred overtime data for {len(cred_data["nodeOverTime"])} nodes and {len(cred_data["edgeOverTime"])} edges')
    print(f'The graph has {len(graph["nodes"])} nodes, {len(graph["edges"])} edges and {len(graph["sortedNodeAddresses"])} node addresses')

def main(argv):
    if len(argv) == 0:
        sys.exit(0)

    try:
        opts, args = getopt.getopt(argv, "hi:", [])
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(USAGE)
            sys.exit()
        elif opt in ('-i'):
            input_path = arg

    convert_graph(input_path)


if __name__ == "__main__":
    main(sys.argv[1:])
