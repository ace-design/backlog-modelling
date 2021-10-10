"""
    # Category: Iteration Planning
    # Scenario title: Story Recommendation
    # ECMFA'22 paper: section #IV.D
"""
from collections import defaultdict
from itertools import combinations, product
from multiprocessing import Pool


import networkx as nx
from networkx.algorithms.similarity import graph_edit_distance
from networkx.algorithms.community import greedy_modularity_communities, asyn_fluidc
from numpy import arange, linspace
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, is_valid_linkage, fcluster
from scipy.cluster.vq import whiten, kmeans2


from scenarios.cases import build_a_case
# todo: update pipfile with libraries


OUTPUT_FILES = {
    'g13': 'outputs/4_clustering_g13.pdf',
    'g24': 'outputs/4_clustering_g24.pdf',
}
GROUND_TRUTH = {
    'g13': 'scenarios/data/4_g13_ground_truth.txt',
    'g24': 'scenarios/data/4_g24_ground_truth.txt'
}


def get_true_clusters(path):
    d = defaultdict(list)
    with open(path) as f:
        c = 0
        for line in f:
            line = line.strip()
            if not line:
                c += 1
                continue
            d[c].append(line[1:-1])
    return d



def graph_distance(g1, g2):

    def node_subst_cost(n1, n2):
        #If not same label, max cost

        try:
            if n1['label'] != n2['label']:
                return 1
        except KeyError:
            return 1

        if n1['label'] in ('persona', 'entity'):
            if n1['text'] == n2['text']:
                return -1
            else:
                return 0.5 #Small penalty
        else:#Must be story, penalty fraction of matching actions, up to 0.99
            c1 = set(n1['actions'])
            c2 = set(n2['actions'])

            return  0.25 * len(c1 ^ c2) / len(c1 | c2)

    return graph_edit_distance(g1, g2, node_subst_cost=node_subst_cost)


def get_clusters(case, dist, labels, t):
    Z = linkage(dist, method='average') #same length to root
    threshold = t*(max(Z[:,2]))
    assert(is_valid_linkage(Z))
    dendro = dendrogram(Z, color_threshold=threshold, labels=labels, no_plot=True)
    clusters = fcluster(Z, t=threshold, criterion='distance')

    map_label_cluster = {l:c for c, l in zip(clusters, labels)}


    """
    for lab, col in zip(dendro['ivl'], dendro['leaves_color_list']):
        #'C0' is default above threshold
        if col == 'C0':
            map_label_cluster.pop(lab)
    """
    return map_label_cluster

def analyze_dendro(case, dist, labels, true_clusters):

    xx = []
    y = []
    for t in arange(0, 1, 0.001):
        d_clusters = get_clusters(case, dist, labels, t)


        TP = 0
        for c in true_clusters.values():
            try:
                val = d_clusters[c[0]]
            except KeyError:
                #Not in any cluster! no need to check
                continue
            if all((d_clusters.get(l, 'a') == val) for l in c):
                TP += 1
        frac_TP = TP / len(true_clusters)
        if not len(set(d_clusters.values())):
            nb_clusters = 0
        else:
            nb_clusters = len(set(d_clusters.values()))
        xx.append(f'{nb_clusters / len(true_clusters):.1}')
        y.append(frac_TP)
    x = list(range(len(xx)))

    nb_leafs = sum(len(c) for c in true_clusters.values())
    y.append(1)

    plt.plot(linspace(0, nb_leafs - 1, len(y)), y, label='dendro')


def analyze_kmeans(case, graphs, labels, true_clusters):
    data = []
    for i, g in enumerate(graphs):
        nb_personas = 0
        nb_entities = 0
        nb_actions = 0
        print(len(g.nodes()))
        for n, d in g.nodes(data=True):
            print(n, d)
            if d['label'] == 'persona':
                nb_personas += 1
            elif d['label'] == 'entity':
                nb_entities += 1
            else:
                nb_actions = len(d['actions'])
        data.append([nb_personas, nb_entities, nb_actions])
    data = whiten(data)

    xx = []
    y =  []
    for i in range(len(graphs), 0, -1):
        _, clusts = kmeans2(data, i, minit='points')
        d_clusters = {l:c for l, c in zip(labels, clusts)}


        TP = 0
        for c in true_clusters.values():
            try:
                val = d_clusters[c[0]]
            except KeyError:
                #Not in any cluster! no need to check
                continue
            if all((d_clusters.get(l, 'a') == val) for l in c):
                TP += 1
        frac_TP = TP / len(true_clusters)
        xx.append(f'{i / len(true_clusters):.1}')
        y.append(frac_TP)
    x = list(range(len(xx)))
    plt.plot(x, y, label='k-means 3D')



    #K mean sur struct (nb_acteur / nb_entites / nb_actions)
    #K means sur long vect (tous acteurs / tous entites / nb_actions)


def analyze_kmeans_long(case, graphs, labels, true_clusters):
    personas = list(sorted(set(n for g in graphs for n, d in g.nodes(data=True) if d['label'] == 'persona')))
    entities = list(sorted(set(n for g in graphs for n, d in g.nodes(data=True) if d['label'] == 'entity')))

    l = len(personas) + len(entities) + 1
    data = []
    for i, g in enumerate(graphs):
        data.append([0] * l)
        for n, d in g.nodes(data=True):
            if d['label'] == 'persona':
                data[-1][personas.index(n)] += 1
            elif d['label'] == 'entity':
                data[-1][entities.index(n) + len(personas)] += 1
            else:
                data[-1][-1] = len(d['actions'])
    data = whiten(data)

    xx = []
    y =  []
    for i in range(len(graphs), 0, -1):
        _, clusts = kmeans2(data, i, minit='points')
        d_clusters = {l:c for l, c in zip(labels, clusts)}


        TP = 0
        for c in true_clusters.values():
            try:
                val = d_clusters[c[0]]
            except KeyError:
                #Not in any cluster! no need to check
                continue
            if all((d_clusters.get(l, 'a') == val) for l in c):
                TP += 1
        frac_TP = TP / len(true_clusters)
        xx.append(f'{i / len(true_clusters):.1}')
        y.append(frac_TP)
    x = list(range(len(xx)))
    plt.plot(x, y, label=f'K-means {len(data[0])}D')



def analyze_communities_fluids(case, graphs, labels, true_clusters):

    g = graphs[0].copy()
    for g2 in graphs[1:]:
        g = nx.compose(g, g2.copy())
    g.add_node('Projet', label='projet')
    for n, d in g.nodes(data=True):
        if d['label'] == 'story':
            g.add_edge(n, 'Projet')

    xx = []
    y =  []
    # We check for different level of communities (i)
    for i in range(len(graphs), 0, -1):
        d_clusters = {}
        #Make "i" communities
        clusts = list(asyn_fluidc(g, i))
        for i, c in enumerate(clusts):
            for l in c:
                if g.nodes()[l]['label'] == 'story':
                    d_clusters[g.nodes()[l]['text']] = i

        TP = 0
        for c in true_clusters.values():
            try:
                val = d_clusters[c[0]]
            except KeyError:
                #Not in any cluster! no need to check
                continue
            if all((d_clusters.get(l, 'a') == val) for l in c):
                TP += 1
        frac_TP = TP / len(true_clusters)
        xx.append(f'{i / len(true_clusters):.1}')
        y.append(frac_TP)
    x = list(range(len(xx)))
    print(y)
    plt.xticks([x[0], x[-1]], [f'0|{len(graphs)}', '1|1'])
    plt.plot(x, y, label='fluid')
    plt.xticks([], [])

def analyze_case(scenario, case, truth, output):
    g = case.graph
    stories = [s.identifier for s in case.stories]
    stories_text = [s.text for s in case.stories]
    subgraphs = [g.subgraph([s] + list(g.neighbors(s))) for s in stories]

    graph_distance(subgraphs[0], subgraphs[2])

    with Pool(6) as pool:
        costs = pool.starmap(graph_distance, combinations(subgraphs, 2))
        m_c = min(costs)
        if m_c < 0:
            distances = [x - m_c for x in costs]

    true_clusters = get_true_clusters(truth)
    analyze_dendro(case, distances, stories_text, true_clusters)
    analyze_kmeans(case, subgraphs, stories_text,  true_clusters)
    analyze_kmeans_long(case, subgraphs, stories_text,  true_clusters)
    analyze_communities_fluids(case, subgraphs, stories_text,  true_clusters)

    plt.legend()
    plt.title(f"Scenario {scenario}")
    plt.ylabel("Fraction of curated story clusters in the same automatic cluster")
    plt.xlabel("Threshold (dendrogram) | number of target communities (others)")
    plt.ylim([0.5, 1])
    plt.savefig(output)
    plt.clf()



def run():
    print("Running Scenario #4")
    g13 = build_a_case('g13')
    g24 = build_a_case('g24')

    analyze_case('g13', g13, GROUND_TRUTH['g13'], OUTPUT_FILES['g13'])
    analyze_case('g24', g24, GROUND_TRUTH['g24'], OUTPUT_FILES['g24'])




