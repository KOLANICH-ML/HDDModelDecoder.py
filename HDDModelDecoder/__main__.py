import sys, json, re
from . import decodeModel
from collections import OrderedDict
from .utils import makeSerializeable

import importlib.util

def ifModExists(modName):
	return importlib.util.find_spec(modName) is not None

useML = (ifModExists("numpy") and ifModExists("pandas") and ifModExists("xgboost") and ifModExists("Chassis") and ifModExists("AutoXGBoost"))

try:
	from RichConsole import groups, rsjoin
	styles={
		"prefix": groups.Fore.lightcyanEx,
		"cli": groups.Fore.lightgreenEx,
		"help": groups.Fore.lightmagentaEx,
	}
except:
	styles={
		"prefix": lambda x:x,
		"cli": lambda x:x,
		"help": lambda x:x,
	}
	def rsjoin(self, *args, **kwargs):
		return self.join(*args, **kwargs)


endMainRx=re.compile("\.__main__$")
wsRx=re.compile("\s")
def splitByWhitespaces(file):
	for l in file:
		yield from wsRx.split(l)


def showHelp():
	if sys.platform=="win32":
		try:
			import colorama
			colorama.init()
		except:
			pass
	prefix=styles["prefix"](rsjoin(" ", ("python -m", endMainRx.sub("", __spec__.name))))
	print(
		rsjoin("\n", (
			styles["cli"](rsjoin(" ", (prefix, cliArg))) + styles["help"]("  - "+par[1])
			for cliArg, par in singleArgLUT.items()
		))
	)

def getModelObj(mn):
	return makeSerializeable(decodeModel(mn, useML, True))

def whole(modelNames):
	json.dump( OrderedDict(( (el, getModelObj(el)) for el in modelNames )), sys.stdout, indent="\t")

def fromStdinByOne():
	for el in filter(None, splitByWhitespaces(sys.stdin)):
		json.dump(getModelObj(el), sys.stdout, indent="\t")
		sys.stdout.write("\n")
		sys.stdout.flush()

def fromStdinWhole():
	whole(filter(None, splitByWhitespaces(sys.stdin)))

singleArgLUT=OrderedDict((
	("model_name_1, model_name_2, ...", (None, "to pass models namebers as parameters")),
	("--", (fromStdinByOne, "to pipe models namebers into stdin and get the results as JSON one by one")),
	("-" , (fromStdinWhole, "to pipe models namebers file into stdin and get the results as a JSON array")),
	("-h", (showHelp, "shows help")),
	("--help", (showHelp, "shows help")),
))

def main():
	if len(sys.argv)<2:
		showHelp()
	elif len(sys.argv)==2 and sys.argv[1] in singleArgLUT:
		singleArgLUT[sys.argv[1]][0]()
	else:
		whole(sys.argv[1:])
		sys.stdout.write("\n")

if __name__ == "__main__":
	main()