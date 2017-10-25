# Depth first search
# Skeleton for traversing graphs


def dfs(G):

    for v in V(G):
        v.visited = False

    for v in V(G):
        if not v.visited:
            dfs_visit(v)


def dfs_visit(v):
    v.visited = True

    for u in neighbors(v):
        if not u.visited:
            dfs_visit(u)


# With little extra work we turn the DFS into a topological sort

def topological_sort(G):

    results = []

    for v in V(G):
        v.visited = False

    for v in V(G):
        if not v.visited:
            topo_visit(v, results)

    # Return the final ordering
    return results


def topo_visit(v, results):

    v.visited = True

    for u in neighbors(v):
        if not u.visited:
            topo_visit(u, results)
        results.prepend(v)


def dfs2(G):

    """Adaption of the DFS algorithm to return connected components"""

    for v in V(G):
        v.visited = False

    result = []

    for v in V(G):
        if not v.visited:
            X = dfs2_visit(v)
            result.append(X)

    return result


def dfs2_visit(v):

    v.visited = True
    S = [v]

    for u in neighbors(v):
        if not u.visited:
            R = dfs2_visit(u)
            S.extend(R)

    return S

