"""
    # Category: Product analysis
    # Scenario title: Graph structure
    # ECMFA'22 paper: section #IV.A
"""
from scenarios.cases import build_cases
# todo: update pipfile with libraries


from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


OUTPUT_FILE = 'outputs/1_moustache.pdf'  # Figure 7


def run():
    print("Running Scenario #1")
    cases = build_cases()
    data = []
    for k, v in cases.items():
        g = v.graph
        nb_persona = sum(1 for n in g.nodes(data=True) if n[1]['label'] == 'persona')
        nb_story = sum(1 for n in g.nodes(data=True) if n[1]['label'] == 'story')
        nb_entity = sum(1 for n in g.nodes(data=True) if n[1]['label'] == 'entity')
        nb_action = sum(len(n[1]['actions']) for n in g.nodes(data=True) if n[1]['label'] == 'story')
        nb_edge = len(g.edges())
        data.append((nb_persona, 'Nb personas'))
        data.append((nb_story, 'Nb user stories'))
        data.append((nb_entity, 'Nb entities'))
        data.append((nb_action, 'Nb actions'))
        data.append((nb_edge, 'Nb edges'))

    df = pd.DataFrame(data, columns=['count', 'parameter'])
    sns.boxplot(data=df, x='parameter', y='count')
    plt.savefig(OUTPUT_FILE)
