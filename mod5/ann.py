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

        # input, output
        self.X = T.fmatrix()
        self.Y = T.fmatrix()

        #Layers
        self.w_h = self.init_weights((784, self.listOfLayers[0]))
        self.w_h2 = self.init_weights((self.listOfLayers[0], self.listOfLayers[1]))
        self.w_o = self.init_weights((self.listOfLayers[1], 10))

        #Forward propagation
        h, h2, py_x = self.model(self.X, self.w_h, self.w_h2, self.w_o, 0., 0.)
        y_x = T.argmax(py_x, axis=1)

        # Error sammenliknet med svaret
        self.cost = T.mean(T.nnet.categorical_crossentropy(py_x, self.Y))
        params = [self.w_h, self.w_h2, self.w_o]

        # Backpropagation
        updates = self.RMSprop(self.cost, params, lr=0.001)

        # Training function
        self.train = theano.function(inputs=[self.X, self.Y], outputs=self.cost, updates=updates, allow_input_downcast=True)

        # Prediction function
        self.predict = theano.function(inputs=[self.X], outputs=y_x, allow_input_downcast=True)


    def blind_test(self,images):
        btX = images/255.

        predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)

        return

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

    # Backpropagation
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

        #X = self.dropout(X, p_drop_input)
        h = self.rectify(T.dot(X, w_h))

        #h = self.dropout(h, p_drop_hidden)
        h2 = self.rectify(T.dot(h, w_h2))

        #h2 = self.dropout(h2, p_drop_hidden)
        py_x = self.softmax(T.dot(h2, w_o))
        return h, h2, py_x


    def training(self, trX, trY):
        train = theano.function(inputs=[self.X, self.Y], outputs=cost, updates=updates, allow_input_downcast=True)

    def run(self):
        trX, teX, trY, teY = mnist(onehot=True)

        print ("Starting...")
        for i in range(20):
            for start, end in zip(range(0, len(trX), 100), range(100, len(trX), 100)):
                self.cost = self.train(trX[start:end], trY[start:end])

            #for x in range(len(trX)):
            #    cost = train(trX[x],trY[x])
            #cost = train(trX,trY)
            print ("epoch: " + str(i + 1))
        print ("Epoch number " + str(i + 1) + " predicted : " + str(np.mean(np.argmax(teY, axis=1) == self.predict(teX)) * 100) + str(" % correct"))

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

a = ann(listOfLayers=[100,100], learningRate=10, momentumRate=10, errorFunc=10)
a.run()
