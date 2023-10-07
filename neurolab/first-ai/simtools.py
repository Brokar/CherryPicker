import numpy as np
import neurolab as nl
from numpy.core.fromnumeric import reshape
import numpy.random as rand
import math
import pylab as pl



def rand_matrix(size, valid_samples, vervose=False):
    """
    Creates a square matrix with 1s in random positions. 
    size is m: m x m
    valid_sampels: number of ones
    """
    matrix = np.zeros((size, size), dtype=int)
    i = 0
    while i < valid_samples:
        x = rand.randint(0, size-1)
        y = rand.randint(0, size-1)
        mid = int(size / 2)
        if (matrix[y,x] == 1) or ((x == mid and y == mid)):
            pass
        else:
            if vervose:
                print("Inserting in x:"+str(x)+" y:"+str(y))
            matrix[y,x] = 1
            i+=1

    return matrix

def get_sign(number):
    """
    Returns 1 if the number is >= 0 and -1 in the rest 
    of the cases.
    """
    if (number>=0):
      return 1
    elif (number<0):
      return -1

def find_min_dist_one(matrix):
    """
    Returns the position of a 1 in the matrix that is 
    closest to the center of the matrix
    """
    mid = int(len(matrix) / 2)
    best_match = len(matrix)
    best_pos = [mid-1, mid-1]
    for row_idx, row in enumerate(matrix):
        for col_idx, is_tree in enumerate(row):
            if(is_tree):
                cr_match = math.dist([row_idx,col_idx],[mid,mid])
                if cr_match < best_match:
                    best_match = cr_match
                    best_pos = [row_idx, col_idx]
    return best_pos

