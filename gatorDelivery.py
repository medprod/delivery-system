from AVLTree import Node, avlTree

myTree = avlTree()

nodes = {}                  
orders = {
    "eta": [],              
    "priority": [],       
    "ID": [],               
    "deliveryTime": [],     
    "deliveryStatus": [],   
}

retTime = 0
currSize = 0

def getPriority(orderValue, createTime, valueWeight=0.3, timeWeight=0.7):
    return (0.3*orderValue/50)-(0.7*createTime)

def printByTime(time1, time2):
    global orders
    orderString = ""
    for i in range(currSize):
        if orders["eta"][i] > time2:
            break
        elif orders["eta"][i] >= time1:
            orderString += f"{orders['ID'][i]}, "
    if len(orderString) > 0:
        return "["+orderString[:-2]+"]\n"
    else:
        return "No orders in that time period\n"

def printByOrder(orderId):
    global orders, nodes
    orderString = f"{orderId}"
    orderString += f", {nodes[orderId].createTime}"
    orderString += f", {nodes[orderId].value}"
    orderString += f", {nodes[orderId].deliveryTime}"
    orderString += f", {nodes[orderId].eta}"
    return "["+orderString+"]\n"

def getRankOfOrder(orderId):
    global orders
    if orderId not in orders["ID"]:
        return ""
    num = orders["ID"].index(orderId)

    return f"Order {orderId} will be delivered after {num} orders.\n"


def createOrder(orderId, currentSystemTime, orderValue, deliveryTime):
    global orders, nodes, currSize, retTime
    timestamp = max(currentSystemTime, retTime)
    startIdx = 0  
    deliveredOrders = {}
    for i in range(currSize):
        if currentSystemTime >= orders["eta"][i]:  
            orders["deliveryStatus"][i] = 2
            deliveredOrders[orders["ID"][i]] = orders["eta"][i]
            startIdx = i+1
            timestamp = max(timestamp, orders["eta"][i]+orders["deliveryTime"][i])
            retTime = orders["eta"][i]+orders["deliveryTime"][i]

        elif currentSystemTime >= orders["eta"][i]-orders["deliveryTime"][i]:
            orders["deliveryStatus"][i] = 1
            startIdx = i+1
            timestamp = orders["eta"][i]+orders["deliveryTime"][i]
            retTime = orders["eta"][i]+orders["deliveryTime"][i]
            break

        else:
            break

    priority = getPriority(orderValue, currentSystemTime)

    insertRank = currSize
    for i in range(startIdx, currSize):
        if priority > orders["priority"][i]:
            insertRank = i
            break
    
    if insertRank == startIdx:
        orderETA = timestamp + deliveryTime
    else:
        prevEndTime = orders["eta"][insertRank-1] + orders["deliveryTime"][insertRank-1]
        orderETA = prevEndTime + deliveryTime

    
    updatedOrders = {}
    prevEndTime = orderETA + deliveryTime
    for i in range(insertRank, currSize):
        currStartTime = orders["eta"][i]-orders["deliveryTime"][i]
        if currStartTime < prevEndTime:
            offset = abs(prevEndTime-currStartTime)
            orders["eta"][i] += offset
            updatedOrders[orders["ID"][i]] = orders["eta"][i]
        prevEndTime = orders["eta"][i]+orders["deliveryTime"][i]


    outputStr = ""

    outputStr += f"Order {orderId} has been created - ETA: {orderETA}\n"


    if len(updatedOrders) > 0:
        updatedString = ""
        for id, eta in updatedOrders.items():
            updatedString += f"{id}: {eta}, "
        outputStr += "Updated ETAs: [" + updatedString[:-2] + "]\n"


    if len(deliveredOrders) > 0:
        for id, eta in deliveredOrders.items():
            outputStr += f"Order {id} has been delivered at time {eta}\n"


    orders["ID"].insert(insertRank, orderId)
    orders["eta"].insert(insertRank, orderETA)
    orders["priority"].insert(insertRank, priority)
    orders["deliveryTime"].insert(insertRank, deliveryTime)
    orders["deliveryStatus"].insert(insertRank, 0)

    cutIdx = startIdx if startIdx == 0 or orders["deliveryStatus"][startIdx-1] == 2 else startIdx-1
    for i in range(cutIdx):
        removeKey = orders["priority"][i]
        removeId = orders["ID"][i]
        myTree.delete(myTree.root, removeKey, removeId)   
        nodes[orders["ID"][i]] = None         
        del nodes[orders["ID"][i]]             
    
    for l in orders.values():
        del l[:cutIdx]                         


    newOrderNode = Node(orderId, currentSystemTime, orderValue, deliveryTime, orderETA, priority)
    myTree.insert(myTree.root, newOrderNode)
    nodes[orderId] = newOrderNode
    
    currSize = currSize - cutIdx + 1

    return outputStr

def cancelOrder(orderId, currentSystemTime):
    global orders, nodes, currSize, retTime
    outputStr = ""

    deliveredOrders = {}
    for i in range(currSize):
        if currentSystemTime >= orders["eta"][i]:
            deliveredOrders[orders["ID"][i]] = orders["eta"][i]
        else:
            break

    if orderId not in nodes or currentSystemTime >= nodes[orderId].eta - nodes[orderId].deliveryTime:
        outputStr += f"Cannot cancel. Order {orderId} has already been delivered.\n"
        

        if len(deliveredOrders) > 0:
            for id, eta in deliveredOrders.items():
                outputStr += f"Order {id} has been delivered at time {eta}\n"

            for l in orders.values():
                del l[:len(deliveredOrders)]   

            for id in deliveredOrders:         
                keyForDel = nodes[id].priority
                idForDel = nodes[id].id
                nodes[id] = None
                del nodes[id]
                myTree.delete(myTree.root, keyForDel, idForDel)

            currSize -= len(deliveredOrders)      
                
        return outputStr

    orderIdx = orders["ID"].index(orderId)
    if orderIdx == currSize - 1:
        for l in orders.values():
            del l[orderIdx]
        nodes[orderId] = None
        del nodes[orderId]
        currSize -= 1
        return f"Order {orderId} has been canceled\n"
    
    timestamp = max(currentSystemTime, retTime)
    if orderIdx >= 1:
        timestamp = max(timestamp, orders["eta"][orderIdx-1]+orders["deliveryTime"][orderIdx-1])

    updatedOrders = {}
    prevEndTime = timestamp
    for i in range(orderIdx+1, currSize):
        currStartTime = orders["eta"][i] - orders["deliveryTime"][i]
        if currStartTime > prevEndTime:
            offset = abs(currStartTime-prevEndTime)
            orders["eta"][i] -= offset
            updatedOrders[orders["ID"][i]] = orders["eta"][i]
        prevEndTime = orders["eta"][i] + orders["deliveryTime"][i]


    outputStr += f"Order {orderId} canceled\n"


    if len(updatedOrders) > 0:
        updatedString = ""
        for id, eta in updatedOrders.items():
            updatedString += f"{id}: {eta}, "
        outputStr += "Updated ETAs: [" + updatedString[:-2] + "]\n"

    if len(deliveredOrders) > 0:
        for id, eta in deliveredOrders.items():
            outputStr += f"Order {id} has been delivered at time {eta}\n"
    
    for l in orders.values():
        del l[orderIdx]                
        del l[:len(deliveredOrders)]    
    
    keyForDel = nodes[orderId].priority
    idForDel = nodes[orderId].id
    nodes[orderId] = None              
    del nodes[orderId]                  
    myTree.delete(myTree.root, keyForDel, idForDel)

    for id in deliveredOrders:          
        keyForDel = nodes[id].priority
        idForDel = nodes[id].id
        nodes[id] = None
        del nodes[id]
        myTree.delete(myTree.root, keyForDel, idForDel)

    currSize -= (1 + len(deliveredOrders))     

    return outputStr

def updateTime(orderId, currentSystemTime, newDeliveryTime):
    global orders, nodes, currSize
    outputStr = ""

    deliveredOrders = {}
    for i in range(currSize):
        if currentSystemTime >= orders["eta"][i]:
            deliveredOrders[orders["ID"][i]] = orders["eta"][i]
        else:
            break

    for l in orders.values():
        del l[:len(deliveredOrders)]
    
    currSize -= len(deliveredOrders)

    for id in deliveredOrders:
        keyForDel = nodes[id].priority
        idForDel = nodes[id].id
        nodes[id] = None
        del nodes[id]
        myTree.delete(myTree.root, keyForDel, idForDel)
    
    if orderId not in nodes or currentSystemTime >= nodes[orderId].eta - nodes[orderId].deliveryTime:
        outputStr += f"Cannot update. Order {orderId} has already been delivered.\n"
        
        if len(deliveredOrders) > 0:
            for id, eta in deliveredOrders.items():
                outputStr += f"Order {id} has been delivered at time {eta}\n"
        
        return outputStr
    
    

    orderIdx = orders["ID"].index(orderId)
    offset = newDeliveryTime - orders["deliveryTime"][orderIdx]
    orders["eta"][orderIdx] += offset                   
    orders["deliveryTime"][orderIdx] = newDeliveryTime 
    nodes[orderId].eta = orders["eta"][orderIdx]       
    nodes[orderId].deliveryTime = newDeliveryTime

    updatedOrders = {}
    if offset != 0:
        updatedOrders[orderId] = orders["eta"][orderIdx]

    prevEndTime = orders["eta"][orderIdx] + newDeliveryTime
    for i in range(orderIdx+1, currSize):
        currStartTime = orders["eta"][i] - orders["deliveryTime"][i]
        offset = prevEndTime - currStartTime
        orders["eta"][i] += offset             
        nodes[orders["ID"][i]].eta += offset    
        updatedOrders[orders["ID"][i]] = orders["eta"][i]
        prevEndTime = orders["eta"][i] + orders["deliveryTime"][i]



    if len(updatedOrders) > 0:
        updatedString = ""
        for id, eta in updatedOrders.items():
            updatedString += f"{id}: {eta}, "
        outputStr += "Updated ETAs: [" + updatedString[:-2] + "]\n"
    

    if len(deliveredOrders) > 0:
        for id, eta in deliveredOrders.items():
            outputStr += f"Order {id} has been delivered at time {eta}\n"
    
    return outputStr

def outputRemaining():
    outputStr = ""
    for id, eta in zip(orders["ID"], orders["eta"]):
        outputStr += f"Order {id} has been delivered at time {eta}\n"

    return outputStr

def processCommand(cmd):
    cmd = cmd.strip().split('(')
    cmdType = cmd[0]
    argStr = cmd[1][:-1]
    args = argStr.split(",")
    args = [arg.strip() for arg in args]
    
    if cmdType == "print" and len(args) == 1:
        orderId = int(args[0])
        return printByOrder(orderId)
    
    elif cmdType == "print" and len(args) == 2:
        time1, time2 = map(int, args)
        return printByTime(time1, time2)
    
    elif cmdType == "getRankOfOrder" and len(args) == 1:
        orderId = int(args[0])
        return getRankOfOrder(orderId)
    
    elif cmdType == "createOrder" and len(args) == 4:
        orderId, currentSystemTime, orderValue, deliveryTime = map(int, args)
        return createOrder(orderId, currentSystemTime, orderValue, deliveryTime)
    
    elif cmdType == "cancelOrder" and len(args) == 2:
        orderId, currentSystemTime = map(int, args)
        return cancelOrder(orderId, currentSystemTime)
    
    elif cmdType == "updateTime" and len(args) == 3:
        orderId, currentSystemTime, newDeliveryTime = map(int, args)
        return updateTime(orderId, currentSystemTime, newDeliveryTime)

    else:
        print("Please enter a valid command.")
        return ""

if __name__ == "__main__":
    import sys

    inputFile = sys.argv[1]
    fileName = inputFile[:-4]

    outputStr = ""

    with open(inputFile, 'r') as f:
        cmd = f.readline()
        while not cmd.startswith("Quit()"):
            outputStr += processCommand(cmd[:-1])
            cmd = f.readline()

    if cmd.startswith("Quit()"):
        outputStr += outputRemaining()

    with open(f"{fileName}_output_file.txt", 'w') as f:
        f.writelines(outputStr)