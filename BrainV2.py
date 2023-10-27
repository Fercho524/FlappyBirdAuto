import numpy as np
import random

def sigmoid(x):
    return 1 / (1 + np.e**(-np.float128(x)))

def relu(x):
    return max(0,x)
    
def random_weights(structure):
    weights = []
    for i in range(1,len(structure)):
        weights.append(np.random.uniform(-1, 1, (structure[i-1], structure[i])))
    return weights

class Brain():
    def __init__(self, structure, weights):    
        self.weights = random_weights(structure) if len(weights) == 0 else weights

    def predict(self,enviroment):
        results = enviroment
        for w_m in self.weights:
            h = []
            for w_i in range(w_m.shape[1]):
                h.append(sigmoid(np.dot(w_m[:,w_i], results)))
            results = h

        return results[0]