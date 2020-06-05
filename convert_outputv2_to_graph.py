#!/usr/bin/python
#
# Simple script to convert CRED graphs into other kind of graphs using the igraph-python library
#
# NOTE: This version of the script supports the new output v2 format added by this commit:
# https://github.com/sourcecred/sourcecred/commit/b985214fa2754ca61c62133059529e3060de954d
#
# The conversion traverses the output.json file generated by SourceCred and extract node and edges information.
# Placeholders for cred calculations are added as comments.
#
# Note that CRED graphs support dangling edges (i.e., edges with no source/target nodes). Dangling edges are not
# included in the resulting converted graph (a message notifies the number of dangling edges found)
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
-i   - The path of the CRED graph (output.json file)
-o   - The path for the generated graph
-f   - Format of the generated graph (gml, graphml, dot, svg...)
"""
USAGE = 'convert_outputV2_to_graph.py -i CRED_GRAPH_PATH -o OUTPUT_GRAPH -f OUTPUT_GRAPH_FORMAT'


def convert_graph(input_graph_path):
    """Converts a CRED-like graph into a graph format supported by the igraph library
    :param input_graph_path: The path to the CRED graph to convert
    """

    with open(input_graph_path, encoding="utf8") as f:
        graph = json.load(f)

    g = Graph(directed=True)
    idx = 0  # As nodes are ordered, we keep track of index

    # Collecting nodes
    for cred_node in graph[1]['orderedNodes']:
        igraph_node_atts = {'label': cred_node['address'][2]+'-'+cred_node['address'][-1][:7],
                            'type': cred_node['address'][2],
                            'timestamp': cred_node['timestamp'] if cred_node['timestamp'] is not None else 0,
                            'totalCred': cred_node['totalCred']['cred'],
                            'index': idx,
                            #'credOverTime': cred_node['credOverTime'] # To play with cred
                            }
        g.add_vertex(name=str(idx), **igraph_node_atts)
        idx += 1

    # Collecting edges
    # Note that CRED graphs support dangling edges (i.e., edges with no source/target nodes)
    dangling_edges = []
    for cred_edge in graph[1]['orderedEdges']:
        igraph_edge_atts = {'address': '-'.join(cred_edge['address']),
                            'timestamp': cred_edge['timestamp'],
                            'backwardsWeight': cred_edge['rawWeight']['backwards'], 
                            'forwardsWeight': cred_edge['rawWeight']['forwards'],
                            'backwardFlow': cred_edge['totalCred']['backwardFlow'],
                            'forwardFlow': cred_edge['totalCred']['forwardFlow'],  
                            #'credOverTime': cred_edge['credOverTime'] # To play with cred
                            }
        try:
            g.add_edge(str(cred_edge['srcIndex']), str(cred_edge['dstIndex']), **igraph_edge_atts)
        except ValueError as ve:
            dangling_edges.append({"srcIndex": cred_edge['srcIndex'], "dstIndex": cred_edge['dstIndex']})

    # Reporting the number of dangling edges found
    print(f"Dangling edges found: {len(dangling_edges)}")

    return g


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
        opts, args = getopt.getopt(argv, "hi:o:f:", [])
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
        elif opt in ('-f'):
            output_format = arg

    g = convert_graph(input_graph_path)

    if output_format != "json":
        Graph.save(g, output_path, format=output_format)
    elif output_format == "json":
        json_g = convert_to_JSON(g)
        with open(output_path, 'w') as f:
            json.dump(json_g, f)


if __name__ == "__main__":
    main(sys.argv[1:])