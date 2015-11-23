import pickle
import numpy as np
import theano

def get_training_data(tr_file):
    f = open(tr_file, 'r')
    tr_raw = pickle.load(f)
    f.close()
    move_teller = 0
    trX = [[]]
    trY = []
    for i in range(len(tr_raw)):
        if ((i+1)%17==0):
            trY.append(tr_raw[i])
            trX.append([])
            move_teller += 1
        else :
            trX[move_teller].append(tr_raw[i])
    trX = floatX(trX[:-1])
    #for i in range(len(trX)):
    #    trX[i] = trX[i]/max(trX[i])

    return trX/13., one_hot(trY,4)

def floatX(X):
    return np.asarray(X, dtype=theano.config.floatX)

def one_hot(x,n):
	if type(x) == list:
		x = np.array(x)
	x = x.flatten()
	o_h = np.zeros((len(x),n))
	o_h[np.arange(len(x)),x] = 1
	return o_h
