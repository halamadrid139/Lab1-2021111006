import numpy as np
import random
# 绘制有向图
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib import colors


def displayMatrix(G):
    # 从G中提取节点和邻接矩阵
    node, matrix = G
    # 创建一个自定义的颜色映射
    cmap = colors.ListedColormap(['white', 'lightblue'])
    # 创建一个规范化对象
    norm = colors.Normalize(vmin=0, vmax=1)
    # 使用matplotlib的matshow函数来显示邻接矩阵
    plt.matshow(matrix, fignum=1, cmap=cmap, norm=norm)
    # 在每个单元格中添加权重值
    for i in range(len(node)):
        for j in range(len(node)):
            plt.text(j, i, matrix[i][j], ha='center', va='center', color='black')
    # 设置x轴和y轴的刻度
    plt.xticks(np.arange(len(node)), node, rotation=90)
    plt.yticks(np.arange(len(node)), node)
    # 显示图形
    plt.savefig('matrix.jpg')
    plt.show()


def showDirectedGraph(G):
    # 从G中提取节点和邻接矩阵
    node, matrix = G
    # 创建一个有向图
    graph = nx.DiGraph()
    # 添加节点
    for n in node:
        graph.add_node(n)
    # 添加边和权重
    for i in range(len(node)):
        for j in range(len(node)):
            if matrix[i][j] != 0:
                # 添加一个键来区分两个方向的边
                graph.add_edge(node[i], node[j], weight=matrix[i][j])

    # 绘制图形
    plt.figure(figsize=(10, 10))  # 设置图形大小
    # pos = nx.random_layout(graph) # 结点随机分布
    pos = nx.circular_layout(graph)  # 结点在一个圆环上均匀分布
    edges = graph.edges(data=True)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, width=2)
    edge_labels = {(u, v): d['weight'] for u, v, d in edges}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10, label_pos=0.3)  # 权重标签在靠近目标节点的位置
    # 显示图形
    plt.savefig('graph.jpg')
    plt.show()


def queryBridgeWords(G, word1, word2, verbose):
    # 从G中提取节点和邻接矩阵
    node, matrix = G
    # 检查word1和word2是否在节点列表中
    if word1 not in node and word2 in node:
        if verbose: print(f"No “{word1}” in the graph!")
        return []
    elif word2 not in node and word1 in node:
        if verbose: print(f"No “{word2}” in the graph!")
        return []
    elif word1 not in node and word2 not in node:
        if verbose: print(f"No “{word1}” and “{word2}” in the graph!")
        return []
    # 获取word1和word2在节点列表中的索引
    index1 = node.index(word1)
    index2 = node.index(word2)
    # 找到所有的桥接词
    bridge_words = []
    for i in range(len(node)):
        if matrix[index1][i] != 0 and matrix[i][index2] != 0:
            bridge_words.append(node[i])
    # 如果桥接词列表为空，打印"No bridge words from word1 to word2!"
    if not bridge_words:
        if verbose: print(f"No bridge words from {word1} to {word2}!")
    else:
        # 如果桥接词列表只有一个元素，直接输出
        if len(bridge_words) == 1:
            if verbose: print(f"The bridge word from {word1} to {word2} is: {bridge_words[0]}.")
        elif len(bridge_words) == 2:
            # 如果桥接词列表有两个元素，直接用"and"连接
            if verbose: print(f"The bridge words from {word1} to {word2} are: {bridge_words[0]} and {bridge_words[1]}.")
        else:
            # 如果桥接词列表有三个或更多元素，使用逗号和"and"来连接
            if verbose: print(
                f"The bridge words from {word1} to {word2} are: {', '.join(bridge_words[:-1])} and {bridge_words[-1]}.")
    return bridge_words


def generateNewText(G, text):
    # 将文本转换为小写并分割成单词列表
    words = text.lower().split()
    # 创建一个新的列表来存储修改后的单词
    new_words = []
    # 遍历单词列表
    for i in range(len(words) - 1):
        # 添加当前单词到新的单词列表
        new_words.append(words[i])

        # 找到当前单词和下一个单词的桥接词
        bridge_words = queryBridgeWords(G, words[i], words[i + 1], False)

        # 如果找到了桥接词，从中随机选择一个并添加到新的单词列表
        if bridge_words:
            bridge_word = random.choice(bridge_words)
            new_words.append(bridge_word)

    # 添加最后一个单词到新的单词列表
    new_words.append(words[-1])

    # 将新的单词列表转换回文本
    new_text = ' '.join(new_words)
    print(new_text)
    return new_text


x = float('inf')


def dijkstra(matrix, begin, end):
    mat = matrix.copy()  # 防止matrix数组被修改
    bkd = False  # 不可达判断
    wcb = False  # 该结点无出边
    maxsize = 1000  # 足够大的数表示inf
    n = len(mat)
    for i in range(0, n):
        for j in range(0, n):
            if i != j and mat[i][j] == 0:
                mat[i][j] = maxsize
    parent = []  # 用于记录每个结点的父辈结点
    collected = []  # 用于记录是否经过该结点
    distTo = mat[begin]  # 用于记录该点到begin结点路径长度,初始值存储所有点到起始点距离
    path = []  # 用于记录路径
    for i in range(0, n):  # 初始化工作
        if i == begin:
            collected.append(True)  # 所有结点均未被收集
        else:
            collected.append(False)
        parent.append(-1)  # 均不存在父辈结点
    while True:
        if collected[end] == True:
            break
        min_n = maxsize
        v = maxsize  # 防止结点无出边
        for i in range(0, n):
            if collected[i] == False:
                if distTo[i] < min_n:  # 代表头结点
                    min_n = distTo[i]
                    v = i
        if v == maxsize:
            wcb = True
            break
        collected[v] = True
        for i in range(0, n):
            if (collected[i] == False) and (distTo[v] + mat[v][i] < distTo[i]):  # 更新最短距离
                parent[i] = v
                distTo[i] = distTo[v] + mat[v][i]
    e = end
    while e != -1:  # 利用parent-v继承关系，循环回溯更新path并输出
        path.append(e)
        e = parent[e]
    path.append(begin)
    path.reverse()
    if wcb == True or distTo[end] >= maxsize:
        bkd = True
    return path, distTo[end], bkd


def calcShortestPath(G, word1, word2, verbose):
    # 从G中提取节点和邻接矩阵
    node, matrix = G
    # 检查word1和word2是否在节点列表中
    if word1 not in node and word2 in node:
        if verbose: print(f"No “{word1}” in the graph!")
        return []
    elif word2 not in node and word1 in node:
        if verbose: print(f"No “{word2}” in the graph!")
        return []
    elif word1 not in node and word2 not in node:
        if verbose: print(f"No “{word1}” and “{word2}” in the graph!")
        return []
    # 获取word1和word2在节点列表中的索引
    index1 = node.index(word1)
    index2 = node.index(word2)
    path, distance, bkd = dijkstra(matrix, index1, index2)
    if bkd == False:
        print("最短路径：")
        for idx in path:
            print("->" + node[idx])
        print("最短路径长度：")
        print(distance)
    else:
        print("不可达")


def randomWalk(G):
    # 从G中提取节点和邻接矩阵
    node, matrix = G
    visted = matrix.copy()  # 防止matrix数组被修改
    start = node.index(np.random.choice(node))  # 出发点
    visitpath = [start] # 记录随机遍历过程
    str = ''

    while True:
        next = []
        # 从出边的几个中随机选择
        for i in range(0, len(matrix)):
            if matrix[start][i] > 0:
                next.append(i)
        if not next: #无出边
            for idx in visitpath:
                str = str + node[idx] + ' '
            with open('outtest.txt', 'w') as fout:
                fout.write(str)
            print(str)
            break
        nextnode = np.random.choice(next)
        visitpath.append(nextnode)
        # 记录每条边被访问次数, 小于零说明访问两次
        visted[start][nextnode]=visted[start][nextnode]-1
        if visted[start][nextnode] == -1:
            for idx in visitpath:
                str = str + node[idx] + ' '
            with open('outtest.txt', 'w') as fout:
                fout.write(str)
            print(str)
            break
        start = nextnode




if __name__ == '__main__':
    # 读取文本文件
    with open('test.txt') as file:
        read_data = file.read()
    # 将文本转换为小写
    rl = read_data.lower()
    # 去除标点符号
    s = ''
    for i in range(0, len(rl)):
        if rl[i] >= 'a' and rl[i] <= 'z':
            s = s + rl[i]
        else:
            s = s + ' '
    # 将字符串分割为单词
    str = s.split()
    node = []  # 结点对应单词的列表
    # 生成结点对应单词的列表
    for i in range(0, len(str)):
        if str[i] not in node:
            node.append(str[i])
    # 初始化邻接矩阵
    matrix = np.zeros((len(node), len(node)), dtype=int)
    # matrix = [[0 for _ in range(len(node))] for _ in range(len(node))] 不调用numpy库的方法
    # 生成边的权重
    for i in range(0, len(str) - 1):
        x = node.index(str[i])  # index()方法返回元素在列表中的位置
        y = node.index(str[i + 1])
        matrix[x][y] = matrix[x][y] + 1
    G = (node, matrix)  # 有向图用结点和邻接矩阵组成的二元组表示

    while True:
        user_input = input(
            "请输入你的选择 (1: 绘制有向图, 2: 查询桥接词, 3: 插入桥接词, 4: 寻找最短路径, 5:随机遍历, q: 退出程序): ")
        if user_input == '1':
            displayMatrix(G)  # 绘制邻接矩阵
            showDirectedGraph(G)  # 绘制并保存有向图
        elif user_input == '2':
            word1 = input("请输入第一个单词: ")
            word2 = input("请输入第二个单词: ")
            # bridge_words = queryBridgeWords(G, "new", "and", True)
            bridge_words = queryBridgeWords(G, word1, word2, True)  # 查询桥接词
        elif user_input == '3':
            # text = "Seek to explore new and exciting synergies"
            text = input("请输入你想要插入桥接词的文本: ")
            new_text = generateNewText(G, text)  # 插入桥接词
        elif user_input == '4':
            word1 = input("请输入第一个单词: ")
            word2 = input("请输入第二个单词: ")
            calcShortestPath(G, word1, word2, True)
        elif user_input == '5':
            randomWalk(G) # 随机遍历
        elif user_input.lower() == 'q':
            break  # 退出程序
        else:
            print("无效的输入!")
