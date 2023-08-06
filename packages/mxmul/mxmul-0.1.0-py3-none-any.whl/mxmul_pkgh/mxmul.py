# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 23:20:39 2021

@author: 何晓辉
"""

def mxmul(mx1,mx2,nrow,nk,ncol):
    rst = [[0 for y in range(ncol)] for x in range(nrow)]
    for i in range(nrow):
        for j in range(ncol):
            for k in range(nk):
                rst[i][j] += mx1[i][k] * mx2[k][j]
    return rst

def mxsum(mx,nrow,ncol):
    s = 0
    for i in range(nrow):
        for j in range(ncol):
            s += mx[i][j]
    return s

if __name__ == "__main__":
    import time
    nrow,nk,ncol = 500,300,500
    mx1 = [[y for y in range(nk)] for x in range(nrow)]
    mx2 = [[y for y in range(ncol)] for x in range(nk)]
    start = time.perf_counter()
    rst = mxmul(mx1,mx2,nrow,nk,ncol)
    end = time.perf_counter()
    print("运算时间为{:.4f}s".format(end-start))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    