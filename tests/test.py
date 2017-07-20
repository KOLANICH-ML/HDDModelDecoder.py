#!/usr/bin/env python3
import sys
from pathlib import Path
import unittest
import itertools, re
from collections import OrderedDict
from glob import glob

testsDir=Path(__file__).parent
parentDir=testsDir.parent
datasetDir=parentDir / "dataset"
sys.path.insert(0, str(parentDir))

from dataset import *
from HDDModelDecoder import decodeModel

def genTestMethod(model):
	model=type(model)(model)
	def testFunc(self):
		decoded=decodeModel(model["model"])
		#for pr in decoded:
		#	self.assertEqual(decoded[pr], model[pr])
		self.assertTrue(decoded)
		if "capacity" in decoded:
			decoded["capacity"]=roundCapacity(decoded["capacity"])
		self.assertDictCommonSubset(model, decoded)
	testFunc.__name__="test"+model["model"]
	#testFunc.__doc__=model["model"]
	return testFunc

def createDictsCommonSubset(d1, d2):
	t1={}
	t2={}
	for k in set(d1.keys()) & set(d2.keys()):
		t1[k]=d1[k]
		t2[k]=d2[k]
		if isinstance(t1[k], dict) and isinstance(t2[k], dict):
			(t1[k], t2[k]) =createDictsCommonSubset(t1[k], t2[k])
	return (t1, t2)

def generateTest(name, datasetFileName=None):
	if not datasetFileName:
		datasetFileName=datasetDir / (name+".tsv")
	models=loadTSVDataset(datasetFileName)
	class DatasetTestMeta(type):
		def __new__(cls, className, parents, attrs, *args, **kwargs):
			for m in models.values():
				testFunc=genTestMethod(m)
				attrs[testFunc.__name__]=testFunc
				
			res=super().__new__(cls, className, parents, attrs, *args, **kwargs)
			return res
	class Test(unittest.TestCase, metaclass=DatasetTestMeta):
		maxDiff=None
		def assertDictCommonSubset(self, d1, d2):
			self.assertDictContainsSubset(*createDictsCommonSubset(d1, d2))
	Test.__name__=name
	return Test

def generateTests(names=None):
	if not names:
		names=[n.stem for n in datasetDir.glob("*.tsv")]
	for name in names:
		yield generateTest(name)

def combineSuites(testSuites):
	s=unittest.TestSuite()
	for testSuite in testSuites:
		s.addTests(testSuite._tests)
	return s

class GeneratedTestProgram(unittest.TestProgram):
	def __init__(self, tests, defaultTest=None, argv=None, testRunner=None, testLoader=unittest.loader.defaultTestLoader, exit=True, verbosity=1, failfast=None, catchbreak=None, buffer=None, warnings=None, *args, **kwargs):
		runTestsBackup=self.runTests
		self.testz=tests
		super().__init__(object(), defaultTest, argv, testRunner, testLoader, exit, verbosity, failfast, catchbreak, buffer, warnings, *args, **kwargs)
	def createTests(self):
		self.test=combineSuites(map(self.testLoader.loadTestsFromTestCase, self.testz))
		if self.testNames:
			self.testNames=set(self.testNames)
			self.test._tests=type(self.test._tests)(filter(lambda e: e[1] in self.testNames, self.test._tests.items()))

GeneratedTestProgram(generateTests())
