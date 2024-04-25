class Node(object):
    def __init__(self, orderId, ETA, priority, currSysTime, orderValue, deliveryTime) -> None:
        self.eta = ETA
        self.priority = priority
        
        self.id = orderId
        self.createTime = currSysTime
        self.value = orderValue
        self.deliveryTime = deliveryTime

        self.leftChi = None
        self.rightChi = None
        self.parent = None
        self.height = 1
    
    def updateHeight(self):
        leftHeight = 0 if not self.leftChi else self.leftChi.height
        rightheight = 0 if not self.rightChi else self.rightChi.height
        self.height = max(leftHeight, rightheight) + 1

class avlTree(object):
    def __init__(self) -> None:
        self.root = None
        
    def insert(self, curr, node):
        if not curr:
            self.root = node
            curr = self.root
        elif node.priority > curr.priority:
            if curr.rightChi:
                self.insert(curr.rightChi, node)
            else:
                curr.rightChi = node
                node.parent = curr
        else:
            if curr.leftChi:
                self.insert(curr.leftChi, node)
            else:
                curr.leftChi = node
                node.parent = curr
        
        curr.updateHeight()

        # balance tree
        self.balanceTree(curr)

    def delete(self, curr, key, id):
        if not curr:
            # fell off
            return
        
        elif curr.id == id:
            parent = curr.parent
            if not curr.leftChi:
                if parent is None:
                    if curr.rightChi is None:
                        self.root = None
                    else:
                        self.root = curr.rightChi
                        curr.parent = None
                else:
                    if curr.rightChi is None:
                        if parent.leftChi == curr:
                            parent.leftChi = None
                        else:
                            parent.rightChi = None
                    else:
                        if parent.leftChi == curr:
                            parent.leftChi = curr.rightChi
                            curr.rightChi.parent = parent
                        else:
                            parent.rightChi = curr.rightChi
                            curr.rightChi.parent = parent
                curr = curr.rightChi

            elif not curr.rightChi:
                # it only has a left child
                parent = curr.parent
                if not parent:
                    self.root = curr.leftChi
                    curr.leftChi.parent = None
                else:
                    if parent.leftChi == curr:
                        parent.leftChi = curr.leftChi
                        curr.leftChi.parent = parent
                    else:
                        parent.rightChi = curr.leftChi
                        curr.leftChi.parent = parent
                curr = curr.leftChi

            # order of node is two (has both children)
            else:
                # find min in right subtree
                # swap and delete
                minNode = self.getMin(curr.rightChi)
                self.nodeSwap(curr, minNode)
                self.delete(curr, key, id)
        
        elif key > curr.priority:
            self.delete(curr.rightChi, key, id)
        elif key <= curr.priority:
            self.delete(curr.leftChi, key, id)
        
        if curr:
            # update height
            curr.updateHeight()

            # balance tree
            self.balanceTree(curr)

    def rRotate(self, A, B):
        parent = A.parent

        Bl = B.leftChi
        B.leftChi = A
        A.parent = B
        A.rightChi = Bl
        if Bl:
            Bl.parent = A
        B.parent = parent

        A.updateHeight()
        B.updateHeight()

        if not parent:
            self.root = B
        elif parent.leftChi == A:
            parent.leftChi = B
            parent.updateHeight()
        elif parent.rightChi == A:
            parent.rightChi = B
            parent.updateHeight()

    def lRotate(self, A, B):
        parent = A.parent

        Br = B.rightChi
        B.rightChi = A
        A.parent = B
        A.leftChi = Br
        if Br:
            Br.parent = A
        B.parent = parent

        A.updateHeight()
        B.updateHeight()

        if not parent:
            self.root = B
        elif parent.leftChi == A:
            parent.leftChi = B
            parent.updateHeight()
        elif parent.rightChi == A:
            parent.rightChi = B
            parent.updateHeight()

    def rlRotate(self, A, B, C):
        self.lRotate(B, C)
        self.rRotate(A, C)

    def lrRotate(self, A, B, C):
        self.rRotate(B, C)
        self.lRotate(A, C)
    
    def balanceTree(self, curr):
        if not curr:
            return
        if self.getBf(curr) < -1:
            if self.getBf(curr.rightChi) == 1:
                self.rlRotate(curr, curr.rightChi, curr.rightChi.leftChi)
            else:
                self.rRotate(curr, curr.rightChi)

        elif self.getBf(curr) > 1:
            if self.getBf(curr.leftChi) == -1:
                self.lrRotate(curr, curr.leftChi, curr.leftChi.rightChi)
            else:
                self.lRotate(curr, curr.leftChi)

    @staticmethod
    def getBf(node):
        if not node.leftChi and not node.rightChi:
            return 0
        elif not node.leftChi:
            return -node.rightChi.height
        elif not node.rightChi:
            return node.leftChi.height
        else:
            return node.leftChi.height - node.rightChi.height
        
    @staticmethod
    def getMin(node):
        while not node.leftChi:
            node = node.leftChi
        return node
    
    @staticmethod
    def nodeSwap(A, B):
        # id, createTime, value, deliveryTime, eta, priority
        tmp = [A.id, A.createTime, A.value, A.deliveryTime, A.eta, A.priority]

        A.id = B.id
        A.createTime = B.createTime
        A.value = B.value
        A.deliveryTime = B.deliveryTime
        A.eta = B.eta
        A.priority = B.priority

        B.id = tmp[0]
        B.createTime = tmp[1]
        B.value = tmp[2]
        B.deliveryTime = tmp[3]
        B.eta = tmp[4]
        B.priority = tmp[5]