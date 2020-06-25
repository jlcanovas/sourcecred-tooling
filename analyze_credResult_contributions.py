#!/usr/bin/python
#
# Generates a CSV file from credResult graphs. The CSV is printed in STDOUT. Useful for further analysis in other tools
#
# The CSV file follows this format (example):
#    user,authors_commits,authors_comments,authors_issues,...
#    jlcanovas,12,55,2,...
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
USAGE = 'analyze_credResult_contributions.py -g GRAPH_JSON_FILE'


def count_contribution(node_user, cred_edge):
    action = cred_edge[2]
    if action == "AUTHORS":
        node = node_user["authors"]
        type = cred_edge[12]
        subtype = cred_edge[13]
    elif action == "REACTS":
        node = node_user["reacts"]
        type = cred_edge[13]
        subtype = cred_edge[3]  # Not used yet
    elif action == "REFERENCES":
        node = node_user["isReferenced"]
        type = cred_edge[6]
        subtype = cred_edge[7]

    if type == "COMMENT":
        node[type+"_"+subtype] = node.get(type+"_"+subtype, 0) + 1
    node[type] = node.get(type, 0) + 1


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

    with open(input_graph, encoding="utf8") as f:
        cred = json.load(f)

    # Useful locations in the graph3
    graph = cred[1]['weightedGraph'][1]['graphJSON'][1]
    cred_node_addresses = graph['sortedNodeAddresses']

    useridx_to_username = {}
    users = {}
    for cred_node in graph['nodes']:
        cred_node_address = cred_node_addresses[cred_node['index']]
        # We focus only on USERLIKE
        if cred_node_address[2] == "USERLIKE":
            username = cred_node_address[4]
            users[username] = {"authors": {}, "isReferenced": {}, "reacts": {}}
            useridx_to_username[cred_node['index']] = username

    for cred_edge in graph['edges']:
        if cred_edge['srcIndex'] in useridx_to_username:
            node = users[useridx_to_username[cred_edge['srcIndex']]]
            count_contribution(node, cred_edge['address'])

        if cred_edge['dstIndex'] in useridx_to_username:
            node = users[useridx_to_username[cred_edge['dstIndex']]]
            count_contribution(node, cred_edge['address'])

    print(f'user,authors_commits,authors_issues,authors_pulls,authors_comments,isReferenced_issues,isReferenced_pulls,isReferenced_comments,reacts_issue,reacts_pull,reacts_comments')
    for key in users:
        data = users[key]
        data_authors = data["authors"]
        data_isReferenced = data["isReferenced"]
        data_reacts = data["reacts"]
        print(f'{key},{data_authors.get("COMMIT", 0)},{data_authors.get("ISSUE", 0)},{data_authors.get("PULL", 0)},{data_authors.get("COMMENT", 0)},'
              f'{data_isReferenced.get("ISSUE", 0)},{data_isReferenced.get("PULL", 0)},{data_isReferenced.get("COMMENT", 0)},'
              f'{data_reacts.get("ISSUE", 0)},{data_reacts.get("PULL", 0)},{data_reacts.get("COMMENT", 0)}')


if __name__ == "__main__":
    main(sys.argv[1:])