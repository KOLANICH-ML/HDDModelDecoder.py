#!/usr/bin/env python3
__all__=("loadTSVDataset", "roundCapacity", "attrGrouppedToRecords", "recordsToAttrGroupped")

import os, sys
import itertools, more_itertools
import re, json
from collections import OrderedDict, defaultdict
from pathlib import Path
datasetDir=Path(__file__).parent

from .myTSV import myTSV

sepRx=re.compile("\t+ *")

interfacesDSRXs = {
	"interface":"^([USP]?ATA|SAS|CE-?ATA|USB|FC)",
	"speed":"\\b(\\d+\\.\\d*)\\s+Gb[p/]s$",
	"version":"\\b(\\d+\\.\\d*)$",
}
interfacesDSRXs = { k:re.compile(r) for k, r in interfacesDSRXs.items() }

DictT=OrderedDict
#DictT=dict

def parseInterface(ifStr:str):
	res=DictT()
	rm=interfacesDSRXs["interface"].search(ifStr)
	if rm:
		rm=rm.groups()
		res["interface"]=rm[0]
	else:
		return None
	if "ATA" in res["interface"]:
		rm=interfacesDSRXs["speed"].search(ifStr)
		if rm:
			rm=rm.groups()
			res["speed"]=float(rm[0])
	elif "USB"==res["interface"]:
		rm=interfacesDSRXs["version"].search(ifStr)
		if rm:
			rm=rm.groups()
			res["version"]=tuple((int(el) for el in rm[0].split(".")))
	if "ZIF" in ifStr:
		res["ZIF"]=True
	return res

#import math
def roundCapacity(cap:(int, float)):
	#mult=10**min(math.floor(math.log10(cap)), 3)
	mult=10
	return round(cap/mult)*mult

def loadTSVDataset(fn:str):
	with fn.open("rt", encoding="utf-8") as f:
		lines=myTSV(fn)
		models=DictT(((l["model"], l) for l in lines))
		for m in models.values():
			try:
				m["rpm"]=int(m["rpm"])
			except:
				if m["rpm"]=="????":
					m["variable_rpm"]=True
				del(m["rpm"])
			m["capacity"]=roundCapacity(float(m["capacity"]))
			try:
				m["buffer_size"]=int(m["buffer_size"])
			except:
				del(m["buffer_size"])
			if "sector_size" in m:
				m["sector_size"]=int(m["sector_size"])
			m["interface"]=parseInterface(m["interface"])
		return models

def attrGrouppedToRecords(dic:dict, attrName:str="series", groupAttr:str="name"):
	return list(more_itertools.flatten((({groupAttr:mn, attrName:av} for mn in mns) for av, mns in dic.items())))

def recordsToAttrGroupped(lst:list, attrName:str="series", groupAttr:str="name"):
	res=defaultdict(set)
	for m in lst:
		res[m[attrName]].add(m[groupAttr])
	res={k:list(v) for k, v in res.items()}
	return res
