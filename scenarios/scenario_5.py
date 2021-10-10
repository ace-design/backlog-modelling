"""
    # Category: Product analysis
    # Scenario title: elements' weight
    # ECMFA'22 paper: section #IV.B
"""
from itertools import product, combinations
from multiprocessing import Pool
import pickle
from statistics import mean


import matplotlib.pyplot as plt
from numpy import isnan
import pandas as pd
import seaborn as sns
from tqdm import tqdm
import spacy


from scenarios.cases import all_cases

OUTPUT_FILE = 'outputs/5_similarities.pdf'


CASES = all_cases()



def _compare_all_products_spacy(case12):
    case1, case2 = case12

    nlp = spacy.load("en_core_web_lg")  # make sure to use larger package!

    graph = CASES.graph


    groups = [{}, {}]
    for g, c in zip(groups, (case1, case2)):
        c = [(n, data) for n, data in graph.nodes(data=True)
             if n.split('_')[1] == c]

        for n, data in c:

            personas = []
            entities = []
            for n1 in graph.neighbors(n):
                data1 = graph.nodes(data=True)[n1]
                if data1['label'] == 'persona':
                    personas.append(data1['text'])
                elif data1['label'] == 'entity':
                    entities.append(data1['text'])

            for p, e in product(personas, entities):
                g[p, e] = data['actions']

    results = []
    for (g1, c1), (g2, c2) in product(groups[0].items(), groups[1].items()):
        a1, e1 = g1
        a2, e2 = g2

        _c1, _c2 = c1, c2
        tot = 0
        if len(c1) < len(c2):
            c1, c2, = c2, c1

        cost_contr = 0
        for c11 in c1:
            doc1 = nlp(c11)
            cost_contr += min(doc1.similarity(nlp(c21)) for c21 in c2)
        cost_contr /= len(c1)
        cost_act = nlp(a1).similarity(nlp(a2))
        cost_ent = nlp(e1).similarity(nlp(e2))
        tot = cost_contr + cost_act + cost_ent
        results.append(((g1, _c1), (g2, _c2), (cost_act, cost_ent, cost_contr), tot))

    results = [x for x in results if not isnan(x[-1])]

    return case1, case2, [x[-1] for x in results]

def compare_all_products_spacy():

    g = CASES.graph
    cases_ids = set(n.split('_')[1] for n, data in g.nodes(data=True)
                    if data['label'] == 'story')

    results = []
    cases_ids = list(combinations(cases_ids, 2))
    with Pool(35) as pool:
        for r in tqdm(pool.imap_unordered(_compare_all_products_spacy, cases_ids), total=len(cases_ids)):
            results.append(r)
    return results

def run():
    print("Running Scenario #5")

    data = compare_all_products_spacy()

    with open('tmp.pickle', 'wb') as f:
        pickle.dump(data, f)

    df = [(f"{x}_{y}", z) for x, y, d in data for z in d]
    label = 'Similarity'
    df = pd.DataFrame(df, columns=["Class", "Similarity"])
    sns.kdeplot(data=df, x='Similarity', hue='Class', alpha=0.5, linewidth=0.4, legend=False)

    means = [mean(x[2]) for x in data]
    sns.rugplot(means, height=-0.02, clip_on=False)

    plt.savefig(OUTPUT_FILE)


