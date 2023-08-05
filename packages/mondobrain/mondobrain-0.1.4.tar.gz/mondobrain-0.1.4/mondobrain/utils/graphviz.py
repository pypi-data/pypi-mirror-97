from IPython.display import Image
import networkx as nx
import pygraphviz as pgv

from mondobrain.utils.graph import create_rule_graph


def visualize_rule_graph(G):
    nx.nx_agraph.write_dot(G, "rules.dot")
    G = pgv.AGraph("rules.dot", directed=True)

    G.node_attr["shape"] = "box"
    G.edge_attr["color"] = "red"

    G.layout("dot")
    G.draw("graph.png")

    return Image(filename="graph.png")


def visualize_rule_tree(rule_tree):
    return visualize_rule_graph(create_rule_graph(rule_tree))
