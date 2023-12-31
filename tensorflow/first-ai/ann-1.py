import os
from keras.src.optimizers import SGD
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf
import keras
import keras.losses as loss
import numpy as np
import numpy.random as rand
from simtools import bfs_tree_step, rand_matrix, get_sign, bfs_closest_tree, bfs_next_dir
####### CONSTANTS #######
MATRIX_SIZE=9 # 5
INPUT_NUM = MATRIX_SIZE*MATRIX_SIZE
INPUT_RANGE = [0,1]
OUTPUT_NUM=5
MAX_TREES=4
EPOCHS=80
TRAIN_SAMPLES=400
TEST_SAMPLES=200
PLOT=False


# Set wrapper function to check if duplicated
def do_add(s, x):
  l = len(s)
  s.add(x)
  return len(s) != l

# Data geneator. Data should be splitted in train/test/CrossValid
def generate_data(samples):
    data = []#np.zeros((samples,INPUT_NUM),dtype=int)
    data_set = set()
    solutions = []
    indx=0
    while(indx <samples):
        ntrees = rand.randint(1, MAX_TREES)
        m1 = rand_matrix(MATRIX_SIZE, ntrees)
        sol= bfs_next_dir(m1)
        #print(np.reshape(m1,(-1,1)))
        if(do_add(data_set,tuple(m1.reshape(1,-1)[0]))==True):
            data.append(m1.reshape(1,-1)[0])
            solutions.append(sol)
            indx+=1
    print("Generated data len:", len (data))
    return np.array(data), np.array(solutions)

# Function to test bfs algorithm
def test_best_solution_function():
    m_size=9
    samples=3
    m1 = rand_matrix(m_size,samples, True)
    print(m1)
    print("bfs_tree_step: ",bfs_tree_step(m1))
    t_pos=bfs_closest_tree(m1)
    print("sel_tree_x: "+str(t_pos[1]))
    print("sel_tree_y: "+str(t_pos[0]))
    s=bfs_next_dir(m1)#best_solution(t_pos[1],t_pos[0],p_pos,p_pos)
    ny,nx= bfs_tree_step(m1)[-2]
    print("Next tile {}, {}".format(ny,nx))
    print("Class : ", s)
    #print(np.reshape(m1.reshape(1,-1)[0],(m_size,m_size) ))



class_names = ['x', '-x', 'y', '-y', 'pick']

# Define Sequential model with 3 layers
model = keras.Sequential(
    [
        keras.layers.Dense(units=INPUT_NUM, activation="relu", name="layer1"),
#       keras.layers.Dense(int(INPUT_NUM/3), activation="relu", name="layer2"),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(units=OUTPUT_NUM,activation="Softmax", name="layer3"),
    ]
)
model.compile(optimizer='adam',
              loss=loss.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])



#test_best_solution_function()

data, sol = generate_data(TEST_SAMPLES+TRAIN_SAMPLES)
#data, sol=gen_train_data(TRAINING_SAMPLES)
train_sol = sol[:TRAIN_SAMPLES]
train_data = data[:TRAIN_SAMPLES]
model.fit(train_data,train_sol, epochs=EPOCHS)
# Simulate network(predicting)
model.summary()
test_data = data[TRAIN_SAMPLES:TRAIN_SAMPLES+TEST_SAMPLES]     
test_sol= sol[TRAIN_SAMPLES:TRAIN_SAMPLES+TEST_SAMPLES]
test_loss, test_acc = model.evaluate(test_data,  test_sol)
predicted_value = model.predict(test_data)
indx = 0
float_formatter = "{:.3f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})
print("Number of training samples: ", len(train_sol))
print("Number of test samples: ", len(test_data))
print(class_names)
print(predicted_value[:10])

#for prediction, data, sol in  zip(predicted_value, test_data, sol): 
    
    #norm_prediction=np.array(sol_norm(prediction))
    #
    #if (sol==[0,0,0]).all() and not (norm_prediction==[0,0,1]).all():
    #    correct+=1
    #elif (norm_prediction==sol).all():
    #    correct+=1
    #else:
    #    print("Predicted[{}]: {}".format(indx,prediction))
    #    print("Sol[{}]: {}".format(indx,sol) )
    #indx +=1     

model.save("min_dist.keras")
new_model = keras.models.load_model("min_dist.keras")
new_model.summary()
