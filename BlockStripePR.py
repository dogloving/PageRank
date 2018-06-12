#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/12 22:57
# @Author  : nkuhjp
# @Site    : 
# @File    : BlockStripePR.py
# @Software: PyCharm Community Edition

class BlockStripePR():
    def __init__(self, node_id=dict(), nodes_num=0, nodes_list=[], block_num=15):
        self.beta = 0.85
        self.old_score = []
        self.new_score = []
        self.node_id = node_id # 存储node真实id和索引id
        self.nodes_num = nodes_num # 节点数
        self.nodes_list = nodes_list # 所有节点
        self.block_num = block_num # 块数
        # 令old_score所有node的score一样
        self.old_score = [1 / self.nodes_num] * self.nodes_num

    def pagerank(self, beta=0.85):
        """计算pagerank score"""
        self.beta = beta
        epsilon = 1.0e-6 # 当bias小于epsilon表示已经收敛
        inter_count = 0 # 迭代次数
        while True:
            self.calculate()
            # 计算bias
            bias = 0
            for i in range(self.nodes_num):
                bias += abs(self.old_score[i] - self.new_score[i])
            self.old_score = self.new_score
            if bias <= epsilon:
                break
            inter_count += 1
        print('迭代了', inter_count, '次，最后的误差为', bias)
        self.sort()

    def sort(self):
        """对结果根据score进行排序，并输出前100的值"""
        score_id = []
        for i in range(self.nodes_num):
            score_id.append((self.new_score[i], self.nodes_list[i]))
        score_id = sorted(score_id, reverse=True)
        with open('result.txt', 'w') as f:
            print('Top 100的页面ID和score分别为:')
            for i in range(self.nodes_num):
                if i < 100:
                    print(str(score_id[i][1]) + '\t' + str(score_id[i][0]))
                f.write(str(score_id[i][1]) + '\t' + str(score_id[i][0]) + '\n')

    def calculate(self):
        """一次迭代"""
        self.new_score = [0] * self.nodes_num
        # 读取文件，更新new_rank
        for i in range(self.block_num):
            filename = 'prblock' + str(self.block_num) + '_' + str(i) + '.txt'
            with open(filename, 'r') as f:
                line = f.readline().strip()
                while line != '':
                    nums = line.split(' ')
                    src_node, degree, dst_nodes = self.node_id[int(nums[0])], int(nums[1]), \
                                                  [self.node_id[int(x)] for x in nums[2:]]
                    for node in dst_nodes:
                        self.new_score[node] += self.beta * self.old_score[src_node] / degree
                    line = f.readline().strip()
        # 处理dead ends问题
        rank_sum = sum(self.new_score)
        for i in range(self.nodes_num):
            self.new_score[i] += (1 - rank_sum) / self.nodes_num
