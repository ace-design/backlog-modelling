from backlog.io import JSONImporter
from backlog.model import Backlog

PATH_PREFIX = 'dataset/cases'


def build_a_case(name, path=PATH_PREFIX):
    """load a given case"""
    return JSONImporter.load(f"{path}/{name}.json")


def build_cases(path=PATH_PREFIX):
    """load all known cases, as a key-value dictionary"""
    tmp = dict()
    cases = ['g02', 'g03', 'g04', 'g05', 'g08',
             'g10', 'g11', 'g12', 'g13', 'g14', 'g16', 'g17', 'g18', 'g19',
             'g21', 'g22', 'g23', 'g24', 'g25', 'g26', 'g27', 'g28']
    for c in cases:
        tmp[c] = build_a_case(c, path)
    return tmp


def all_cases(path=PATH_PREFIX):
    """Merge all cases together into a common backlog"""
    backlog = Backlog.empty().named_as("all")
    for n, b in build_cases(path).items():
        backlog = backlog + b.named_as("all")
    return backlog




