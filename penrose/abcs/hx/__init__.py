#
"""
"""
from penrose import (abcs, util,)


class Universe(abcs.Loggable):

    @property
    def htree(self):
        """
        """
        import hou
        # yep, that's not a real tree yet
        return HTree.singleton or \
            HTree(dict(
                out=hou.node('/out/'),
                obj=hou.node('/obj/')))

    @property
    def obj(self):
        return self.htree.tree['obj']

    @property
    def out(self):
        return self.htree.tree['out']

    @property
    def obj(self):
        return self.htree.tree['obj']


class HTree(Universe):

    singleton = None

    def __init__(self, tree, **kwargs):
        assert not HTree.singleton, 'already instantiated'
        self.tree = tree
        HTree.singleton = self

    @property
    def htree(self):
        return self
