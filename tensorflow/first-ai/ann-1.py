import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf
import keras
import keras.losses as loss
import numpy as np
from numpy.core.fromnumeric import reshape
import numpy.random as rand
import math
import pylab as pl
from simtools import rand_matrix, get_sign, find_min_dist_one
####### CONSTANTS #######
MATRIX_SIZE=9 # 5
INPUT_NUM = MATRIX_SIZE*MATRIX_SIZE
INPUT_RANGE = [0,1]
OUTPUT_NUM=3
TREES=3
TRAINING_SAMPLES=200
TEST_SAMPLES=200
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
            #values=[[y_sign,0,0],[0,x_sign,0]]
            #dir = values[rand.choice([0,1])]
            dir=[y_sign,0,0]
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
    for _ in range(0,num): 
        input_layer.append(rng)
    return input_layer

def gen_train_data(samples):
    data = np.zeros((samples,INPUT_NUM),dtype=int)
    solutions = np.zeros((samples,OUTPUT_NUM), dtype=int)
    for i in range(samples):
        m1 = rand_matrix(MATRIX_SIZE,TREES)
        t_pos=find_min_dist_one(m1)
        p_pos = int(len(m1)/2)
        sol=best_solution(t_pos[1],t_pos[0],p_pos,p_pos)
        #print(np.reshape(m1,(-1,1)))
        data[i,:]=m1.reshape(1,-1)[0]
        solutions[i,:] = sol
    return data, solutions

def gen_test_data(samples):
    data = np.zeros((samples,INPUT_NUM),dtype=int)
    solutions = np.zeros((samples,OUTPUT_NUM), dtype=int)
    for i in range(samples):
        m1 = rand_matrix(MATRIX_SIZE,TREES)
        t_pos=find_min_dist_one(m1)
        p_pos = int(len(m1)/2)
        sol=best_solution(t_pos[1],t_pos[0],p_pos,p_pos, True)
        #print(np.reshape(m1,(-1,1)))
        data[i,:]=m1.reshape(1,-1)[0]
        solutions[i,:] = sol
    return data, solutions

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
# Define Sequential model with 3 layers
model = keras.Sequential(
    [
       keras.layers.Dense(units=INPUT_NUM, activation="relu", name="layer1"),
       keras.layers.Dense(int(INPUT_NUM/3), activation="tanh", name="layer2"),
       keras.layers.Dense(units=OUTPUT_NUM, activation="tanh", name="layer3"),
    ]
)
model.compile(optimizer='adam',
              loss=loss.MeanSquaredError(),
              metrics=['accuracy'])



#test_best_solution_function()

data, sol=gen_train_data(TRAINING_SAMPLES)
model.fit(data,sol, epochs=1000)
# Simulate network(predicting)
model.summary()
correct=0
test_data, sol = gen_test_data(TEST_SAMPLES)
predicted_value = model.predict(test_data)
indx = 0
for prediction, data, sol in  zip(predicted_value, test_data, sol): 
    norm_prediction=np.array(sol_norm(prediction))
    
    if (sol==[0,0,0]).all() and not (norm_prediction==[0,0,1]).all():
        correct+=1
    elif (norm_prediction==sol).all():
        correct+=1
   # else:
   #     print("Predicted[{}]: {}".format(indx,norm_prediction))
   #     print("Data[{}]: {}".format(indx,data) )
    indx +=1     
print("Accuracy: ", correct/TEST_SAMPLES)
print("Correct: ", correct)

model.save("min_dist.keras")
