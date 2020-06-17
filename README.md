# sourcecred-tooling

This repository includes a set of scripts and other tools to play with the graphs created 
by [SourceCred](https://sourcecred.io)

## Converters

* ```convert_cred_to_graph```: Converts CRED graphs (`cred.json` files) into other kind of graphs  using the igraph-python library
* ```convert_credResult_to_graph```: Converts CRED graphs (`credResult.json` files) into other kind of graphs using the  igraph-python library. The format of the input CRED graph must be a JSON file generated by the cli2 command. This
  file follows [the credResult.js type definition](https://github.com/sourcecred/sourcecred/blob/2fd32dd78547a101c33d2c0112962b8b9f2503fb/src/analysis/credResult.js#L30-L42)
* ```convert_outputV2_to_graph```: Converts CRED graphs (`output.json` files) into other kind of graphs using the igraph-python library. This version of the script supports the new output v2 format added by [this commit](https://github.com/sourcecred/sourcecred/commit/b985214fa2754ca61c62133059529e3060de954d)
* ```convert_graph_to_D3JSON```: Convert graphs (formats supported by igraph-python library, i.e., the output of the previous scripts) into a D3-comaptible JSON

## Viewers

* ```view_graph.py```: Shows igraph-supported graph files 
* ```view_graph_D3.html```: HTML page using the JSON output of ```convert_graph_to_D3JSON``` to visualize the graph using D3

## Injecters & Modifiers

* ```inject_weidght_to_graph.py```: Injects a weights definition into a cred graph definition (created by the cli2 graph command)

## CSV helpers

* ```analyze_credResult.py```: Generates a CSV file from credResult graphs. The CSV is printed in STDOUT. Useful for further analysis in other tools
* ```join_csvs.py```:  Given two CSVs generated by ```analyze_credResult.py```, this script joins the CSV data by selecting only users (USERLIKE) rows and joining via their username. The result is printed in STDOUT
* ```digest_csvs.py```: Generates an HTML page (via STDOUT) including tables for the data generated by join_csvs.py script.

## Ad-hoc tests
* ```view_graph_D3_codersVScommenters.html```: HTML page that does the same as ```view_graph_D3.html``` plus changing the color of nodes according to cred values in the node. Please, check the comments at the header file