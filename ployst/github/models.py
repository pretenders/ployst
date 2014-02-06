class Hierarchy(list):

    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        if not key in self._data:
            new_row = HierarchyLevel(level=key, notify=self.new_node)
            self._data[key] = new_row
        return self._data[key]

    def get_node(self, branch_name):
        for level in self:
            node = level.get_node(branch_name)
            if node:
                return node

    def get_parent(self, level):
        "Get the appropriate parent node for items on the level given"
        while level > 0:
            try:
                return self[level-1][0]
            except IndexError:
                level -= 1
        return None

    def new_node(self, node, hierarchy_level):
        """
        Callback for when nodes are added to levels.

        Add the parent for the node, and take care of other nodes parents.

        Assign the parent for this node.
        If this is the first node for the level:
          - Insert the row into the hierarcy at this point.
          - Ensure that all nodes in the level below are pointing to this node
            for parenthood.
        """
        level = hierarchy_level.level
        node.parent = self.get_parent(level)

        if len(hierarchy_level) == 1:
            for child_node in self[level + 1]:
                child_node.parent = node
            self.insert(level, hierarchy_level)


class HierarchyLevel(list):

    def __init__(self, level, notify):
        self._nodes = {}
        self.level = level
        self.notify = notify

    def get_node(self, branch_name):
        try:
            return self._nodes[branch_name]
        except KeyError:
            return None

    def append(self, item):
        node = HierarchyNode(*item)
        self._nodes[node.branch] = node
        super(HierarchyLevel, self).append(node)
        self.notify(node, self)


class HierarchyNode(object):

    def __init__(self, branch, commit):
        self.branch = branch
        self.commit = commit
        self._parent = None
        self.children = []
        self.in_parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if self._parent:
            self._parent.children.remove(self)
        self._parent = value
        if self._parent:
            self._parent.children.append(self)

    def __eq__(self, other):
        # import pdb; pdb.set_trace()
        if type(other) == tuple:
            return (self.branch, self.commit) == other
        elif type(other) == HierarchyNode:
            if self.branch == other.branch and self.commit == other.commit:
                return True
        return False
