import theano
from theano import tensor as T
import numpy as np
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
import get_data

srng = RandomStreams()

class Ann:
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
        updates = self.RMSprop(self.cost, params, lr=self.learningRate, rho=self.momentumRate)

        # Training function
        self.train = theano.function(inputs=[self.X, self.Y], outputs=self.cost, updates=updates, allow_input_downcast=True)

        # Prediction function
        self.predict = theano.function(inputs=[self.X], outputs=tunedWeights[-1], allow_input_downcast=True)

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

    def sigmoid(self,X):
        return T.nnet.sigmoid(X)

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

    def training(self,trX,trY, delta, epochs):

        for i in range(epochs):
            for start, end in zip(range(0, len(trX), delta), range(delta, len(trX), delta)):
                self.cost = self.train(trX[start:end], trY[start:end])

        #print ("Epoch number " + str(i + 1) + " predicted : " + str(np.mean(np.argmax(teY, axis=1) == self.predict(teX)) * 100) + str(" % correct"))
