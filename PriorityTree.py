class Node(object):
    def __init__(self, priority, eta, orderID, currSysTime, orderValue, deliveryTime):
        self.priority = priority
        self.eta = eta
        self.orderID = orderID
        self.currSysTime = currSysTime
        self.orderValue = orderValue
        self.deliveryTime = deliveryTime
        
        self.leftChi = None
        self.rightChi = None
        
        self.height = 0

class PriorityTree(object):
    def __init__(self):
        self.root = None
        self.orders  = {}

    def createOrder(self, orderID, currSysTime, orderValue, deliveryTime):
        priority = (0.3 * (orderValue/50)) - (0.7 * currSysTime)
        self.root = self.createNode(self.root, priority, orderID, currSysTime, orderValue, deliveryTime)
        
        self.orders[orderID] = {
            "orderID": orderID,
            "currSysTime": currSysTime,
            "orderValue": orderValue,
            "deliveryTime": deliveryTime
        }

    def createNode(self, node, priority, orderID, currSysTime, orderValue, deliveryTime):
        if node is None:
            return Node(priority, orderID, currSysTime, orderValue, deliveryTime)

        if priority <= node.priority:
            node.leftChi = self.createNode(node.leftChi, priority, orderID, currSysTime, orderValue, deliveryTime)
        else:
            node.rightChi = self.createNode(node.rightChi, priority, orderID, currSysTime, orderValue, deliveryTime)

        node.height = 1 + max(self.retHeight(node.leftChi), self.retHeight(node.rightChi)) 
        
        return self.ensureBalance(node)
    
    def retHeight(self, node):
        if node is None:
            return -1
        return node.height

    def retBalance(self, node):
        if node is None:
            return 0
        return self.retHeight(node.leftChi) - self.retHeight(node.rightChi)

    def ensureBalance(self, node):
        balanceVal = self.retBalance(node)
        
        if balanceVal > 1:
            if self.retBalance(node.leftChi) >= 0:
                return self.rotateRight(node)
            else:
                return self.rotateLR(node)
        elif balanceVal < -1:
            if self.retBalance(node.rightChi) <= 0:
                return self.rotateLeft(node)
            else:
                return self.rotateRL(node)
        return node

    def rotateRight(self, data):
        temp = data.leftChi
        ex = temp.rightChi
        temp.rightChi = data
        data.leftChi = ex
       
        data.height = 1 + max(self.retHeight(data.leftChi), self.retHeight(data.rightChi))
        temp.height = 1 + max(self.retHeight(temp.leftChi), self.retHeight(temp.rightChi))
        
        return temp

    def rotateLeft(self, data):
        temp = data.rightChi
        ey = temp.leftChi
        temp.leftChi = data
        data.rightChi = ey
        
        data.height = 1 + max(self.retHeight(data.leftChi), self.retHeight(data.rightChi))
        temp.height = 1 + max(self.retHeight(temp.leftChi), self.retHeight(temp.rightChi))
        
        return temp
    
    def rotateLR(self, data):
        data.leftChi = self.rotateLeft(data.leftChi)
        return self.rotateRight(data)
    
    def rotateRL(self, data):
        data.rightChi = self.rotateRight(data.rightChi)
        return self.rotateLeft(data)
    
    
    def cancelOrder(self, priority, orderID, currSysTime):
        if self.root is None:
            print("AVL Tree is empty.")
        else:
            self.root = self.cancelNode(self.root, priority)

    def cancelNode(self, node, priority):
        if node is None:
            return None
        elif priority < node.priority:
            node.leftChi = self.cancelNode(node.leftChi, priority)
        elif priority > node.priority:
            node.rightChi = self.cancelNode(node.rightChi, priority)
        else:
            if node.leftChi is None and node.rightChi is None:
                return None
            elif node.leftChi is None:
                tempNode = node.rightChi
                return tempNode
            elif node.rightChi is None:
                tempNode = node.leftChi
                return tempNode
            
            tempNode = self.getPredecessor(node.leftChi)
            node.priority = tempNode.priority
            node.leftChi = self.cancelNode(node.leftChi, tempNode.priority)
            
        if not node:
            return node

        node.height = 1 + max(self.retHeight(node.leftChi), self.retHeight(node.rightChi))
        balanceVal = self.retBalance(node)

        if balanceVal > 1 and self.retBalance(node.leftChi) >= 0:
            return self.rotateRight(node)

        if balanceVal < -1 and self.retBalance(node.rightChi) <= 0:
            return self.rotateLeft(node)

        if balanceVal > 1 and self.retBalance(node.leftChi) < 0:
            return self.rotateLR(node)

        if balanceVal < -1 and self.retBalance(node.rightChi) > 0:
            return self.rotateRL(node)
        
        return node
    
    def getPredecessor(self, node):
        if node.rightChi:
            return self.getPredecessor(node.rightChi)
        return node
    
    # def printRoot(self):
    #     print(self.root.priority)
    #     return
    
    def traverse(self):
        if self.root:
            self.traverseInOrder(self.root)

    def traverseInOrder(self, node):
        if node.leftChi:
            self.traverseInOrder(node.leftChi)
        print('%s' % node.priority)
        if node.rightChi:
            self.traverseInOrder(node.rightChi)
            
    def printOrderDetails(self, orderID):
        if orderID in self.orders:
            orderDetails = self.orders[orderID]
            print(f"[{orderID}, {orderDetails['currSysTime']}, {orderDetails['orderValue']}, {orderDetails['deliveryTime']}]")
        else:
            print("Order not found.")
            
      
if __name__ == '__main__':
    avl = PriorityTree()
    avl.createOrder(1001, 1, 200, 3)
    avl.createOrder(1002, 3, 250, 6)
    avl.createOrder(1003, 8, 100, 3)
    avl.createOrder(1004, 13, 100, 5)
    avl.createOrder(1005, 30, 300, 3)
    avl.traverse()
    
    avl.printOrderDetails(1005)
    # avl.printRoot()
    