import theano
from theano import tensor as T
import numpy as np
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
from load import mnist
import mnist_basics as mnist_b
import copy
import matplotlib.pyplot as plt

class ann:
    def __init__ (self, neuronsInHiddenLayers, listOfFunctions, learningRate, momentumRate, errorFunc):
        self.neuronsInHiddenLayers = neuronsInHiddenLayers
        self.listOfFunctions = listOfFunctions
        self.numOfHiddenLayers = len(neuronsInHiddenLayers)
        self.learningRate = learningRate
        self.momentumRate = momentumRate
        self.errorFunc = errorFunc

        # input, output
        self.X = T.fmatrix()
        self.Y = T.fmatrix()
        #Layers
        self.hidden_layers = []
        for i in range(len(neuronsInHiddenLayers)):
            if i == (len(neuronsInHiddenLayers) - 1):
                break
            self.hidden_layers.append( self.init_weights( ( self.neuronsInHiddenLayers[i], self.neuronsInHiddenLayers[i+1] ) ) )

        #Forward propagation
        tunedWeights = self.model(self.X, self.hidden_layers)
        y_x = T.argmax(tunedWeights[-1], axis=1)

        # Error sammenliknet med svaret
        self.cost = T.mean(T.nnet.categorical_crossentropy(tunedWeights[-1], self.Y))
        params = self.hidden_layers

        # Backpropagation
        updates = self.RMSprop(self.cost, params, lr=0.001)

        # Training function
        self.train = theano.function(inputs=[self.X, self.Y], outputs=self.cost, updates=updates, allow_input_downcast=True)

        # Prediction function
        self.predict = theano.function(inputs=[self.X], outputs=y_x, allow_input_downcast=True)


    def blind_test(self,images):
        btX = self.floatX(images)
        btX = btX/255.
        res = self.predict(btX)
        res = res.tolist()
        return res

    # Helper
    def floatX(self, X):
        return np.asarray(X, dtype=theano.config.floatX)

    def printSetUp(self):
        setUp = []
        for (f,b) in zip(self.neuronsInHiddenLayers, self.listOfFunctions):
            setUp.append(f)
            setUp.append(b)
        print (setUp)

    # Initialize weight
    def init_weights(self, shape):
        return theano.shared(self.floatX(np.random.randn(*shape) * 0.01))

    # Activation fuctions
    def rectify(self, X):
        return T.maximum(X, 0.)

    def softmax(self, X):
        e_x = T.exp(X - X.max(axis=1).dimshuffle(0, 'x'))
        return e_x / e_x.sum(axis=1).dimshuffle(0, 'x')

    def sigmoid(self, X):
        return T.nnet.sigmoid(X)

    def arctan(self, X):
        return T.arctan(X)

    def tanh(self, X):
        return T.tanh(X)

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

    def runActivationFunction(self, X, w, activation_function):
        if activation_function == "sigmoid":
            h = self.sigmoid(T.dot(X, w))
        elif activation_function == "rectify":
            h = self.rectify(T.dot(X, w))
        elif activation_function == "softmax":
            h = self.softmax(T.dot(X, w))
        elif activation_function == "arctan":
            h = self.arctan(T.dot(X, w))
        elif activation_function == "tanh":
            h = self.tanh(T.dot(X, w))
        return h

    # Artificial neural net model
    def model(self, X, hidden_layers):
        ret = []

        for i in range(len(hidden_layers)):
            if i == 0:
                ret.append( self.runActivationFunction(X, hidden_layers[i], self.listOfFunctions[i]) )
            else:
                ret.append( self.runActivationFunction(ret[i-1], hidden_layers[i], self.listOfFunctions[i]) )
        return ret


    def training(self, trX, trY):
        train = theano.function(inputs=[self.X, self.Y], outputs=cost, updates=updates, allow_input_downcast=True)


    def run(self, delta, epochs):
        trX, trY = mnist_b.load_mnist()
        trX = self.floatX(trX)
        trX = trX/255.
        trX = trX.reshape((60000,28*28)).astype(float)
        trY = one_hot(trY, 10)

        teX, teY = mnist_b.load_mnist("testing")
        teX = self.floatX(teX)
        teX = teX/255.
        teX = teX.reshape((10000,28*28)).astype(float)
        teY = one_hot(teY, 10)

        result_list = [self.neuronsInHiddenLayers, self.listOfFunctions, delta, epochs,[]]
        print ("Starting...")
        self.printSetUp()
        for i in range(epochs):
            for start, end in zip(range(0, len(trX), delta), range(delta, len(trX), delta)):
                self.cost = self.train(trX[start:end], trY[start:end])

            predicted = np.mean(np.argmax(teY, axis=1) == self.predict(teX)) * 100
            result_list[4].append(predicted)
            print ("epoch: " + str(i + 1))
            print ("Epoch number " + str(i + 1) + " predicted : " + str(predicted) + str(" % correct"))

        print (result_list)
        plt.plot(result_list[4])
        plt.ylabel('correctness rate')
        plt.xlabel('epochs')
        plt.show()

#--------------HELPER FUNCTION------------------------------
def one_hot(x,n):
	if type(x) == list:
		x = np.array(x)
	x = x.flatten()
	o_h = np.zeros((len(x),n))
	o_h[np.arange(len(x)),x] = 1
	return o_h

#a = ann(neuronsInHiddenLayers=[784,10,10], listOfFunctions=["rectify","softmax"], learningRate=0.001, momentumRate=10, errorFunc=10)
a = ann(neuronsInHiddenLayers=[784,500,500,10], listOfFunctions=["rectify","rectify","softmax"], learningRate=0.001, momentumRate=10, errorFunc=10)
#a = ann(neuronsInHiddenLayers=[784,500,500,10], listOfFunctions=["rectify","rectify","sigmoid"], learningRate=0.001, momentumRate=10, errorFunc=10)
#a = ann(neuronsInHiddenLayers=[784,10,10,10,10], listOfFunctions=["rectify","rectify","rectify","softmax"], learningRate=0.001, momentumRate=10, errorFunc=10)


a.run(delta=100,epochs=50)
mnist_b.minor_demo(a)
