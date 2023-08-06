import os
from graphviz import Digraph
from pyvis.network import Network


class VisualGraph:

    def __init__(self,nodes,edges,is_module=False):
        self.nodes = nodes
        self.edges = edges
        self.digraph = Digraph('G',filename='cluster.gv')
        self.network = Network(heading='XDetection-Module' if is_module else "XDetection-Function",height=900,width=1400,directed=True,notebook=True)
        self.digraph.filename = "XDetection-Function"

        if is_module:
            self.digraph.filename = "XDetection-Module"

    def dot(self,is_created=False):
        for node in self.nodes:
            self.digraph.node(node)
        self.digraph.edges(self.edges)

        self.digraph.format = 'dot'
        if is_created:
            self.digraph.render(cleanup=True)

    def svg(self):
        self.dot()
        self.digraph.format = 'svg'

        self.digraph.render(cleanup=True)

    def jpg(self):
        self.dot()
        self.digraph.format = 'jpg'

        self.digraph.render(cleanup=True)

    def pdf(self):
        self.dot()
        self.digraph.format = 'pdf'

        self.digraph.render(cleanup=True)

    def html(self):
        """
        :return:
        """

        self.network.show_buttons(filter_=['physics'])
        self.network.add_nodes(self.nodes)
        self.network.add_edges(self.edges)

        self.network.show('{0}.html'.format(self.digraph.filename))

