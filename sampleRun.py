#!/usr/bin/env python

'''
Keith Murray
'''
import modelText
import random


def main():
    depth = 5
    saveFilename1 = "IRobotModel"
    saveFilename2 = "SciFiModel"



    # The sample text provided is "I, Robot" by Isaac Asimov 
    training = "IRobot.txt"
    myFile = open(training, 'r')
    text = myFile.read()

    # Model the training text
    models = modelText.generateModel(text, depth, [])
    # Simulate the model
    print 'Simulation01:\t', modelText.simulateText(models, "I")


    # Save the model
    modelText.saveModel(models, saveFilename1)
    # Load model from savefile
    loadedMod = modelText.loadModel(str(saveFilename1)+'.gzip')
    #loadedMod = models # Comment out load/save to see speed difference

    # Expand the model with "Dune" by Frank Herbert
    training2 = "Dune.txt"
    myFile = open(training2, 'r')
    text = myFile.read()
    newmodels = modelText.generateModel(text, len(loadedMod), loadedMod)
    # Simulate the model
    print 'Simulation02:\t', modelText.simulateText(newmodels, "I")

    # Save the expanded model 
    modelText.saveModel(newmodels, saveFilename2)

    # Print 10 sentences with random starting words
    for i in range(10):
	fakeText = modelText.simulateText(newmodels, random.sample(models[0],1)[0])
	print fakeText

    return


main()
