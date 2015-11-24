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
    #stripped training with number of empty
    trX_s = []

    for i in range(len(trX[:-1])):
        if max(trX[i])<12:
            trX_s.append(trX[i])

    for i in range(len(trX_s)):
        trX_s[i].append(trX_s[i].count(0))

    trX_s = floatX(trX_s)

    for i in range(len(trX_s)):
        trX_s[i][:-1] = trX_s[i][:-1]/max(trX_s[i][:-1])
        trX_s[i][-1] = trX_s[i][-1]/16.
    '''
    #training with number of empty

    for i in range(len(trX)):
        trX[i].append(trX[i].count(0))

    trX = floatX(trX[:-1])

    for i in range(len(trX)):
        trX[i][:-1] = trX[i][:-1]/max(trX[i][:-1])
        trX[i][-1] = trX[i][-1]/16.
    '''
    '''
    trX_s = []

    for i in range(len(trX[:-1])):
        if max(trX[i])<12:
            trX_s.append(trX[i])

    trX_s = floatX(trX_s)

    for i in range(len(trX_s)):
        trX_s[i] = trX_s[i]/max(trX_s[i])

    #normal training
    trX = floatX(trX[:-1])

    for i in range(len(trX)):
        trX[i] = trX[i]/max(trX[i])
    '''
    return trX_s, one_hot(trY,4)

def floatX(X):
    return np.asarray(X, dtype=theano.config.floatX)

def one_hot(x,n):
	if type(x) == list:
		x = np.array(x)
	x = x.flatten()
	o_h = np.zeros((len(x),n))
	o_h[np.arange(len(x)),x] = 1
	return o_h
