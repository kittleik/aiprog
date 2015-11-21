from ann import ANN as ann
import mnist_basics as mnist

import theano
import theano.tensor as T
import theano.tensor.nnet as nnet
import numpy as np

#a = ann
#a.test()

train_x = np.linspace(-1, 1, 101)

train_y = 2 * train_x + np.random.randn(*train_x.shape) * 0.33

# symbolic variables
X = T.scalar()
Y = T.scalar()

def model(X, W):
    return X * W

W = theano.shared(np.asarray(0., dtype=theano.config.floatX))
y = model(X, W)

cost = T.mean(T.sqr(y - Y))
gradient = T.grad(cost=cost, wrt=W)
updates = [[W, W - gradient * 0.01]]

train = theano.function(inputs=[X,Y], outputs=cost, updates=updates, allow_input_downcast=True)

for i in range(100):
    for x,y in zip(train_x, train_y):
        train(x,y)
