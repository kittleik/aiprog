from ann import ann
import mnist_basics as mnist


EPOCHS_PER_GAME             = 3
BATCH                       = 100
NEURONS_IN_HIDDEN_LAYERS    = [784,500,500,10]
LIST_OF_FUNCTIONS           = ["rectify","rectify","softmax"]
LEARNING_RATE               = 0.001
MOMENTUM_RATE               = 0.9

a = ann(neuronsInHiddenLayers=NEURONS_IN_HIDDEN_LAYERS, listOfFunctions=LIST_OF_FUNCTIONS, learningRate=LEARNING_RATE, momentumRate=MOMENTUM_RATE, errorFunc="RMSprop")
a.run(BATCH,EPOCHS_PER_GAME)
mnist.minor_demo(a)
