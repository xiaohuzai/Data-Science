# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 20:58:57 2018

@author: huang
"""


"""
搜索算法
"""

def indexOfMin(lyst):
    '''
    Return the index of the minimum item.
    '''
    minIndex = 0
    currentIndex = 1
    while currentIndex < len(lyst):
        if lyst[currentIndex]<lyst[minIndex]:
            minIndex = currentIndex
        currentIndex += 1
    return minIndex

def sequentialSearch(target,lyst):
    '''
    Return the position of the target item if found,
    or -1 otherwise
    '''
    position = 0
    while position<len(lyst):
        if target == lyst[position]:
            return position
        position += 1
    return -1

def binarySearch(target,sortedLyst):
    '''
    二叉搜索
    '''
    left = 0
    right = len(sortedLyst)-1
    while left<=right:
        midpoint = (left + right)//2
        if target == sortedLyst[midpoint]:
            return midpoint
        elif target < sortedLyst[midpoint]:
            right = midpoint-1
        else:
            left = midpoint+1
    return -1

"""
排序算法
"""

def swap(lyst,i,j):
    '''
    Exchange the items at position i and j
    '''
    temp = lyst[i]
    lyst[i] = lyst[j]
    lyst[j] = temp
    
def selectionSort(lyst):
    '''
    选择排序，找到最小值，将其排到最前
    n2
    '''
    i = 0
    while i < len(lyst)-1:
        minIndex = i
        j = i+1
        while j <len(lyst):
            if lyst[j] < lyst[minIndex]:
                minIndex = j
            j += 1
        if minIndex != i:
            swap(lyst,minIndex,i)
        i += 1

def bubbleSort(lyst):
    '''
    冒泡排序，两两交换
    '''
    n = len(lyst)
    while n > 1:
        i = 1
        while i < n:
            if lyst[i] <lyst[i-1]:
                swap(lyst,i,i-1)
            i += 1
        n -= 1

def bubbleSortWithTweak(lyst):
    '''
    冒泡排序，改良版
    ''' 
    n = len(lyst)
    while n > 1:
        swapped = False
        i = 1
        while i < n:
            if lyst[i] <lyst[i-1]:
                swap(lyst,i,i-1)
                swapped = True
            i += 1
        if not swapped:
            return
        n -=1

def insertionSort(lyst):
    i = 1
    while i < len(lyst):
        itemToInsert = lyst[i]
        j = i-1
        while j > 0:
            if itemToInsert < lyst[j]:
                lyst[j+1] = lyst[j]
                j -= 1
            else:
                break
        lyst[j+1] = itemToInsert
        i += 1

'''
快速排序
'''
def partition(lyst,left,right):
    middle = (left+right)//2
    pivot = lyst[middle]
    lyst[middle] = lyst[right]
    lyst[right] = pivot
    boundary = left
    for index in range(left,right):
        if lyst[index] < pivot:
            swap(lyst,index,boundary)
            boundary += 1
    swap(lyst,right,boundary)
    return boundary

def quicksort(lyst,left,right):
    if left < right:
        pivoLocation = partition(lyst,left,right)
        quicksort(lyst,left,pivoLocation)
        quicksort(lyst,pivoLocation+1,right)

    
    
    
    
    
    
            
    
    
    
    
    
    