"""

A -1- B -3- C
      |     |
      9     2
      |     |
      D -3- E

"""

G = {
    'A': {'B': 1},
    'B': {
        'A': 1,
        'C': 3,
        'D': 9
    },
    'C': {
        'B': 3,
        'E': 2
    },
    'D': {
        'B': 9,
        'E': 3
    },
    'E': {
        'C': 2,
        'D': 3
    }
}

def largeur_simple(G, s):
    # G = { s : [adja(s)], ...}
    dict(zip(set(G), [ set(v) for v in G.values() ]))

    done = [s]
    file = [s]

    while file != []:
        s = file.pop(0)
        for node in G[s]:
            if node not in done:
                file.append(node)
                done.append(node)
    return done

def largeur(G, src, dst):
    """
    O(s + a)
    """
    # init à infini
    from math import inf
    # { A: inf, B: inf, ...}
    pcc = dict(zip(set(G), [inf] * len(set(G))))

    file = [(src, 0)]
    done = []
    preds = {}

    while file != []:
        s, dist = file.pop(0)
        done.append(s)
        for node, dist_s in G[s].items(): # dico de dico
            if node not in done:
                if pcc[node] > dist + dist_s:
                    pcc[node] = dist + dist_s
                    preds[node] = s
                file.append((node, dist + dist_s))

    # construction du return
    ret = [dst]
    pred = dst
    while src not in ret:
        pred = preds[pred]
        ret.append(pred)
    ret.reverse()
    return ret, pcc[dst]


def dijkstra(G, src, dst):
    """
    O((a + s) log s)
    """
    # init à infini
    from math import inf
    # { A: inf, B: inf, ...}
    pcc = dict(zip(set(G), [inf] * len(set(G))))

    file = [(src, 0)]
    done = []
    preds = {}

    while file != []:
        file.sort(key = lambda x: x[1]) # sort by dist
        s, dist = file.pop(0)
        done.append(s)
        for node, dist_s in G[s].items():
            if node not in done:
                if pcc[node] > dist + dist_s:
                    pcc[node] = dist + dist_s
                    preds[node] = s
                file.append((node, dist + dist_s))

    # construction du return
    ret = [dst]
    pred = dst
    while src not in ret:
        pred = preds[pred]
        ret.append(pred)
    ret.reverse()
    return ret, pcc[dst]

print(largeur_simple(G, 'A'))
print(largeur(G, 'A', 'E'))
print(dijkstra(G, 'A', 'E'))