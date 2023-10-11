__all__=("decodeModel",)
import typing
from warnings import warn

from .HGST import *
from .Samsung import *
from .Seagate import *
from .WD import *
from .Toshiba import *

warn("We have moved from M$ GitHub to https://codeberg.org/KOLANICH-ML/HDDModelDecoder.py, read why on https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo .")

def decodeModel(model:str, predict:bool=False, vector:bool=False) -> typing.Dict[str, typing.Any]:
	if model[0]=="H" or model[0]=="W":
		if model[0:2]=="WD":
			return WDDecoder(model, predict, vector)
		try:
			return HGSTDecoder(model)
		except:
			pass
	elif model[0:2]=="ST":
		return SeagateDecoder(model)
	elif model[0:2]=="SP":
		return SamsungDecoder(model)
	
	try:
		res=SamsungDecoder(model)
		if res:
			return res
	except:
		pass
	return ToshibaDecoder(model)
