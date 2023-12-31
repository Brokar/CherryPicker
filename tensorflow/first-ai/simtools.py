from os import path
import numpy as np
import numpy.random as rand
import math



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

def adjacents_idnx(matrix, pos):
    """
    Returns a valid adjecent list of positions 
    from the matrix, excluding borders and pos 
    """
    adj_l = []
    # Ranges shall be used if we would allow 
    # diagonal moves
    for i in [pos[0]-1, pos[0]+1]:
        if(i>0 and i < len(matrix)): 
                adj_l.append((i,pos[1]))
    for j in [pos[1]-1, pos[1]+1]:
        if(j >0 and j <len(matrix)):
            adj_l.append((pos[0],j))
    return adj_l

def reverse_bfs(pred, target):
    """
    Reverse the pred matrix from the target 
    and return the shortest path
    """
    # Adding ending node
    path =[target]
    while (pred[target[0],target[1]] != 0):
        path.append(pred[target[0],target[1]])
        target = pred[target[0],target[1]]
    return path

def bfs_tree_step(matrix):
    """
    Returns a list of steps to the closest
    tree
    """
    m_size = len(matrix)
    mid = int(m_size / 2)
    visited = np.zeros((m_size,m_size), dtype=bool)
    pred = np.zeros((m_size,m_size), dtype=object)
    queue = []
    # Mark mid as visited and put queued
    queue.append((mid,mid))
    visited[mid,mid] = True
    while queue:
        s = queue.pop(0)
        for cell in adjacents_idnx(matrix, s):
            if visited[cell[0],cell[1]] == False:
                queue.append(cell)
                visited[cell[0],cell[1]] = True
                pred[cell[0],cell[1]] = s
                if(matrix[cell[0],cell[1]] == 1):
                    # tree found
                    return reverse_bfs(pred, cell)
    # Nothing found
    return [(mid,mid)]

def bfs_next_dir(matrix):
    path_t = bfs_tree_step(matrix)
    dir = 0
    if(len(path_t)<3):
        dir = 4
    else:
        if(path_t[-2][0]-path_t[-1][0]>0):
            dir=0
        elif(path_t[-2][0]-path_t[-1][0]<0):
            dir=1
        elif(path_t[-2][1]-path_t[-1][1]>0):
            dir=2
        elif(path_t[-2][1]-path_t[-1][1]<0):
            dir=3
    return dir

def bfs_closest_tree(matrix):
    """
    Returns the position of a 1 in the matrix that is 
    closest to the center of the matrix
    """
    m_size = len(matrix)
    mid = int(m_size / 2)
    visited = np.zeros((m_size,m_size), dtype=bool)
    queue = []
    # Mark mid as visited and put queued
    queue.append((mid,mid))
    visited[mid,mid] = True
    while queue:
        s = queue.pop(0)
        for cell in adjacents_idnx(matrix, s):
            if visited[cell[0],cell[1]] == False:
                queue.append(cell)
                visited[cell[0],cell[1]] = True
                if(matrix[cell[0],cell[1]] == 1):
                    # tree found
                    return [cell[1], cell[0]]
    return [mid,mid]

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

