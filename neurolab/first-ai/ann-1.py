from neurolab.error import MAE
import numpy as np
import neurolab as nl
from numpy.core.fromnumeric import reshape
import numpy.random as rand
import math
import pylab as pl
from simtools import rand_matrix, get_sign, find_min_dist_one

####### CONSTANTS #######
MATRIX_SIZE=7 # 5
INPUT_NUM = MATRIX_SIZE*MATRIX_SIZE
INPUT_RANGE = [0,1]
TREES=3
TRAINING_SAMPLES=100
TEST_SAMPLES=100
PLOT=False


def best_solution(x,y,xo,yo, no_rand=False):
    x_dist=abs(x-xo)
    y_dist=abs(y-yo)
    x_sign=get_sign(x-xo)
    y_sign=get_sign(y-yo)
    if x_dist==y_dist:
        if no_rand:
            dir=[0,0,0]
        else:
            values=[[y_sign,0,0],[0,x_sign,0]]
            dir = values[rand.choice([0,1])]
    elif x_dist+y_dist == 1:
        # we don't need to get closer
        dir = [0,0,1]
    elif x_dist < y_dist:
        dir = [y_sign,0,0]
    else:
        dir = [0, x_sign,0]
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
        t_pos=find_min_dist_one(m1)
        p_pos = int(len(m1)/2)
        sol=best_solution(t_pos[1],t_pos[0],p_pos,p_pos)
        #print(np.reshape(m1,(-1,1)))
        data[0].append(m1.reshape(1,-1)[0])
        data[1].append(np.reshape(sol,(1,-1))[0])
    return data

def gen_test_data(samples):
    data = ([],[])
    for _ in range(samples):
        m1 = rand_matrix(MATRIX_SIZE,TREES)
        t_pos=find_min_dist_one(m1)
        p_pos = int(len(m1)/2)
        sol=best_solution(t_pos[1],t_pos[0],p_pos,p_pos, True)
        #print(np.reshape(m1,(-1,1)))
        data[0].append(m1.reshape(1,-1)[0])
        data[1].append(np.reshape(sol,(1,-1))[0])
    return data

# Function to test best_solution function
def test_best_solution_function():
    m_size=7
    samples=3
    m1 = rand_matrix(m_size,samples, True)
    print(m1)
    t_pos=find_min_dist_one(m1)
    print("sel_tree_x: "+str(t_pos[1]))
    print("sel_tree_y: "+str(t_pos[0]))
    p_pos = int(len(m1)/2)
    s=best_solution(t_pos[1],t_pos[0],p_pos,p_pos)
    print("sol_x: "+str(s[1]))
    print("sol_y: "+str(s[0]))
    print("pick : "+str(s[2]))
    #print(np.reshape(m1.reshape(1,-1)[0],(m_size,m_size) ))
# Create network with 1 hidden layer and random initialized
#nl.net.newff() is feed forward neural network
#1st argument is min max values of predictor variables
#2nd argument is no.of nodes in each layer i.e 4 in hidden 1 in o/p
#transf is transfer function applied in each layer
def sol_norm(input):

    x=abs(input[1])
    y=abs(input[0])
    pick=abs(input[2])
    x_sign=get_sign(input[1])
    y_sign=get_sign(input[0])

    if pick > x and pick > y:
        dir = [0,0,1]
    elif x==y:
        values=[[x_sign,0,0],[0,y_sign,0]]
        dir = values[rand.choice([0,1])]
    elif x > y:
        dir = [0, x_sign,0]
    else:
        dir = [y_sign, 0,0]
    return dir


input_layer = create_input_layer(INPUT_NUM,INPUT_RANGE)
# output is 2 for direction and 1 for picking up tree
neural_net = nl.net.newff( input_layer,[16,3])

#test_best_solution_function()

data=gen_train_data(100)

error = []
error.append(neural_net.train(np.array(data[0]), np.array(data[1]), epochs = 3000, show = 0, goal=0.00001))
print("Final error: ", error[0][-1])
#plotting epoches Vs error
#we can use this plot to specify the no.of epoaches in training to reduce time
if PLOT:
    pl.figure(1)
    pl.plot(error[0])
    pl.xlabel('Number of epochs')
    pl.ylabel('Training error')
    pl.grid()
    pl.show()

# Simulate network(predicting)
correct=0
new_data = gen_test_data(TEST_SAMPLES)
for input, sol in  zip(*new_data):
    #print(input)
    predicted_value = neural_net.sim([np.array(input)])
    norm_prediction=np.array(sol_norm(predicted_value[0]))
    predicted_value=predicted_value[0]
    if (sol==[0,0,0]).all() and not (norm_prediction==[0,0,1]).all():
        correct+=1
    elif (norm_prediction==sol).all():
        correct+=1
    #print("Predicted " + "[{:.3f}".format(predicted_value[0])+" {:.3f}".format(predicted_value[1])+" {:.3f}]".format(predicted_value[2]) +" vs good sol "+ str(sol) + " in:")
    #print("Predicted " +str(norm_prediction)+" vs good sol "+ str(sol) + " in:")
    #print(str(np.reshape(input,(MATRIX_SIZE,MATRIX_SIZE))))
print("Accuracy: ", correct/TEST_SAMPLES)
print("Correct: ", correct)
for idx,layer in enumerate(neural_net.layers):
    np.savetxt("layer_{}_w.csv".format(idx), layer.np['w'], delimiter=",") 
    np.savetxt("layer_{}_b.csv".format(idx), layer.np['b'], delimiter=",") 
    # print("layer {} has {} inputs and {} outputs".format(idx, layer.ci, layer.co))
   # print("layer {} np[w] {}".format(idx, layer.np['w']))
   # print("layer {} np[b] {}".format(idx, layer.np['b']))
