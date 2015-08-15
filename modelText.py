#!/usr/bin/env python

'''
Keith Murray
'''
import random
import gzip,cPickle




def generateModel(text, depth, models = []):
    def growModel(d, w1, w2):
	if w1 in d:
	    subd = d[w1]
	    if w2 in subd:
	    	subd[w2] += 1
	    else:
	    	subd[w2] = 1
    	else:
	     d[w1] = {w2:1}
    	return d
    def parseText(text):
	# http://stackoverflow.com/questions/18221436
	text = text.lower()
	text = text.replace(".", " .")
	text = text.replace("!", " !")
	text = text.replace("?", " ?")
	text = text.replace("'", "")
	text = text.replace('"', '')
	return text
    def scanText(text, window, d = {}):
	i = 0
	while i < len(text)-window:
	    w1 = text[i]
	    w2 = text[i+window]
	    d = growModel(d, w1, w2)
	    i += 1
	return d


    sink = [".", "!", "?"]

    text = parseText(text)
    text = text.split()
    
    if (len(models) == 0):
	# Building initial model
	for i in range(depth):
	    models.append(scanText(text, i+1))
    
    else:
	# GROWING MODEL
	if depth != len(models):
	    print "ERROR: Model is not equal to stated depth."
	    return
	for i in range(depth):
	    models[i] = scanText(text, i+1, models[i])
	
    return models


def simulateText(model, keyword, limSize=100):
    #print model[keyword]
    moError = 0.0001 # NOT IN USE (NIU)
    sink = [".", "!", "?"]
    def normalizeD(subd):
	# NIU
	totWeight = sum(subd.itervalues())/float(1 - moError) # http://stackoverflow.com/questions/4880960
	for key, value in subd.keys():
	    subd[key] = subd[key] / float(totWeight)
	return subd

    def mergeModels(models):
	# really basic model merge, just to get a result
	masterD = {}
	masterD = models[0] # no manipulation to most recent model
	# for cleaner see http://stackoverflow.com/questions/11011756/
	for i in range(1, len(models)):
	    d2 = models[i]
	    for d2key in d2.keys():
		if d2key in masterD:
		    masterD[d2key] = masterD[d2key] + d2[d2key]
		    # **Code below may cause unnerving Overflow Errors. **
		    #   It has the weird effect of a record skipping, and depending on which
		    #   word it skips on, the text stream may be creepy. 
		    #   Enjoy.
		    #masterD[d2key] = min((masterD[d2key] + d2[d2key]* min(len(d2key), 9)), 1000000)
		    #masterD[d2key] = masterD[d2key] + d2[d2key]* min(len(d2key), 9)
		else:
		    masterD[d2key] = d2[d2key]
	return masterD
	
    def nextWord(keyD):
	mD = mergeModels(keyD)
	totWeight = sum(mD.itervalues())
	n = random.uniform(0, totWeight)
	runSum = 0
	words = mD.keys()
	freqs = [mD[x] for x in words] # http://stackoverflow.com/questions/18453566
	for i in range(len(freqs)):
	    runSum = runSum + freqs[i]
	    if n <= runSum:
		return words[i]
	if len(words) == 0:
	    print "ERROR: Keyword does not appear in model."
	    print "\tReturning word 'the' to generate text"
	    return "the"
	return words[len(words)-1]

    # Allows for multiple words to be input
    keyword = keyword.lower()
    keyword = keyword.split()
    newText = keyword

    i = 1
    while True:
	keyD = []
  	for j in range(min(len(model), i)):
	    depthD = model[j]
	    try:
		keyD.append(depthD[newText[i-j-1]])
	    except:
		# Error Note: If there are no dictionaries for the key, 'the' will be returned
		keyD.append({})
	newWord = nextWord(keyD)
	newText.append(newWord)
	i += 1
	if (newWord in sink) or i > limSize:
	    break
    newText = " ".join(newText)
    newText = newText[0].upper()+newText[1:-2]+newText[-1]
	    
	
    return newText

def saveModel(models, filename):
    # Copied from bioil's Dstory.py
    file = gzip.open(filename+'.gzip', 'w')
    cPickle.dump(models, file)
    file.close()
    return

def loadModel(filename):
    # Copied from bioil's Dstory.py
    file = gzip.open(filename)
    models = cPickle.load(file)
    file.close()
    return models


