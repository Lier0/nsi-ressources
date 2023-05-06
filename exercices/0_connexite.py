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

G_non_connexe = {
    'A': {'A': 1},
    'B': {'B': 1}
}

def largeur(G, src, dst):
    # init à infini
    from math import inf
    pcc = dict(zip(set(G), [inf] * len(set(G))))

    file = [(src, 0)]
    done = []
    preds = {}

    while file != []:
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
    if dst not in preds: return None # break si non connexe
    while src not in ret:
        pred = preds[pred]
        ret.append(pred)
    ret.reverse()
    return ret, pcc[dst]


def est_connexe(G): # fortement
    done = []
    for src in G.keys():
        for dst in G.keys():
            if src != dst and largeur(G, src, dst) == None:
                return False
    return True

print(largeur(G, 'A', 'E'))
print(est_connexe(G))