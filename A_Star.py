import copy
import datetime
import math


# 打印节点
def showMatrix(matrix):
    for x in range(0, 3):
        for y in range(0, 3):
            print(matrix[x][y], end='')
        print(" ")
    print("--------")
    return


def Matrix2String(matrix):
    string = ""
    for x in range(0, 3):
        for y in range(0, 3):
            string += str(matrix[x][y])+' '
        string += '\n'
    return string


# 移动数码
def move(matrix, srcX, srcY, drcX, drcY):
    temp = matrix[srcX][srcY]
    matrix[srcX][srcY] = matrix[drcX][drcY]
    matrix[drcX][drcY] = temp
    return matrix


# 判断节点的奇偶性
def getStatus(matrix):
    sum = 0
    for i in range(0, 3):
        for j in range(0, 3):
            for m in range(0, i + 1):
                for n in range(0, j):
                    if matrix[i][j] > matrix[m][n]:

                        sum += 1
    return sum


# 定义节点数据
class Node:
    def __init__(self, matrix, g=0, h=0):
        self.matrix = matrix  # 二维数组
        self.father = None  # 父节点
        self.children = []
        self.g = g  # g(n):开始节点到节点n的路径代价
        self.h = h  # h(n):节点n到目标结点的最小代价路径估计值
        self.x = 0 
        self.y = 0 # positions 

    # 以Manhattan距离为启发函数
    def setH1(self, endNode):
        for x in range(0, 3):
            for y in range(0, 3):
                for m in range(0, 3):
                    for n in range(0, 3):
                        if self.matrix[x][y] == endNode.matrix[m][n]:
                            self.h += (abs(x - m) + abs(y - n))

    # 以不在目标位置上的点的个数为启发函数
    def setH2(self, endNode):
        for x in range(0, 3):
            for y in range(0, 3):
                if self.matrix[x][y] != endNode.matrix[x][y]:
                    self.h += 1

    # 以Euclidean距离为启发函数
    def setH3(self, endNode):
        for x in range(0, 3):
            for y in range(0, 3):
                for m in range(0, 3):
                    for n in range(0, 3):
                        if self.matrix[x][y] == endNode.matrix[m][n]:
                            self.h += math.sqrt((m-x)*(m-x)+(n-y)*(n-y))

    def setG(self, g):
        self.g = g

    def setFather(self, node):
        self.father = node

    def getG(self):
        return self.g


class A_Star:

    def __init__(self, startNode, endNode):

        # startNode:  起点
        # endNode:    终点

        # Open表
        self.openList = []
        # Close表
        self.closeList = []
        # 起点
        self.startNode = startNode
        # 终点
        self.endNode = endNode
        # 当前处理的节点
        self.currentNode = startNode
        # 最后生成的路径
        self.pathlist = []
        # 花费的代价(也是扩展的节点数)
        self.step = 0
        # 生成的节点数
        self.generate = 0
        # 搜索开始时间
        self.start_time = 0
        # 搜索结束时间
        self.end_time = 0

        return

    #  获得openlist中F值最小的节点
    def getMinFNode(self):
        nodeTemp = self.openList[0]
        for node in self.openList:
            if node.g + node.h < nodeTemp.g + nodeTemp.h:
                nodeTemp = node
        return nodeTemp

    # 判断节点是否在Open表中
    def nodeInOpenlist(self, node):
        for nodeTmp in self.openList:
            if nodeTmp.matrix == node.matrix:
                return True
        return False

    # 判断节点是否在Close表中
    def nodeInCloselist(self, node):
        for nodeTmp in self.closeList:
            if nodeTmp.matrix == node.matrix:
                return True
        return False

    # 判断终点是否在Open表中
    def endNodeInOpenList(self):
        for nodeTmp in self.openList:
            if nodeTmp.matrix == self.endNode.matrix:
                return True
        return False

    # 从Open表中取出节点
    def getNodeFromOpenList(self, node):
        for nodeTmp in self.openList:
            if nodeTmp.matrix == node.matrix:
                return nodeTmp
        return None

    # 搜索一个节点
    def searchOneNode(self, node):

        if self.nodeInCloselist(node):
            return

        gTemp = self.step  # G值计算

        # 如果节点不在Open表中，就把它加入
        if self.nodeInOpenlist(node) == False:
            node.setG(gTemp)
            node.setH3(self.endNode)  # H值计算   !!此行代码可更换启发函数，例setH1，setH2……
            self.openList.append(node)
            self.currentNode.children.append(node) # 记录子节点
            node.father = self.currentNode
        # 如果在Open表中，判断currentNode到当前点的G是否更小，如果更小，就重新计算g值，并且改变父节点
        else:
            nodeTmp = self.getNodeFromOpenList(node)
            if self.currentNode.g + gTemp < nodeTmp.g:
                nodeTmp.g = self.currentNode.g + gTemp
                nodeTmp.father.children.remove(nodeTmp)
                nodeTmp.father = self.currentNode
                self.currentNode.children.append(nodeTmp) # add child node. 
        return

    # 搜索下一个可以移动的数码，并进行移动，以此生成新节点
    def searchNext(self):
        flag = False
        for x in range(0, 3):
            for y in range(0, 3):
                if self.currentNode.matrix[x][y] == 0:
                    flag = True
                    break
            if flag == True:
                break

        self.step += 1

        # 移动数码
        if x - 1 >= 0:
            self.generate += 1
            matrixTemp = move(copy.deepcopy(
                self.currentNode.matrix), x, y, x - 1, y)
            self.searchOneNode(Node(matrixTemp))
        if x + 1 < 3:
            self.generate += 1
            matrixTemp = move(copy.deepcopy(
                self.currentNode.matrix), x, y, x + 1, y)
            self.searchOneNode(Node(matrixTemp))
        if y - 1 >= 0:
            self.generate += 1
            matrixTemp = move(copy.deepcopy(
                self.currentNode.matrix), x, y, x, y - 1)
            self.searchOneNode(Node(matrixTemp))
        if y + 1 < 3:
            self.generate += 1
            matrixTemp = move(copy.deepcopy(
                self.currentNode.matrix), x, y, x, y + 1)
            self.searchOneNode(Node(matrixTemp))
        return

    # 开始搜索
    def start(self):

        self.start_time = datetime.datetime.now()

        # 判断是否有解，只有当起点和终点的奇偶性相同时，才有解
        start_sum = getStatus(self.startNode.matrix)
        end_sum = getStatus(self.endNode.matrix)
        if start_sum % 2 != end_sum % 2:
            return False

        # 将初始节点加入Open表
        self.startNode.setH3(self.endNode)   # 此行代码可更换启发函数，例setH1，setH2……
        self.startNode.setG(self.step)
        self.openList.append(self.startNode)

        # 获取当前Open表里F值最小的节点,把它添加到Close表中，并从Open表中删除它
        while True:
            self.currentNode = self.getMinFNode()
            self.closeList.append(self.currentNode)
            self.openList.remove(self.currentNode)
            self.step = self.currentNode.getG()
            self.searchNext()

            # 检验是否结束
            if self.endNodeInOpenList():  # 终点在Open表中
                nodeTmp = self.getNodeFromOpenList(self.endNode)
                # 将路径中的节点压入pathlist中
                while True:
                    self.pathlist.append(nodeTmp)
                    if nodeTmp.father != None:
                        nodeTmp = nodeTmp.father
                    else:
                        self.end_time = datetime.datetime.now()
                        return True
            elif len(self.openList) == 0:  # Open表中已无节点，但终点此时仍没有出现
                return False
            elif self.step > 31:  # 8数码问题最大移动步数为31
                return False

    # 输出移动过程
    def showPath(self):
        for node in self.pathlist[::-1]:
            showMatrix(node.matrix)

    # 输出搜索所花时间
    def showTime(self):
        print("搜索花费总时间:", (self.end_time - self.start_time).microseconds/1000, "ms")

    # 输出扩展节点数
    def showStep(self):
        print("扩展的节点数:", self.step)

    def showGenerate(self):
        print("生成的节点数:", self.generate)

    def getTime(self):
        return (self.end_time - self.start_time).microseconds/1000

    def getPath(self):
        return self.pathlist[::-1]

    def getPathString(self):
        string = ""
        for n in self.pathlist[::-1]:
            string += Matrix2String(n.matrix)
            string += '\n'
        return string
