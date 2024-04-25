class Node(object):
    def __init__(self, value):
        self.value = value
        self.leftChi = None
        self.rightChi = None
        self.height = 0

class AVLTree(object):
    def __init__(self):
        self.root = None

    def insertNode(self, value):
       self.root = self.insert(self.root, value)

    def insert(self, node, value):
        if node is None:
            return Node(value)

        if value <= node.value:
            node.leftChi = self.insert(node.leftChi, value)
        else:
            node.rightChi = self.insert(node.rightChi, value)

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
    
    
    def removeNode(self, value):
        if self.root is None:
            print("AVL Tree is empty.")
        else:
            self.root = self.remove(self.root, value)
            
    def remove(self, node, value):
        if node is None:
            return None
        elif value < node.value:
            node.leftChi = self.remove(node.leftChi, value)
        elif value > node.value:
            node.rightChi = self.remove(node.rightChi, value)
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
            node.value = tempNode.value
            node.leftChi = self.remove(node.leftChi, tempNode.value)
            
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
            
    def printRoot(self):
        print(self.root.value)
        return
    
    
    def traverse(self):
        if self.root:
            self.traverseInOrder(self.root)

    def traverseInOrder(self, node):
        if node.leftChi:
            self.traverseInOrder(node.leftChi)
        print('%s' % node.value)
        if node.rightChi:
            self.traverseInOrder(node.rightChi)

if __name__ == '__main__':
    avl = AVLTree()
    avl.insertNode(10)
    avl.insertNode(20)
    avl.insertNode(5)
    avl.insertNode(6)
    avl.insertNode(15)
    avl.traverse()

    avl.removeNode(20)
    avl.removeNode(15)
    avl.traverse()
        

        
            
            
            
            
                
                
            
            
            
    

            
        
        
        
        
        

            
        