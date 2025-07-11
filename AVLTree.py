"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 0
        self.bf = 0  # balance factor (left.height - right.height)

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        if self is None or self.key is None:
            return False
        return True

    """adds virtual children to the node"""

    def add_virtual_children(self):
        self.left = AVLNode(None, None)
        self.right = AVLNode(None, None)
        self.height = 0
        self.left.parent = self
        self.right.parent = self


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        self.max = None
        self.bf_zero_count = 0
        self.size1 = 0

    """searches for a node in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key
    """

    def search(self, key):
        if self.root is None:
            return None

        pointer = self.root
        while pointer.key is not None:
            if pointer.key == key:
                return pointer
            if key < pointer.key:
                pointer = pointer.left
            else:
                pointer = pointer.right
        return None

    def update_metadata(self, node):
        """Update the height and size of a node, assuming its children are never None"""
        if node.is_real_node():
            node.height = 1 + max(node.left.height, node.right.height)
            prev_bf = node.bf
            node.bf = node.left.height - node.right.height
            if prev_bf == 0 and node.bf != 0:
                self.bf_zero_count -= 1
            elif prev_bf != 0 and node.bf == 0:
                self.bf_zero_count += 1

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Fix parents
        y.parent = x.parent
        x.parent = y
        if T2.is_real_node():
            T2.parent = x

        # Reconnect to parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left == x:
                y.parent.left = y
            else:
                y.parent.right = y

        # Update metadata
        self.update_metadata(x)
        self.update_metadata(y)

        return y

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Fix parents
        x.parent = y.parent
        y.parent = x
        if T2.is_real_node():
            T2.parent = y

        # Reconnect to parent
        if x.parent is None:
            self.root = x
        else:
            if x.parent.left == y:
                x.parent.left = x
            else:
                x.parent.right = x

        # Update metadata
        self.update_metadata(y)
        self.update_metadata(x)

        return x

    def rotate_left_right(self, z):
        """
        Performs Left-Right rotation on node z:
        First, left-rotate z.left
        Then, right-rotate z
        """
        z.left = self.left_rotate(z.left)
        if z.left.is_real_node():
            z.left.parent = z
        return self.right_rotate(z)

    def rotate_right_left(self, z):
        """
        Performs Right-Left rotation on node z:
        First, right-rotate z.right
        Then, left-rotate z
        """
        z.right = self.right_rotate(z.right)
        if z.right.is_real_node():
            z.right.parent = z
        return self.left_rotate(z)

    """inserts a new node into the dictionary with corresponding key and value

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @param start: can be either "root" or "max"
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, key, val, start="root"):
        new_node = AVLNode(key, val)
        new_node.add_virtual_children()
        self.bf_zero_count += 1
        self.size1 += 1
        if self.root is None:
            self.root = new_node
            self.max = new_node
            return 0

        should_break = False
        stopper = None

        if start == "root" or (start == "max" and self.max is self.root):
            current = self.root
            while current.is_real_node():
                parent = current
                if key < current.key:
                    current = current.left
                else:
                    current = current.right
            new_node.parent = parent
            if key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
            node = new_node
            rotations = 0
        elif start == "max":
            pointer = self.max
            while pointer.parent is not None and pointer.key > new_node.key:
                pointer = pointer.parent
            current = pointer

            while current.is_real_node():
                parent = current
                if key < current.key:
                    current = current.left
                else:
                    current = current.right
            new_node.parent = parent
            if key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
            node = new_node
            rotations = 0
        else:
            return None
        while node is not None and node is not stopper:
            prev_h = node.height
            self.update_metadata(node)
            height_changed = prev_h != node.height
            if node.bf > 1:
                if key < node.left.key:
                    node = self.right_rotate(node)
                    rotations += 1
                else:
                    node = self.rotate_left_right(node)
                    rotations += 2
            elif node.bf < -1:
                if key > node.right.key:
                    node = self.left_rotate(node)
                    rotations += 1
                else:
                    node = self.rotate_right_left(node)
                    rotations += 2
            elif not height_changed:
                if should_break:
                    break
                should_break = True
            else:
                rotations += 1
            node = node.parent
        if new_node.key > self.max.key:
            self.max = new_node
        return rotations

    def predecessor(self, node):
        if not node.is_real_node():
            return None

        if node.left.is_real_node():
            curr = node.left
            while curr.right.is_real_node():
                curr = curr.right
            return curr

        curr = node
        while curr.parent is not None and curr.key == curr.parent.left.key:
            curr = curr.parent
        if curr.parent is None:
            return AVLNode(None, None)
        return curr.parent

    def successor(self, node):
        if not node.is_real_node():
            return None

        if node.right.is_real_node():
            curr = node.right
            while curr.left.is_real_node():
                curr = curr.left
            return curr

        curr = node
        while curr.parent is not None and curr.key == curr.parent.right.key:
            curr = curr.parent
        if curr.parent is None:
            return AVLNode(None, None)
        return curr.parent

    def rebalance_upwards(self, node):
        operations = 0
        while node is not None:
            pre_height = node.height
            self.update_metadata(node)
            post_height = node.height

            if node.bf > 1:
                if node.left.bf < 0:
                    node = self.rotate_left_right(node)
                    operations += 2
                else:
                    node = self.right_rotate(node)
                    operations += 1

            elif node.bf < -1:
                if node.right.bf > 0:
                    node = self.rotate_right_left(node)
                    operations += 2
                else:
                    node = self.left_rotate(node)
                    operations += 1

            if (pre_height == post_height) and (abs(node.bf) < 2):
                break
            else:
                operations += 1

            node = node.parent
        return operations

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, node):
        if node is None or not node.is_real_node():
            return 0
        if self.size == 1 and node is self.root:
            self.root = None
            self.max = None
            self.bf_zero_count = 0
            self.size1 = 0
            return 0

        self.size1 -= 1
        key = node.key
        current = self.root
        parent = AVLNode(None, None)

        while current.is_real_node() and current.key != key:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        if not current.is_real_node():
            return 0

        if current.left.is_real_node() and current.right.is_real_node():
            succ = self.successor(current)
            current.key = succ.key
            current.value = succ.value
            node = succ
            key = succ.key
        if node.bf == 0:
            self.bf_zero_count -= 1

        child = node.left if node.left.is_real_node() else node.right
        if node == self.root:
            self.root = child
            if child.is_real_node():
                child.parent = None
        else:
            if node == node.parent.left:
                node.parent.left = child
            else:
                node.parent.right = child
            if child.is_real_node():
                child.parent = node.parent

        if self.max == node:
            self.max = self.predecessor(node)

        operations = self.rebalance_upwards(node.parent)

        return operations

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        if self is None or self.root is None or not self.root.is_real_node():
            return []
        result = []
        node = self.root

        while node and node.is_real_node() and node.left.is_real_node():
            node = node.left

        while node and node.is_real_node():
            result.append((node.key, node.value))
            if node.right.is_real_node():
                node = node.right
                while node.left.is_real_node():
                    node = node.left
            else:
                while node.parent is not None and node == node.parent.right:
                    node = node.parent
                node = node.parent

        return result

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        if self is None or self.root is None:
            return 0
        return self.size1

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        if self is None or self.size1 == 0:
            return None
        return self.root

    """gets amir's suggestion of balance factor

    @returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
    """

    def get_amir_balance_factor(self):
        return self.bf_zero_count / self.size() if self.size() > 0 else 0

    def __repr__(self):  # you don't need to understand the implementation of this method
        def printree(root):
            if not root or root.key is None:
                return ["#"]

            root_key = str(root.key)
            height = str(root.height)  # החזרת הגובה לצד המפתח
            left, right = printree(root.left), printree(root.right)

            # חישוב רוחב הצומת בצורה שתכלול את הגובה, בלי להשפיע על המיקום של הקווים
            lwid = len(left[-1]) if left else 0
            rwid = len(right[-1]) if right else 0
            rootwid = len(root_key) + len(height) + 3  # לכלול גם את הגובה

            # הצגת הצומת עם הגובה
            result = [(lwid + 1) * " " + root_key + " (" + height + ")" + (rwid + 1) * " "]

            # חישוב הקווים והקישורים לצמתים
            ls = len(left[0].rstrip()) if left else 0
            rs = len(right[0]) - len(right[0].lstrip()) if right else 0
            result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

            # הוספת השורות של הצמתים השמאליים והימניים
            for i in range(max(len(left), len(right))):
                row = ""
                if i < len(left):
                    row += left[i]
                else:
                    row += lwid * " "

                row += (rootwid + 2) * " "

                if i < len(right):
                    row += right[i]
                else:
                    row += rwid * " "

                result.append(row)

            return result

        return '\n'.join(printree(self.root))