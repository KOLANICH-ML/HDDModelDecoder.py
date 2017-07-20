__all__=("predictSeries",)
from ..utils import flattenDict
from .WDDmatSpec import spec, predictableFeatures
from lazy_object_proxy import Proxy
from lazily import lazyImport
from lazily import pandas
from lazily import Chassis
from lazily import AutoXGBoost

params={
	"booster": "dart",
	"colsample_bytree" : 0.965454918895709,
	"learning_rate" : 0.4326448624157522,
	"max_depth" : 20,
	"min_child_weight" : 0.03892563664756513,
	"min_split_loss" : 0.017928142119567426,
	"n_estimators" : 35,
	"reg_alpha" : 0.1971895336987934,
	"subsample" : 0.8519303786620037
}

#from pprint import pprint

def loadModel():
	from pathlib import Path
	currentDir=Path(__file__).parent
	modelsDir=currentDir / "WD_models"
	hyperparamsFile=modelsDir / "bestHyperparams.json"
	axg=AutoXGBoost.AutoXGBoostImputer(spec, None, params)
	axg.dontWarnAboutMissingStopColumns=True
	axg.loadHyperparams(hyperparamsFile)
	axg.loadModels(prefix=modelsDir, format=None)
	# axg.models, axg.bestHyperparams, axg.catIndex are the same in both loadings
	return axg

axg=Proxy(loadModel)

def predict(decoded, returnVector=False):
	dmat=Chassis.Chassis(spec)
	dmat.dontWarnAboutMissingStopColumns=True
	flattened=flattenDict(decoded)
	dmat.importDataset(pandas.DataFrame.from_records([flattened]))
	
	res={}
	for cn in axg.scores:
		pred=axg.predict(cn, dmat=dmat, argmax=(not returnVector))
		predictionVec=pred[0]
		if returnVector and cn in axg.catIndex:
			res[cn]=dict(zip(axg.catIndex[cn], predictionVec))
		else:
			res[cn]=predictionVec
	return res
