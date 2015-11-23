import requests

lr = [32, 128, 128, 64, 128, 32, 64, 128, 64, 128, 128, 64, 64, 64, 64, 128, 128, 128, 64, 128, 64, 32, 64, 64, 128, 64, 64, 128, 32, 128, 128, 64, 64, 64, 64, 64, 256, 128, 128, 64, 128, 128, 128, 64, 32, 64, 64, 32, 128, 128]

la = [128, 128, 128, 64, 512, 256, 128, 128, 128, 128, 128, 128, 256, 256, 256, 64, 64, 128, 64, 128, 256, 256, 256, 256, 256, 64, 128, 128, 512, 128, 128, 128, 128, 256, 128, 64, 128, 256, 256, 256, 128, 256, 128, 256, 128, 512, 128, 64, 128, 128]


def welch(list1, list2):
    params = {"results": str(list1) + " " + str(list2), "raw": "1"}
    resp = requests.post('http://folk.ntnu.no/valerijf/6/', data=params)
    return resp.text

print welch(lr,la)

#a = Ann(neuronsInHiddenLayers=[16,250,200,4], listOfFunctions=["rectify","rectify","softmax"], learningRate=0.001, momentumRate=10, errorFunc=10)
#a.training(trX, trY,20,1)
