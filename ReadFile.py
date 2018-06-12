#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/12 20:35
# @Author  : nkuhjp
# @Site    : 
# @File    : ReadFile.py
# @Software: PyCharm Community Edition

class ReadFile():
    def __init__(self):
        self.nodes_list = [] # 存储所有节点
        self.nodes_num = 0 # 节点总数
        self.dead_nodes_num = 0 # 死节点数
        self.edges_num = 0 # 链接数
        self.block_num = 15 # 块数
        self.node_id = dict() # 存储node真实id和索引id

    def create_file(self, block_num=15):
        """创建block_num个文件，用来存储块"""
        for block in range(block_num):
            filename = 'prblock' + str(block_num) + '_' + str(block) + '.txt'
            with open(filename, 'w') as f:
                f.write('')

    def get_statistics(self, filename='WikiData.txt'):
        """第一次读取文件获取基本信息"""
        if filename.strip() == '':
            filename = 'WikiData.txt'
        nodes_set = set() # 所有节点
        live_nodes_set = set() # 非dead node，即有出度的node
        edges = 0 # 链接总数
        with open(filename, 'r') as f:
            line = f.readline().strip()
            while line != '':
                src_node, dst_node = [int(node) for node in line.split('\t')]
                nodes_set.add(src_node)
                nodes_set.add(dst_node)
                live_nodes_set.add(src_node)
                edges += 1
                line = f.readline().strip()
        self.nodes_num = len(nodes_set) # 7115
        self.dead_nodes_num = len(nodes_set) - len(live_nodes_set) # 1005
        self.edges_num = edges # 103689
        print('节点总数 ', self.nodes_num, ', 死节点数 ', self.dead_nodes_num, ', 链接数 ', self.edges_num)
        self.sort_nodes(nodes_set)

    def sort_nodes(self, nodes_set=dict()):
        """对节点排序，将node与id对应"""
        self.nodes_list = list(nodes_set)
        nodes = sorted(self.nodes_list)
        for i in range(len(nodes)):
            self.node_id[nodes[i]] = i

    def write_block(self, node_dst=dict()):
        """将src,degree,destination逐行写入block中"""
        # 计算块大小
        block_size = self.nodes_num // self.block_num + 1
        for node in node_dst:
            dst_nodes = node_dst[node]
            line_nodes = []
            index = 0 # 当前行应该存在哪个
            for dst_node in dst_nodes:
                order = self.node_id[dst_node]
                if index != (order // block_size):
                    if len(line_nodes) != 0:
                        self.write_line(index, node, len(dst_nodes), line_nodes)
                    line_nodes = []
                index = order // block_size
                line_nodes.append(dst_node)
            self.write_line(index, node, len(dst_nodes), line_nodes)
            if node % 100 == 0:
                print('节点', node, '完成')

    def write_line(self, index, src_node, degree, line_nodes=[]):
        """将src,degree,destination一行写入对应block"""
        filename = 'prblock' + str(self.block_num) + '_' + str(index) + '.txt'
        with open(filename, 'a') as f:
            f.write(str(src_node) + ' ' + str(degree) + ' ')
            for node in line_nodes:
                f.write(str(node) + ' ')
            f.write('\n')

    def read_file(self, filename='WikiData.txt', block_num=15):
        """读取文件，并将数据分成block_num块"""
        if filename.strip() == '':
            filename = 'WikiData.txt'
        self.block_num = block_num
        # 创建block_num个块
        self.create_file(block_num)

        node_dst = dict() # 存储一个节点及其指向的节点
        with open(filename, 'r') as f:
            line = f.readline().strip()
            while line != '':
                src_node, dst_node = [int(node) for node in line.split('\t')]
                if src_node in node_dst:
                    node_dst[src_node].append(dst_node)
                else:
                    node_dst[src_node] = [dst_node]
                line = f.readline().strip()
        self.write_block(node_dst)

    def get_nodeId(self):
        """返回node_id"""
        return self.node_id

    def get_nodeNumber(self):
        """返回Node数"""
        return self.nodes_num

    def get_nodeList(self):
        """返回nodes_list"""
        return self.nodes_list

    def get_blockNumber(self):
        """返回block_num"""
        return self.block_num