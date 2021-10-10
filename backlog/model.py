import networkx as nx
from networkx.algorithms.operators.binary import compose


class Story:
    """A story is modelled as an action performed on entities to bring values to personas"""
    def __init__(self, identifier, personas, entities, actions, text):
        self.__identifier = identifier
        self.__personas = personas
        self.__entities = entities
        self.__actions = actions
        self.__text = text

    @property
    def identifier(self):
        return self.__identifier

    @property
    def actions(self):
        return self.__actions

    @property
    def personas(self):
        return self.__personas

    @property
    def entities(self):
        return self.__entities

    @property
    def text(self):
        return self.__text

    def __invert__(self):  # ~ formal operator
        """Story promotion to transform a story into a backlog"""
        return Backlog.build(self)


class Backlog:
    """Backlog representation"""

    """ ##############
        # Public API #
        ############## """

    @classmethod
    def empty(cls):
        return cls()

    def __iadd__(self, other):  # <- formal operator
        """Increment a backlog by adding a new story"""
        return self + ~other

    def __add__(self, other):  # oplus formal operator
        """Merge two backlogs together"""
        result = Backlog.empty()
        result.__name = self.__merge_names(self.__name, other.__name)
        result.__graph = compose(self.__graph, other.__graph)
        return result

    def __str__(self):
        return nx.nx_pydot.to_pydot(self.__graph).__str__()

    def named_as(self, name):
        self.__name = name
        return self

    @property
    def graph(self):
        return self.__graph.copy(as_view=True)

    @property
    def personas(self):
        nodes = [data['text'] for n, data in self.graph.nodes(data=True) if data['label'] == 'persona']
        return nodes

    @property
    def entities(self):
        nodes = [data['text'] for n, data in self.graph.nodes(data=True) if data['label'] == 'entity']
        return nodes

    @property
    def stories(self):
        nodes = [n for n, data in self.graph.nodes(data=True) if data['label'] == 'story']
        result = list()
        for n in nodes:
            p_ids = [p_id for p_id, attrs in self.graph.adj[n].items() if attrs['label'] == 'has_for_persona']
            personas = [self.graph.nodes[p]['text'] for p in p_ids]
            actions = self.graph.nodes[n]['actions']
            e_ids = [e_id for e_id, attrs in self.graph.adj[n].items() if attrs['label'] == 'has_for_entity']
            entities = [self.graph.nodes[e]['text'] for e in e_ids]
            text = self.graph.nodes[n]['text']
            result.append(Story(n, personas, entities, actions, text))
        return result

    def absorb(self, extra):
        result = Backlog.empty()
        result.__name = self.__name
        g = self.__graph.copy()
        nx.set_node_attributes(g, extra)
        result.__graph = g
        return result

    """ #######################################
        # Private API (use at your own risks) #
        ####################################### """

    @classmethod
    def build(cls, story):
        """Create a backlog based on a story (internal factory)"""
        result = cls.empty()
        # Load entities, personas and action as nodes
        p_nodes = map(lambda x: result._add_persona(x), story.personas)
        e_nodes = map(lambda x: result._add_entity(x), story.entities)
        s_node = result._add_story(story.identifier, story.actions, story.text)
        # Link elements together
        for p in p_nodes:
            result.__graph.add_edge(s_node, p, label='has_for_persona')
        for e in e_nodes:
            result.__graph.add_edge(s_node, e, label='has_for_entity')
        return result

    def __init__(self):
        """Private constructor, initialize the underlying graph"""
        self.__graph = nx.Graph()
        self.__name = None

    def _add_persona(self, persona):
        identifier = f"p_{persona}"
        self.__graph.add_node(identifier, label='persona', text=persona)
        return identifier

    def _add_entity(self, entity):
        identifier = f"e_{entity}"
        self.__graph.add_node(identifier, label='entity', text=entity)
        return identifier

    def _add_story(self, identifier, actions, text):
        s_id = f"s_{identifier}"
        self.__graph.add_node(s_id, label='story', text=text, actions=actions)
        return s_id

    @staticmethod
    def __merge_names(this, that):
        if this and that and this != that:
            raise ValueError(f"{this} != {that}")
        else:
            return this or that
