import numpy as np
import random as random

def initialise_map (layer,lenght,height,number_of_cherries):
    #layer1=terrain,layer2=player1,layer3=bot
    map=np.zeros((layer,lenght,height))
    #player and bot are placed in the middle of theon top and bottom of map
    map[1,int(lenght/2),0]=1
    map[2,int(lenght/2),-1]=1
    x_sample=random.sample(range(lenght),number_of_cherries)
    y_sample=random.sample(range(height),number_of_cherries)
    for sample_number in range (number_of_cherries):
        map[0,x_sample[sample_number],y_sample[sample_number]]=1
    return map


print (initialise_map(3,5,5,3))
