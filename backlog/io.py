import json
from backlog.model import Backlog, Story


class JSONImporter:

    @staticmethod
    def load(path):
        with open(path) as file:
            raw = json.load(file)
        name = raw.get('case')
        stories = raw.get('stories')
        backlog = Backlog.empty().named_as(name)
        for s in stories:
            story = Story(s['identifier'], s['personas'], s['entities'], s['actions'], s['text'])
            backlog += story
        return backlog


