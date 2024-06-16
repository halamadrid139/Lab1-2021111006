import unittest
import numpy as np
from qBW import queryBridgeWords as qB

class MyTestCase(unittest.TestCase):
    def setUp(self):
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
        self.G = (node, matrix)  # 有向图用结点和邻接矩阵组成的二元组表示

    def test_1(self):
        qBlist, warn=qB(self.G, 'work', 'hard')
        self.assertEqual(warn, 'No “work” and “hard” in the graph!')

    def test_2(self):
        qBlist, warn=qB(self.G, 'seek', 'civilizations')
        self.assertEqual(warn, 'No bridge words from seek to civilizations!')

    def test_3(self):
        qBlist, warn=qB(self.G, 'seek', 'civilizations')
        self.assertEqual(warn, 'No bridge words from seek to civilizations!')

    def test_4(self):
        qBlist, warn=qB(self.G, 'seek', 'new')
        self.assertEqual(warn, 'The bridge word from seek to new is: out.')

if __name__ == '__main__':
    unittest.main()
