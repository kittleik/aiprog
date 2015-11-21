import theano
from theano import tensor as T
import numpy as np
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
from load import mnist
#import mnist_basics as mnist

srng = RandomStreams()


class ann:
    def __init__ (self, listOfLayers, learningRate, momentumRate, errorFunc):
        self.listOfLayers = listOfLayers
        self.numOfLayers = len(listOfLayers)
        self.learningRate = learningRate
        self.momentumRate = momentumRate
        self.errorFunc = errorFunc


    def blind_test():
        return 0

    # Helper
    def floatX(self, X):
        return np.asarray(X, dtype=theano.config.floatX)
    # Initialize weight
    def init_weights(self, shape):
        return theano.shared(self.floatX(np.random.randn(*shape) * 0.01))

    # Activation fuctions
    def rectify(self, X):
        return T.maximum(X, 0.)

    def softmax(self, X):
        e_x = T.exp(X - X.max(axis=1).dimshuffle(0, 'x'))
        return e_x / e_x.sum(axis=1).dimshuffle(0, 'x')

    def RMSprop(self, cost, params, lr=0.001, rho=0.9, epsilon=1e-6):
        grads = T.grad(cost=cost, wrt=params)
        updates = []
        for p, g in zip(params, grads):
            acc = theano.shared(p.get_value() * 0.)
            acc_new = rho * acc + (1 - rho) * g ** 2
            gradient_scaling = T.sqrt(acc_new + epsilon)
            g = g / gradient_scaling
            updates.append((acc, acc_new))
            updates.append((p, p - lr * g))
        return updates

    # Drop out
    def dropout(self, X, p=0.):
        if p > 0:
            retain_prob = 1 - p
            X *= srng.binomial(X.shape, p=retain_prob, dtype=theano.config.floatX)
            X /= retain_prob
        return X

    # Artificial neural net model
    def model(self, X, w_h, w_h2, w_o, p_drop_input, p_drop_hidden):
        X = self.dropout(X, p_drop_input)
        h = self.rectify(T.dot(X, w_h))

        h = self.dropout(h, p_drop_hidden)
        h2 = self.rectify(T.dot(h, w_h2))

        h2 = self.dropout(h2, p_drop_hidden)
        py_x = self.softmax(T.dot(h2, w_o))
        return h, h2, py_x

    def run(self):
        trX, teX, trY, teY = mnist(onehot=True)

        X = T.fmatrix()
        Y = T.fmatrix()

        w_h = self.init_weights((784, 625))
        w_h2 = self.init_weights((625, 625))
        w_o = self.init_weights((625, 10))

        noise_h, noise_h2, noise_py_x = self.model(X, w_h, w_h2, w_o, 0.2, 0.5)
        h, h2, py_x = self.model(X, w_h, w_h2, w_o, 0., 0.)
        y_x = T.argmax(py_x, axis=1)

        cost = T.mean(T.nnet.categorical_crossentropy(noise_py_x, Y))
        params = [w_h, w_h2, w_o]
        updates = self.RMSprop(cost, params, lr=0.001)

        train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
        predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)
        print ("Starting...")
        for i in range(3):
            for start, end in zip(range(0, len(trX), 128), range(128, len(trX), 128)):
                cost = train(trX[start:end], trY[start:end])
            print ("iteration number " + str(i) + " predicted : " + str(np.mean(np.argmax(teY, axis=1) == predict(teX)) * 100) + str(" % correct"))

'''
class ann:


import mnist_basics as mnist

images, labels = mnist.load_mnist('testing', digits=[0,9])

print (images[0])
print (labels[0])
'''

#----------------------TRAINING DATA--------------------


'''
image = images[1111]
label = labels[1111]

print (label)
mnist.show_digit_image(image,cm='gray')
'''

a = ann(listOfLayers=[10,2,4], learningRate=10, momentumRate=10, errorFunc=10)
a.run()
