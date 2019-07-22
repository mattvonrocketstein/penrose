"""
penrose.hx.abcs:
"""


from penrose import (abcs, util,)

class Base(abcs.Loggable):
    @property
    def hou(self):
        import hou
        return hou

class HWrapper(Base):
    """ """
    @property
    def tree(self):
        """ """
        return HTree()

    @property
    def obj(self):
        """ """
        return self.tree['/obj']

    @property
    def out(self):
        """ """
        return self.tree['/out']


class HTree(dict, Base):
    """ """
    def __init__(self, tree=None, root=None, **kwargs):
        """ """
        self.tree = tree or \
            dict([
                [n.path(), n]
                for n in self.hou.node('/').allSubChildren()])
        self._root = root or '/obj'
        self.logger_name = 'HTree'
        abcs.Loggable.__init__(self)
        dict.__init__(self, self.tree)

    @property
    def root(self):
        return self[self._root]

    def __getitem__(self, name):
        """
        """
        if not name.startswith('/'):
            return self['/'+name]
        # components = [x.strip() for x in name.split('/') if x.strip() ]
        try:
            return self.tree.__getitem__(name)
        except KeyError as exc:
            err = "{}: choices: {}".format(exc, self.keys())
            self.logger.critical(err)
            raise KeyError(err)
