import numpy as np
import neurolab as nl
import numpy.random as rand
import math
####### CONSTANTS #######
MATRIX_SIZE=5
INPUT_NUM = MATRIX_SIZE-1
INPUT_RANGE = [0,1]
TREES=2
TRAINING_SAMPLES=10


def rand_matrix(size, valid_samples):
    matrix = np.zeros((size, size))
    for i in range (valid_samples):
        x = rand.randint(0, size-1)
        y = rand.randint(0, size-1)
        mid = size / 2
        if (matrix[x,y] == 1) or ((x == mid and y == mid)):
            i-=1
        else:
            matrix[x,y] = 1

    return matrix
def get_sign(number):
   if (number>0):
      return 1
   elif (number<0):
      return -1
   else:
      return 0

def find_best_tree(matrix):
    mid = len(matrix) / 2
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

def best_solution(x,y,xo,yo):
    x_dist=abs(x-xo)
    y_dist=abs(y-yo)
    x_sign=get_sign(y-yo)
    y_sign=get_sign(x-xo)
    if x_dist==y_dist:
        values=[[x_sign,0],[0,y_sign]]
        dir = values[rand.choice([0,1])]
    elif x_dist < y_dist:
        dir = [0, y_sign]
    else:
        dir = [x_sign,0]
    return dir



def create_input_layer(num, rng):
    input_layer=[]
    for i in range(0,num): 
        input_layer.append(rng)
    print(input_layer)
    return input_layer
# Create network with 1 hidden layer and random initialized
#nl.net.newff() is feed forward neural network
#1st argument is min max values of predictor variables
#2nd argument is no.of nodes in each layer i.e 4 in hidden 1 in o/p
#transf is transfer function applied in each layer
input_layer = create_input_layer(INPUT_NUM,INPUT_RANGE)
net = nl.net.newff( input_layer,[6,2])
m1 = rand_matrix(MATRIX_SIZE,2)
print(m1)
t_pos=find_best_tree(m1)
s=best_solution(t_pos[0],t_pos[1],len(m1)/2,len(m1)/2)
print(s)


