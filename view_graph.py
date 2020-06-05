#!/usr/bin/python
#
# Simple script to show igraph-supported graph files
#
# Author: Javier Canovas (me@jlcanovas.es)
#

import getopt
import sys

from igraph import Graph, plot


"""
Usage of this script
Main options:
-i   - The path of the igraph file (gml, graphml, etc...)
"""
USAGE = 'graph_viewer.py -i GRAPH_PATH'


def show_graph(input_graph_path):
    """
    Shows a graph using the PyCairo library. Some default viewing options are currently applied
    TODO: Support the configuration of viewing options
    :param input_graph_path: The path to the graph to show
    """

    g = Graph.Load(input_graph_path)

    node_colors = {"COMMIT": "black", "COMMENT": "pink", "ISSUE": "orange", "USERLIKE": "red", "PULL": "blue",
                   "REPO": "pink"}

    commit_nodes = [node.index for node in g.vs if node['type'] == 'COMMIT']
    g.delete_vertices(commit_nodes)

    graph_style = {"vertex_size": 20,
                   "vertex_color": [node_colors[node_type] for node_type in g.vs["type"]],
                   "vertex_label": g.vs["label"],
                   "edge_width": [1 * edge_flow for edge_flow in g.es['forwardFlow']],
                   "layout": g.layout("fr"),
                   "bbox": (1000, 1000),
                   "margin": 100}

    plot(g, **graph_style)


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
        elif opt in '-i':
            input_graph_path = arg

    show_graph(input_graph_path)


if __name__ == "__main__":
    main(sys.argv[1:])
