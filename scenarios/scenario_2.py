"""
    # Category: Product analysis
    # Scenario title: Elements' weight
    # ECMFA'22 paper: section #IV.B
"""
from collections import defaultdict, Counter

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



from scenarios.cases import build_cases
# todo: update pipfile with libraries



OUTPUT_FILE = 'outputs/2_actors.pdf'  # Figure XXX


def run():
    print("Running Scenario #2")
    cases = build_cases()

    df = []
    for k, v in cases.items():
        g = v.graph
        personas_n = [n for n, data in g.nodes(data=True) if data['label'] == 'persona']
        weights = []
        for p in personas_n:
            weights.append(sum(1 for n in g.neighbors(p) if g.nodes[n]['label'] == 'story'))
        tot = sum(weights)
        df.extend([(k, w/tot) for w in weights])

    df = pd.DataFrame(df, columns=['Case', 'Personas weights'])

    means = []
    for x in df['Case'].unique():
        means.append((x, df[df['Case']==x]['Personas weights'].mean()))

    order = [x[0] for x in sorted(means, key=lambda x:x[1])]

    sns.boxplot(data=df, x='Case', y='Personas weights', order=order)
    sns.swarmplot(data=df, x='Case', y='Personas weights', order=order, color=".25")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)






