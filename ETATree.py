class TreeNode:
    def __init__(self, orderId, cst, ov, dt):
        self.orderId = orderId
        self.orderValue = ov
        self.deliveryTime = dt
        self.currSysTime = cst
        self.ETA = 0
        self.priority = self.calculate_priority(ov, cst)
        self.left = None
        self.right = None
        self.height = 0

    def calculate_priority(self, orderValue, systemTime):
        return (0.3 * (orderValue / 50)) - (0.7 * systemTime)

    def calculate_eta(self, deliveryTime, systemTime):
        return max(self.priority, systemTime) + deliveryTime


class ETATree:
    def __init__(self):
        self.root = None

    def create_order_in_eta(self, orderId, currSysTime, orderValue, deliveryTime, eta):
        normalized_order_val = orderValue / 50
        priority = (0.3 * normalized_order_val) - (0.7 * currSysTime)
        self.insert_recursive(self.root, orderId, currSysTime, orderValue, deliveryTime, eta, priority)

    def insert_recursive(self, node, orderId, cst, ov, dt, eta, priority):
        if node is None:
            node = TreeNode(orderId, cst, ov, dt)
            node.ETA = eta
            return node

        elif priority >= node.priority:
            node.left = self.insert_recursive(node.left, orderId, cst, ov, dt, eta, priority)
            self.ensure_balance(node)
            return node
        else:
            node.right = self.insert_recursive(node.right, orderId, cst, ov, dt, eta, priority)
            self.ensure_balance(node)
            return node

    def ensure_balance(self, node):
        if not node:
            return

        initial_balance = self.get_balance_factor(node)
        if abs(initial_balance) > 2:
            raise RuntimeError("ERROR: Detected invalid balance factor")

        if initial_balance == -2:
            bal = self.get_balance_factor(node.left)
            if bal == 1 or bal == 0:
                self.rotate_left(node)
            else:
                self.rotate_right_left(node)
        elif initial_balance == 2:
            bal = self.get_balance_factor(node.right)
            if bal == -1 or bal == 0:
                self.rotate_right(node)
            else:
                self.rotate_left_right(node)

        self.update_height(node)

    def rotate_left(self, node):
        x = node
        y = node.right
        z = node.right.left

        x.right = z
        y.left = x
        node = y

        self.update_height(x)
        self.update_height(y)

        return node

    def rotate_right(self, node):
        x = node
        y = node.left
        z = node.left.right

        x.left = z
        y.right = x
        node = y

        self.update_height(x)
        self.update_height(y)

        return node

    def rotate_left_right(self, node):
        self.rotate_left(node.left)
        return self.rotate_right(node)

    def rotate_right_left(self, node):
        self.rotate_right(node.right)
        return self.rotate_left(node)

    def get_balance_factor(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        if not node:
            return
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_height(self, node):
        if not node:
            return -1
        return node.height

    def find_node_eta(self, orderId):
        if not self.root:
            return 0
        node = self.find_node(self.root, orderId)
        if node:
            return node.ETA + node.deliveryTime
        return 0

    def find_node(self, node, orderId):
        if not node:
            return None
        if node.orderId == orderId:
            return node
        left_result = self.find_node(node.left, orderId)
        if left_result:
            return left_result
        return self.find_node(node.right, orderId)
