import split
import reader
import baselines
import test
import helper
import bprmf
import numpy as np
import RankMFX
import cPickle

SEED1=1
SEED2=11
EPOCHS=3

#learningratevalues=[0.001,0.01,0.1]
#regularizationvalues=[0,0.001,0.01,0.1,1]
learningratevalues=[0.01,0.1]
regularizationvalues=[0,1]

def readDBandSplit(dbfile):
	r=reader.tabSepReader(dbfile)
	fulltrain,testDict=split.split(
		r.getR(),SEED1)
	trainingDict,evalDict=split.split(
		fulltrain,SEED2)
	output=open("splits.npz","wb")
	cPickle.dump(r,output,-1)
	cPickle.dump(trainingDict,output,-1)
	cPickle.dump(testDict,output,-1)
	cPickle.dump(evalDict,output,-1)
	output.close()
	return r,trainingDict,fulltrain,testDict,evalDict

#r,trainingDict,testDict=
#	readDBandSplit("kleinu.data")

def loadData():
	inputfile=open("testDict.npz","rb")
	r=cPickle.load(inputfile)
	trainingDict=cPickle.load(inputfile)
	testDict=cPickle.load(inputfile)
	evalDict=cPickle.load(inputfile)
	inputfile.close()
	return r,trainingDict,testDict,evalDict

#r,trainingDict,testDict,evalDict=loadData()

#helper.writeInternalToFile(
	#r,trainingDict,"training")
#helper.writeInternalToFile(
	#r,testDict,"test")

def constant(r,trainingDict,testDict):
	rec=baselines.constant(trainingDict)
	print("Hitrate for constant: %r"
		%test.hitrate(
			testDict,rec.getRec,10))

#constant(r,trainingDict,testDict)

def random(r,trainingDict,testDict):
	rec=baselines.randomRec(trainingDict)
	print("Hitrate for random: %r"
		%test.hitrate(
			testDict,rec.getRec,10))

#random(r,trainingDict,testDict)

def learnRankMFX(r,trainingDict,reg,ler):
	rank=RankMFX.RankMFX()
	W,H = rank.learnModel(
		r.getMaxUid(),r.getMaxIid(),
		reg,reg,reg,ler,trainingDict,
		350,EPOCHS,
		r.numberOfTransactions)
	np.savez_compressed(
		"RankMFXModelFile",W=W,H=H)
	return W,H

#learnRankMFX(r,trainingDict)

def learnBPRMF(r,trainingDict,reg,ler):
	W,H = bprmf.learnModel(
		r.getMaxUid(),r.getMaxIid(),
		reg,reg,reg,ler,trainingDict,
		350,EPOCHS,
		r.numberOfTransactions)
	np.savez_compressed(
		"BPRMFModelFile",W=W,H=H)
	return W,H

#learnBPRMF(r,trainingDict)

def loadM(name):
	modelf=np.load(name+".npz")
	W=modelf['W']
	H=modelf['H']
	modelf.close
	return W,H

#W,H=loadM("RankMFXModelFile")
#W,H=loadM("BPRMFModelFile")

def testMF(W,H,trainingDict,testDict):
	t=test.MFtest(W,H,trainingDict)
	hr=test.hitrate(testDict,t.getRec,10)
	return hr

#testMF(W,H,trainingDict,testDict)

def tweak(learnModel):
	file=open("results.data","a")
	legend="Algorithm|Regconstant|Learningrate|Epochs|Hitrate\n"
	file.write(legend)

	r,trainingDict,fulltrain,testDict,evalDict=readDBandSplit("kleinu.data")

	results=[]

	for reg in regularizationvalues:
		for ler in learningratevalues:
			W,H=learnModel(
				r,trainingDict,reg,ler)
			results.append(
				testMF(W,H,trainingDict,
				evalDict))
			s=(learnModel.__name__+"|%r|%r|%r|%r\n"
				%(reg,ler,EPOCHS,
				results[-1]))
			print("")
			print(legend+s)
			file.write(s)
			
	index=results.index(max(results))
	count=0
	for reg in regularizationvalues:
		for ler in learningratevalues:
			if count!=index:
				continue
			count+=1
			W,H=learnModel(
				r,fulltrain,reg,ler)
			hr=testMF(W,H,fulltrain,
				testDict)
			s=("Best:\n"+learnModel.__name__+"|%r|%r|%r|%r\n\n"
				%(reg,ler,EPOCHS,
				results[-1]))
			print("")
			print(legend+s)
			file.write(s)

	file.close()

for i in xrange(0,10):
	print("BPRMF %r"%i)
	tweak(learnBPRMF)

for i in xrange(0,10):
	print("RankMFX%r"%i)
	tweak(learnRankMFX)
