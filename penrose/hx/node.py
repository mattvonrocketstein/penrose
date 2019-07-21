""" penrose.hx.node:
        node wrapper for houdini
"""

from penrose import (
    # abcs,
    util,)

import uuid
import hou

LOGGER = util.get_logger(__name__)

from penrose.hx.abcs import HWrapper, HTree

def uniq(): return str(uuid.uuid1())
class Translator(object):

    def right(self, unit):
        self.node.setParmTransform(
            hou.hmath.buildTranslate(
                unit, 0, 0))

    def left(self, unit):
        return self.right(-unit)

    def up(self, unit):
        self.node.setParmTransform(
            hou.hmath.buildTranslate(
                0, unit, 0))

    def down(self, unit):
        return self.up(-unit)

    def inwards(self, unit):
        self.node.setParmTransform(
            hou.hmath.buildTranslate(
                0, 0, unit))
    def outwards(self, unit):
        return self.inwards(-unit)

        #     #         base['x'] + (i*offset),
        #     #         base['y'] + offset*y,
        #     #         base['z']))

class Node(HWrapper, Translator):
    @staticmethod
    def create(under=None, type='geo', into=None, **kwargs):
        assert type is not None
        under = under or HTree().root
        node = under.createNode(type, **kwargs)
        node.setName(into)
        node.moveToGoodPosition()
        return node

    def __str__(self):
        return '<{}:{}>'.format(
            self.__class__.__name__,
            self.name)
    __repr__ = __str__

    def __init__(self, **kwargs):
        """
        """
        node = kwargs.pop('node', None )
        self.create_kwargs = kwargs
        self.copy_count = 0
        if node is None:
            self.type_string = kwargs.pop('type', 'geo')
            self.run_init_scripts = kwargs.pop('run_init_scripts', True)
            self.under = kwargs.pop('under', self.tree['/obj'])
            self.into = kwargs.pop('into', uniq())
            assert isinstance(self.type_string, (basestring,))
            path_name = '/obj/{}'.format(self.into)
            try:
                old_node = self.tree[path_name]
            except KeyError:
                created  = True
                node = Node.create(
                    under=self.under,
                    type=self.type_string,
                    run_init_scripts=self.run_init_scripts,
                    into=self.into)
            else:
                created = False
                node = old_node
        self.node = node
        self.logger_name = self.name
        HWrapper.__init__(self)
        # created and self.logger.debug("created: {}".format(node))
        # not created and self.logger.debug("reused: {}".format(node))
        self.createNode = self.node.createNode
        self.parm = self.node.parm
        self.setParmTransform  = getattr(
            self.node, 'setParmTransform', None)
        self.setWorldTransform  = getattr(
            self.node, 'setWorldTransform', None)
        self.buildLookatRotation  = getattr(
            self.node, 'buildLookatRotation', None)

    def children(self):
        """
        """
        return [
            self.__class__(node=node) for node in self.node.children()
        ]

    @property
    def name(self):
        return self.node.name()

    def copy(self, under=None, into=None): #node=None, count=1, **kwargs):
        """
        """
        self.copy_count += 1
        results = []
        # create_kwargs = self.create_kwargs.copy()
        into = into or '{}-{}-{}'.format(
            self.name, 'copy', self.copy_count)
        # create_kwargs.update(into=into)
        under = under or self.node.parent()
        # self.obj.createNode(
        #     self.type_string,
        #     run_init_scripts=self.run_init_scripts)
        # for i in range(1, count+1):
        self.logger.debug("copying into {} under {}".format(into, under))
        copy = hou.copyNodesTo(tuple([ self.node ]), under)
        copy = copy[0]
        # for copy in results:
        copy.moveToGoodPosition()
        copy.setName(into)
        return self.__class__(node=copy)

class NodeArray(HWrapper, list):

    def __init__(self, *nodes, **kwargs):
        self.nodes = []
        self.container = kwargs.pop('container', None)
        for i, node in enumerate(nodes):
            if not isinstance(node, (list, tuple)):
                node=[node]
            self.nodes += node
        list.__init__(self, self.nodes)
        self.container and self.set_input(self.container)

    @classmethod
    def create_from(cls, obj, count=1, use_original=True, **kwargs):
        """ """
        base = [] if not use_original else [obj]
        all = base + [
            obj.copy(into='{}-{}'.format(obj.name, i)) for i in range(count)
        ]
        return cls(*all, **kwargs)

    def copy(self, container=None):
        """ """
        all = [
            x.copy(
                into='{}-{}'.format(x.name, uniq()))
                for i,x in enumerate(self) ]
        [ x.node.setInput(0, None) for x in all ]
        if not container and self.container:
            container = self.container.copy(
                into=self.container.name + '-copy')
        kwargs = dict(container=container)
        tmp = self.__class__(*all, **kwargs)
        return tmp

    def map(self, fxn):
        return [ fxn(x) for x in self ]

    def map_enum(self, fxn):
        return [ fxn(i, x) for i,x in enumerate(self) ]

    def set_input(self, container):
        self.map(lambda x: x.node.setNextInput(container.node))

#     def set_input(self, umbrella):
#         # for x, row in enumerate(node_group):
#         #     for y, _node in enumerate(node_group):
#         for _node in self.nodes:
#             _node.setNextInput(umbrella)
#             geo = _node.children()[0].geometry()
#                 # bbox = geo.boundingBox()
#                 # center = bbox.center()
#                 # _node.center=center
#                 # node_array[x][y] = dict(
#                 #     node=_node, x=x, y=y,
#                 #     center=center)
#                 # # # https://www.sidefx.com/docs/houdini/hom/hou/BoundingBox.html https://www.sidefx.com/forum/topic/49734/ https://www.sidefx.com/forum/topic/11472/?page=1#post-54958
#                 # # create points at bounding box corners:
#                 # a = bbox.minvec()
#                 # b = (bbox.minvec()[0], bbox.maxvec()[1], bbox.minvec()[2])
#                 # c = (bbox.maxvec()[0], bbox.maxvec()[1], bbox.minvec()[2])
#                 # d = (bbox.maxvec()[0], bbox.minvec()[1], bbox.minvec()[2])
#                 # e = bbox.maxvec()
#                 # f = (bbox.maxvec()[0], bbox.minvec()[1], bbox.maxvec()[2])
#                 # g = (bbox.minvec()[0], bbox.minvec()[1], bbox.maxvec()[2])
#                 # h = (bbox.minvec()[0], bbox.maxvec()[1], bbox.maxvec()[2])
#                 # corners = [a,b,c,d,e,f,g,h]
#                 # print("corners: {}".format(corners))
#                 # # for i, position in enumerate(corners):
#                 # #     point = node.create(type='geo').children()[0].geometry().createPoint()
#                 # #     point.setPosition(position)

# def get_nodes():
#     return [n for n in hou.node('/').allSubChildren()]
#
#
# def print_tree(node, indent=0):
#     """ """
#     for child in node.children():
#         LOGGER.debug(" " * indent + child.name())
#         print_tree(child, indent + 3)
#
#
# def describe_nodes():
#     print_tree(hou.node('/'))
#     nodes = ["{} ({})".format(n.name(),  n.type().name(), )
#              for n in get_nodes()]
#     # hou.ui.displayMessage('\n'.join(nodes))
#     LOGGER.debug(nodes)
