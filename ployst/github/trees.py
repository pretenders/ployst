"""
Branch Hierarchy
===

A branch hierarchy is made up of a series of levels, each of which can have 1
or more nodes on them.

A node represents a branch and is instantiated with commit information.

It is important for a node to know who her parent is and which children are
hers. In the current implementation, a parent is assumed to be the first node
on the closest level "above" the node's current level.

eg. A Hierarchy containing:
Level 0: [A, B]
Level 1: [ ]
Level 2: [C]

C's parent is assumed to be A, due to level 1 having no nodes.

"""


class Hierarchy(list):

    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        if key not in self._data:
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
        """
        :param level:
            The level in the hierarchy that this level represents.

        :param notify:
            A function to be called when an item is appended to this level.
        """
        self._nodes = {}
        self.level = level
        self.notify = notify

    def get_node(self, branch_name):
        """
        Get the node identified by ``branch_name``.

        Return ``None`` if the node is not found on this level.
        """
        try:
            return self._nodes[branch_name]
        except KeyError:
            return None

    def append(self, (branch, commit)):
        """
        Append a HierarchyNode to this level using the branch and commit given.
        """
        node = HierarchyNode(branch, commit)
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
    def parent(self, node):
        """
        Set the parent of this HierarchyNode.

        Remove self from current parent's children, if there is one.
        Add self to the new parent's children.
        """
        if self._parent:
            self._parent.children.remove(self)
        self._parent = node
        if self._parent:
            self._parent.children.append(self)

    def __eq__(self, other):
        """
        Test for equality.

        If comparing against a tuple, compare my branch and commit.
        If comparing against a HierarchyNode, compare branches and commits.
        Else we aren't going to be equal.
        """
        if isinstance(other, tuple):
            return (self.branch, self.commit) == other
        elif isinstance(other, HierarchyNode):
            if self.branch == other.branch and self.commit == other.commit:
                return True
        return False
