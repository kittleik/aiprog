from ann import ANN as ann
import mnist_basics as mnist

import theano
import theano.tensor as T
import theano.tensor.nnet as nnet
import numpy as np

a = T.scalar()
b = T.scalar()

y = a * b

multiply = theano.function(inputs=[a, b], outputs=y)

print (multiply(3,3))
print (multiply(4,5))

W = T.matrix('W')
x = T.matrix('x')

dot = T.dot(x, W)
y   = T.nnet.sigmoid(dot)

train_x = np.linspace(-1, 1, 101)

train_y = 2 * train_x + np.random.randn(*train_x.shape) * 0.33
