"""
    # Category: Iteration Planning
    # Scenario title: Coverage analysis
    # ECMFA'22 paper: section #IV.C
"""
from collections import defaultdict, Counter
import csv


from matplotlib import pyplot as plt


from scenarios.cases import build_a_case
# todo: update pipfile with libraries


OUTPUT_FILE = 'outputs/3_coverage.pdf'  # Figure XXX
STORY_STATUSES = 'scenarios/data/3_story_status.csv'


def run():
    print("Running Scenario #3")
    g14 = build_a_case('g14')
    g14_enriched = _enrich(g14, STORY_STATUSES)  # Story nodes now have a 'status' attribute to be processed
    # todo: Adapt 'data/plots.py'

    g = g14_enriched.graph

    personas = [n for n in g if g.nodes[n]['label'] == 'persona']
    status = {}


    status_frac = defaultdict(list)
    for p in personas:
        c = Counter(g.nodes[n]['status'] for n in g.neighbors(p) if g.nodes[n]['label'] == 'story')

        for status in ('todo', 'doing', 'done'):
            frac_status = 100*c[status] / sum(c.values())
            status_frac[status].append(frac_status)

    data = list(zip([p[2:] for p in personas], status_frac['todo'], status_frac['doing'], status_frac['done']))
    data = sorted(sorted(sorted(data, key=lambda x:x[1]), key=lambda x:x[2]), key=lambda x:x[3])

    names = [x[0] for x in data]
    todo = [x[1] for x in data]
    doing = [x[2] for x in data]
    done = [x[3] for x in data]


    plt.barh(names, todo, 0.5, label='todo')
    plt.barh(names, doing, 0.5, left=todo, label='doing')
    plt.barh(names, done, 0.5, left=list(sum(x) for x in zip(todo, doing)), label='done')

    plt.legend(ncol=3)
    plt.yticks(rotation=45)
    plt.xlim([0, 110])
    plt.xticks([0, 20, 40, 60, 80, 100])
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)





def _enrich(backlog, extras):
    lines = list(csv.reader(open(extras)))[1:]
    info = dict()
    for line in lines:
        info[f's_{line[0]}_{line[1]}'] = {'status': line[2]}
    return backlog.absorb(info)



