# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 21:58:34 2018

@author: huang
"""

class Array(object):
    def __init__(self,capacity,fillValue = None):
        self._items = list()
        for count in range(capacity):
            self._items.append(fillValue)
    
    def __len__(self):
        return len(self._items)
    
    def __str__(self):
        '''
        Array可以被print()打印出来
        '''
        return str(self._items)
    
    def __iter__(self):
        '''
        Array可以被迭代
        '''
        return iter(self._items)
    
    def __getitem__(self,index):
        '''
        Array可以通过下标得到值
        '''
        return self._items[index]
    
    def __setitem__(self,index,newItem):
        '''
        Array可以通过下标设置值
        '''
        self._items[index] = newItem


    
    
    
    
    
    