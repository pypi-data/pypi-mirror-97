import networkx as nx


def create_rule_graph(rules):
    G = nx.DiGraph()

    for node in rules:
        lbl = "score: {:f}\nsize: {}".format(rules[node]["score"], rules[node]["size"])
        G.add_node(node, rule=rules[node]["rule"], label=lbl)

    for node in G.nodes:
        if node[:-2] in G.nodes:
            lbl = node[-1]
            G.add_edge(node[:-2], node, label=lbl)

    return G
