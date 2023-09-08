from neurolab.error import MAE
import numpy as np
import neurolab as nl
from numpy.core.fromnumeric import reshape
import numpy.random as rand
import math
import pylab as pl
####### CONSTANTS #######
MATRIX_SIZE=5 # 5
INPUT_NUM = MATRIX_SIZE*MATRIX_SIZE
INPUT_RANGE = [0,1]
TREES=1
TRAINING_SAMPLES=10


def rand_matrix(size, valid_samples, vervose=False):
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
   if (number>=0):
      return 1
   elif (number<0):
      return -1

def find_best_tree(matrix):
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

def best_solution(x,y,xo,yo):
    x_dist=abs(x-xo)
    y_dist=abs(y-yo)
    x_sign=get_sign(x-xo)
    y_sign=get_sign(y-yo)
    if x_dist==y_dist:
        values=[[y_sign,0],[0,x_sign]]
        dir = values[rand.choice([0,1])]
    elif x_dist+y_dist == 1:
        # we don't need to get closer
        dir = [0,0]
    elif x_dist < y_dist:
        dir = [y_sign,0]
    else:
        dir = [0, x_sign]
    return dir



def create_input_layer(num, rng):
    input_layer=[]
    for i in range(0,num): 
        input_layer.append(rng)
    return input_layer

def gen_train_data(samples):
    data = ([],[])
    for _ in range(samples):
        m1 = rand_matrix(MATRIX_SIZE,TREES)
        t_pos=find_best_tree(m1)
        p_pos = int(len(m1)/2)
        sol=best_solution(t_pos[1],t_pos[0],p_pos,p_pos)
        #print(np.reshape(m1,(-1,1)))
        data[0].append(m1.reshape(1,-1)[0])
        data[1].append(np.reshape(sol,(1,-1))[0])
    return data

# Function to test solution
def test_functions():
    m_size=9
    samples=3
    m1 = rand_matrix(m_size,samples, True)
    print(m1)
    t_pos=find_best_tree(m1)
    print("sel_tree_x: "+str(t_pos[1]))
    print("sel_tree_y: "+str(t_pos[0]))
    p_pos = int(len(m1)/2)
    s=best_solution(t_pos[1],t_pos[0],p_pos,p_pos)
    print("sol_x: "+str(s[1]))
    print("sol_y: "+str(s[0]))
    #print(np.reshape(m1.reshape(1,-1)[0],(m_size,m_size) ))
# Create network with 1 hidden layer and random initialized
#nl.net.newff() is feed forward neural network
#1st argument is min max values of predictor variables
#2nd argument is no.of nodes in each layer i.e 4 in hidden 1 in o/p
#transf is transfer function applied in each layer
def sol_norm(input):
    x=input[1]
    y=input[0]
    x_sign=get_sign(x)
    y_sign=get_sign(y)
    if x==y:
        values=[[x_sign,0],[0,y_sign]]
        dir = values[rand.choice([0,1])]
    elif x > y:
        dir = [0, x_sign]
    else:
        dir = [y_sign, 0]
    return dir



input_layer = create_input_layer(INPUT_NUM,INPUT_RANGE)
#print("input layer " + str(input_layer))
neural_net = nl.net.newff( input_layer,[16,2])
test_functions()

data=gen_train_data(100)
#print(np.array(data[0]))
error = []
error.append(neural_net.train(np.array(data[0]), np.array(data[1]), epochs = 3000, show = 0, goal=0.00001))
print("Final error: ", error[0][-1])
#plotting epoches Vs error
#we can use this plot to specify the no.of epoaches in training to reduce time
pl.figure(1)
pl.plot(error[0])
pl.xlabel('Number of epochs')
pl.ylabel('Training error')
pl.grid()
pl.show()

# Simulate network(predicting)
new_data = gen_train_data(50)
for input, sol in  zip(*new_data):
    #print(input)
    predicted_values = neural_net.sim([np.array(input)])
    print("Predicted " + "[{:.3f}".format(predicted_values[0][0])+" {:.3f}]".format(predicted_values[0][1]) +" vs sol "+ str(sol))
#    print("Predicted " + "[{:.3f}".format(predicted_values[0][0])+" {:.3f}]".format(predicted_values[0][1]) +" in:")
    print("In: \n"+str(np.reshape(input,(MATRIX_SIZE,MATRIX_SIZE))))

