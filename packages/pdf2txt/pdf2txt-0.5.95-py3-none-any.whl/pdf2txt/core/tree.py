from random import randint


class SplitRectangleError(Exception):
    pass


# Binary tree node
class Node:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    @property
    def is_leaf(self):
        return self.left is None and self.right is None

    # An iterative process to print preorder traveral of BT
    def print(self):

        # Base CAse
        if self is None:
            return

            # create an empty stack and push root to it
        nodeStack = []
        nodeStack.append(self)

        # Pop all items one by one. Do following for every popped item
        # a) print it
        # b) push its right child
        # c) push its left child
        # Note that right child is pushed first so that left
        # is processed first */
        while (len(nodeStack) > 0):

            # Pop the top item from stack and print it
            node = nodeStack.pop()
            print(node.data)

            # Push right and left children of the popped node
            # to stack
            if node.right is not None and node.right not in nodeStack:
                nodeStack.append(node.right)
            if node.left is not None and node.left not in nodeStack:
                nodeStack.append(node.left)
            # Function to print leaf

    def get_leaf_nodes(self):
        leafs = []

        def _get_leaf_nodes(node):
            if node is not None:
                if node.is_leaf:
                    leafs.append(node.data)
                if node.left:
                    _get_leaf_nodes(node.left)
                if node.right:
                    _get_leaf_nodes(node.right)

        _get_leaf_nodes(self)
        return leafs
class Rect:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self._area = None
        self._room = None

    @property
    def area(self):
        if self._area is None:
            self._area = self.width * self.height
        return self._area

    @property
    def room(self):
        if self._room is None:
            self._room = self.create_room()
        return self._room

    def create_room(self):
        padding = self.options['padding']
        min_wall_size = self.options['min_wall_size']
        min_walls_ratio = self.options['min_walls_ratio']
        min_area_percent = self.options['min_area_percent']

        x = randint(self.x + padding, self.x + int(self.width / 2))
        y = randint(self.y + padding, self.y + int(self.height / 2))

        width = randint(min_wall_size, self.x + self.width - x) - padding
        height = randint(min_wall_size, self.y + self.height - y) - padding

        if (height / width < min_walls_ratio or width / height < min_walls_ratio or
                width * height < min_area_percent * self.area):
            return self.create_room()

        return Rect(x, y, width, height, self.options)


def split_rect(rect, options):

    if randint(0, 1) == 0:  # split vertical
        r1 = Rect(
            rect.x, rect.y,
            randint(min_split_size, rect.width), rect.height,
            options
        )
        r2 = Rect(
            rect.x + r1.width, rect.y,
            rect.width - r1.width, rect.height,
            options
        )

        # retry if ratio is too small
#        if r1.width / r1.height < min_walls_ratio or r2.width / r2.height < min_walls_ratio:
#            return split_rect(rect, options)
#     else:  # split horizontal
#         r1 = Rect(
#             rect.x, rect.y,
#             rect.width, randint(min_split_size, rect.height),
#             options
#         )
#         r2 = Rect(
#             rect.x, rect.y + r1.height,
#             rect.width, rect.height - r1.height,
#             options
#         )
#
#         # retry if ratio is too small
#         if r1.height / r1.width < min_walls_ratio or r2.height / r2.width < min_walls_ratio:
#             return split_rect(rect, options)
    return r1, r2


def split_tree_of_rectangles(rect, step, options):
    tree = Node(rect)
    if step != 0:
        split = split_rect(rect, options)
        if split:
            tree.left = split_tree_of_rectangles(split[0], step - 1, options)
            tree.right = split_tree_of_rectangles(split[1], step - 1, options)
    return tree
