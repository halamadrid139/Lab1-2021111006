def queryBridgeWords(G, word1, word2):
    # 从G中提取节点和邻接矩阵
    node, matrix = G
    # 检查word1和word2是否在节点列表中
    if word1 not in node and word2 in node:
        warn = f"No “{word1}” in the graph!"
        return [], warn
    elif word2 not in node and word1 in node:
        warn = f"No “{word2}” in the graph!"
        return [], warn
    elif word1 not in node and word2 not in node:
        warn = f"No “{word1}” and “{word2}” in the graph!"
        return [], warn
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
        warn = f"No bridge words from {word1} to {word2}!"
    else:
        # 如果桥接词列表只有一个元素，直接输出
        if len(bridge_words) == 1:
            warn = f"The bridge word from {word1} to {word2} is: {bridge_words[0]}."
        elif len(bridge_words) == 2:
            # 如果桥接词列表有两个元素，直接用"and"连接
            warn = f"The bridge words from {word1} to {word2} are: {bridge_words[0]} and {bridge_words[1]}."
        else:
            # 如果桥接词列表有三个或更多元素，使用逗号和"and"来连接
            warn = f"The bridge words from {word1} to {word2} are: {', '.join(bridge_words[:-1])} and {bridge_words[-1]}."
    return bridge_words, warn
