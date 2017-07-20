#!/usr/bin/env python3
import os, sys
from pathlib import Path
import argparse

learnDir=Path(__file__).parent.absolute()
parentDir=learnDir.parent
sys.path.insert(0, str(parentDir))

from HDDModelDecoder.ml import WDDmatSpec

datasetDir=parentDir / "dataset"
defaultModelsDirName = "WD_models"

defaultModelsDir=Path(WDDmatSpec.__file__).parent/defaultModelsDirName
#defaultModelsDir=learnDir / defaultModelsDirName


def loadDataset():
	import json
	with (datasetDir / "WD_series.json").open("rt", encoding="utf-8") as f:
		return json.load(f)

def flattenDictGen(d):
	for k,v in d.items():
		if isinstance(v, dict):
			yield from ( (k+"_"+kk if k != kk else k, vv) for kk, vv in flattenDictGen(v) )
		else:
			yield (k, v)

def flattenDict(d):
	return dict(flattenDictGen(d))

def prepareDataset():
	import re
	import pandas
	from HDDModelDecoder.WD import WDDecoderInternal
	from decodeWDModelSeriesModifiers import decodeWDModelSeriesModifiers, series, seriesRx, modifiersSplitRx
	from dataset import attrGrouppedToRecords
	ds=loadDataset()
	ds=attrGrouppedToRecords(ds)
	#modifiers=set()
	for r in ds:
		tr=flattenDict(WDDecoderInternal(r["name"], learn=True)[1])
		if "series" in tr:
			del(tr["series"])
		r.update(tr)
		if "series" in r:
			r.update(decodeWDModelSeriesModifiers(r["series"]))
	ds=pandas.DataFrame.from_records(ds)
	ds.loc[(ds.loc[:, "form_factor"] == 3.5) & (ds.loc[:, "Scorpio"].isna()), "Scorpio"] = 0
	ds.loc[ds.loc[:, "Caviar"].isna(), "Caviar"] = 0
	ds.loc[ds.loc[:, "GP"].isna(), "GP"] = 0
	return ds

from AutoXGBoost import AutoXGBoost, formats

def train(train:bool=True, hyperparams:int=0, score:int=0, modelsDir:Path=None, format=None, hyperparamsOptimizerName="MSRSM", hyperparamsOptimizerPointsStorageFile:Path=None):
	if modelsDir is None:
		modelsDir=defaultModelsDir
	
	print("models dir is:", modelsDir)
	
	from pprint import pprint
	from NoSuspend import NoSuspend
	
	ds=prepareDataset()

	params={
		"booster": "dart",
		"nthread": -1,
		"learning_rate": 0.1,
		"min_split_loss": 0.,
		"max_depth": 10,
		"max_delta_step": 1,
		"verbosity": 0,
		#"metric":"error"
	}

	axg=AutoXGBoost(WDDmatSpec.spec, ds, params, prefix=modelsDir)
	print("Dataset columns: ")
	pprint(list(axg.pds.columns))
	with NoSuspend():
		if hyperparams is not None:
			import UniOpt
			if hyperparamsOptimizerPointsStorageFile:
				from UniOpt.core.PointsStorage import SQLiteStorage
				stor=SQLiteStorage(hyperparamsOptimizerPointsStorageFile)
			else:
				stor = None
			axg.saveHyperparams()
		if train:
			if hyperparams is None:
				axg.loadHyperparams()
			pprint(axg.bestHyperparams)
			axg.trainModels()
		if score:
			if not train:
				print("Loading models...")
				axg.loadModels()
				print("Models loaded: ", set(axg.models))
			axg.scoreModels(folds=score)
			axg.sortScores()
			pprint(axg.scores)
		
		if score or train:
			axg.saveModels(format=format)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Trains XGBoost models for WD series")
	parser.add_argument('--train', help='trains the models using current best hyperparams', action='store_true')
	parser.add_argument('--hyperparams', help='optimizes hyperparams using crossvalidation. Currently used hyperparams were acqired with 10000 iterations.', default=None, type=int)
	parser.add_argument('--hyperparamsOptimizerName', help='select hyperparams optimizer', default="MSRSM", type=str)
	parser.add_argument('--hyperparamsOptimizerPointsStorageFile', help='select points storage file for hyperparams optimizer', default=None, type=str)
	parser.add_argument('--score', help='scores models using crossvalidation', default=0, type=int)
	parser.add_argument('--modelsDir', help='dir to store models', default=defaultModelsDir, type=Path)
	parser.add_argument('--format', help='which format of models to use', default="binary", type=lambda f: getattr(formats, f))
	args = parser.parse_args()
	
	if not (args.train or args.hyperparams is not None or args.score):
		raise Exception("You MUST select the mode")
	train(**args.__dict__)
