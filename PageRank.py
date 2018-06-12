#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/12 20:36
# @Author  : nkuhjp
# @Site    : 
# @File    : PageRank.py
# @Software: PyCharm Community Edition

import time
from ReadFile import ReadFile
from BlockStripePR import BlockStripePR

if __name__ == '__main__':
    # 读取文件并分块
    start_time = time.time()
    readFile = ReadFile()
    readFile.get_statistics()
    filename = input('输入要读取的文件名(默认为WikiData.txt):')
    block_num = input('输入要划分的块(默认为15):')
    if not block_num.isdigit() or int(block_num) <= 0:
        block_num = 15
    readFile.read_file(filename, block_num)
    print('读取文件并分块用时: ', time.time()-start_time, '秒')

    # 根据前面的分块计算score
    start_time = time.time()
    blockStripePR = BlockStripePR(readFile.get_nodeId(), readFile.get_nodeNumber(),
                                  readFile.get_nodeList(), readFile.get_blockNumber())
    beta = input('输入beta值(在0.8~0.9之间选择，默认为0.85):')
    if not beta.isdigit() or int(beta) <= 0:
        beta = 15
    blockStripePR.pagerank(beta)
    print('计算pagerank score用时: ', time.time() - start_time, '秒')
