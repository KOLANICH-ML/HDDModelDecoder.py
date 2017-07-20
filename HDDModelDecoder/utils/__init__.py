import sys, os, _io, importlib
from psutil import virtual_memory
__all__=("flattenDict",)

def nearestPowerOf2(num:int):
	return 1 << (num-1).bit_length()

def flattenDictGen(d):
	for k,v in d.items():
		if isinstance(v, dict):
			yield from ( (k+"_"+kk if k != kk else k, vv) for kk, vv in flattenDictGen(v) )
		else:
			yield (k, v)

def flattenDict(d):
	return dict(flattenDictGen(d))

NoneType=type(None)
def makeSerializeable(obj):
	if isinstance(obj, (list, tuple, set)):
		return type(obj)((makeSerializeable(el) for el in obj))
	if isinstance(obj, dict):
		return type(obj)(( (k, makeSerializeable(v)) for k, v in obj.items()  ))
	if not isinstance(obj, (int, str, float, NoneType)):
		if hasattr(obj, "item") and callable(obj.item): # numpy scalar
			return obj.item()
		else:
			return str(obj)
	else:
		return obj
