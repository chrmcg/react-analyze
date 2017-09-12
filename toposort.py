# Credit where credit is due:
# https://en.wikipedia.org/w/index.php?title=Topological_sorting&oldid=799070350#Depth-first_search

def toposort(dict_of_edges):
    nodes = [{
        'name': name,
        'edges': edges,
        'visited': False,
        'done': False,
    } for (name, edges) in dict_of_edges.iteritems()]

    get_node = lambda name: next((node for node in nodes if node['name'] == name), None)

    # We put the least relevant nodes
    #   (i.e. those which have the fewest edges to other nodes in our dict)
    # first in the input array.
    #
    # This causes them to end up at the end of the topologically sorted array,
    # instead of annoyingly scattered throughout.
    relevance_scores = [{
        'name': node['name'],
        'score': sum([(edge_name in dict_of_edges) for edge_name in node['edges']])
    } for node in nodes]

    node_names_by_relevance_ascending = [s['name'] for s in sorted(relevance_scores, key=lambda s: s['score'])]

    get_next_unmarked_node_name = lambda: next((
        name for name in node_names_by_relevance_ascending if
            (not get_node(name)['visited'] and
            not get_node(name)['done'])
    ), None)

    sorted_node_names = []

    def visit(node_name):
        node = get_node(node_name)
        if node is None:
            return
        if node['done']:
            return
        if node['visited']:
            # TODO somehow remove edges based on relevance scores to create a close-enough DAG
            raise Exception('Component dependency graph is not a DAG: at ' + node_name)

        node['visited'] = True

        for edge_name in node['edges']:
            visit(edge_name)

        node['done'] = True

        sorted_node_names.insert(0, node_name)

    while get_next_unmarked_node_name() is not None:
        visit(get_next_unmarked_node_name())

    return sorted_node_names

