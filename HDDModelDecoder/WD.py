__all__=("WDDecoder",)
import re
import warnings
from .interfaces import *

vendors={
	"WD":"Western Digital"
}

rpmBufferSizeTypeFamily={
	"2": {"capacity":16, "type":"NAND"},
	"6": {"capacity":128, "type":"NAND"},
	"A": {
		"rpm": 5400,
		"buffer_size": 2, # 256
		"type":"HDD"
	},
	"B": {
		"rpm": 7200,
		"buffer_size": 2, # 256
		"type":"HDD"
	},
	"C": {"rpm": 5400, "buffer_size": 16, "type":"HDD", "variable_rpm":True},
	"D": {"rpm": 5400, "buffer_size": 32, "type":"HDD"},
	"E": {"rpm": 7200, "buffer_size": 64, "type":"HDD"},
	"F": {"rpm": 10000, "buffer_size": 16, "type":"HDD"},
	"G": {"rpm": 10000, "buffer_size": 8, "type":"HDD"},
	"H": {"rpm": 10000, "buffer_size": 32, "type":"HDD"},
	"J": {"rpm": 7200, "buffer_size": 8, "type":"HDD"},
	"K": {"rpm": 7200, "buffer_size": 16, "type":"HDD"},
	"L": {
		"rpm": 7200,
		"buffer_size": 32, #2
		"type":"HDD"
	},
	"M": {"segment":"Enterprise SED/WD Re"},
	"R": {"rpm": 5400, "buffer_size": 64, "type":"HDD"},
	"S": {
		"rpm": 7200,
		"buffer_size": 64, #8
		"type":"HDD"
	},
	"V": {"rpm": 5400, "buffer_size": 8, "type":"HDD", "segment":"Mobile"},
	"W": {"rpm": 7200, "buffer_size": 128, "type":"HDD"},
	"P": {"rpm": 5400, "type":"HDD", "variable_rpm":True},#/EM (maximum buffer size offered by product)
	"T": {"rpm": 10000, "type":"HDD"},#/EM (maximum buffer size offered by product)
	"Y": {"rpm": 7200, "type":"HDD"},#/EM (maximum buffer size offered by product)
	"Z": {"rpm": 5400, "buffer_size": 128, "type":"HDD"},
	"1": {"rpm": 5400, "buffer_size": 64, "type":"SSHD"}, #SSHD?

	"U": {"rpm": 5400} #?
}

interfaces={
	"R": IF(SATA150, NCQ=True),
	"A": UATA66,
	"B": UATA100,
	"C": IF(PATA, pin_count=33, ZIF=True),
	"D": IF(SATA150, pin_count=22),
	#"E": UATA133, # contradicts the data in dataset, need more investigation
	"E": UATA100, # contradicts the WD docs on model numbers 
	"F": IF(SAS1, pin_count=29),
	"G": IF(SAS2, pin_count=29),
	"K": IF(SATA600, NCQ=True),
	"S": IF(SATA300, pin_count=22),
	#"S": IF(SATA150, pin_count=22), # mobile
	"T": IF(SATA300, pin_count=22),
	"Y": SATA300,#?
	"V": USB20,#?
	"W": USB30,
	"X": IF(SATA600, pin_count=22),
	"Z": IF(SATA600, pin_count=22),
}

# according to the WD documents
capacityUnits={
	"A": 1,
	"B": 1,
	"L": 1,
	"C": 1,
	"G": 1,
	"H": 1,
	"M": 1,
	"E": 1000,
	"F": 1000,
	"J": 1000,
	"K": 1000,
	"N": 1000,
	"P": 1000,
	"S": 1000,
	"T": 1000,
	"X": 1000,
}

# reverse-enginneered
capacityUnits.update({
	"C": 10,
	"D": 10,
	"G": 10,
	"M": 10,
	"F": 10,
	"X": 10,
})

formFactors={
	'A': {"form_factor":3.5},
	'B': {
		"form_factor":2.5, 
		"height":0.374 # unconfirmed
	},
	'C': {"form_factor":1.0},
	'D': {"form_factor":3.5},
	'E': {"form_factor":3.5},
	'F': {"form_factor":3.5}, #(new format)
	'G': {"comment": '2.5" to 3.5" adapter'},
	'H': {"comment": '2.5" to 3.5" backplane adapter'},
	'J': {"form_factor":2.5, "height":0.374},
	'K': {"form_factor":3.5},# "(Generation ID))',
	'L': {"form_factor":2.5, "height":0.276},
	'M': {"form_factor":2.5, "height":0.197},
	'N': {"form_factor":2.5, "height":0.591},
	'P': {"form_factor":3.5}, #'surveillance/WD Purple',
	'S': {"form_factor":2.5, "height":0.276},
	'T': {"form_factor":2.5, "height":0.492},
	'X': {"form_factor":2.5, "height":0.374}, #new format
}


series={
	"9": {"segment":"Enterprise", "comment":"Cloud/Se"},
	"4": {"segment":"Enterprise", "comment":"Archive"},
	"B": {"segment":"Enterprise", "comment":"RE3 / RE2", "series":"RE", "platters": 3},
	"D": {"segment":"Enterprise", "series":"Raptor", "comment":"Self Encrypting Drive", "series":"RE"},
	"K": {"segment":"Enterprise", "comment":"Xe; S25"},
	"L": {"segment":"Enterprise", "series":"VelociRaptor"},
	"R": {"segment":"Enterprise", "sector_size": 4096, "series":"RE"},
	"S": {"segment":"Enterprise", "comment":"Power Safe 512e"},
	"W": {"segment":"Enterprise", "sector_size": 4096, "series":"VelociRaptor"},
	"Y": {"segment":"Enterprise", "comment":"RE4; RE3; RE2", "series":"RE", "platters": 4},
	
	"A": {"segment":"Desktop", "comment":"Blue; Green; Black", "Caviar":True},
	"F": {"segment":"Desktop", "comment":"NAS", "series":"Red"},
	"Z": {"segment":"Desktop", "comment":"Blue; Black; Green", "Caviar":True, "sector_size": 4096},
	
	"0": {"comment":"Dual Drive SSHD/Black", "type":"SSHD"},
	"1": {"comment":"Hybrid SSHD Gen 1/Black", "type":"SSHD"},
	"2": {"comment":"Hybrid SSHD Gen 2/Black", "type":"SSHD"},
	"3": {"comment":"Hybrid SSHD Gen 3/Blue?", "type":"SSHD"},#????????

	"C": {"segment":"Desktop", "comment":"SCSA/Vidity Protege"},
	"E": {"segment":"Mobile", "comment":"Blue; Green; Black"},
	"E": {"segment":"Mobile", "comment":"Scorpio Blue; Green; Black"},
	"J": {"segment":"Mobile", "comment":"Scorpio", "Free Fall Sensor":True},

	"G": {"segment":"Mobile", "series":"Purple"},
	"H": {"segment": "Workstation/Enthusiast", "comment":"VelociRaptor; Raptor X"},
	"M": {"segment": "Branded", "series":"Branded"},
	"P": {"segment":"Mobile", "comment":"Blue; Green; Black", "sector_size": 4096},
	
	"U": {"segment":"Audio/Video", "sector_size": 4096, "series":"AV"},
	"V": {"segment":"Audio/Video", "series":"AV"},
}

customerIDs={
	"00": "Generic",
	"01": "General Enterprise Market",
	"10": "DEC",
	"11": "WD Protege OEM",
	"12": "Intel",
	"18": "Dell",
	"23": "IBM",
	"25": "Toshiba",
	"28": "Microsoft",
	"32": "Reseller",
	"35": "WD Spartan",
	"40": "Apple",
	"44": "WD Protege Other",
	"53": "Gateway",
	"60": "Compaq",
	"71": "HP",
	"75": "Dell",
	"80": "Motorola",
	"90": "Distribution Only",
	"95": "Tektronix",
	"99": "Boeing"
}

regions={
	None:"US",
	"2":"Europe",
	"3":"Canada & Latin",
	"K":"Korea",
}
regionsRx="(["+"".join(filter(None, regions.keys()))+"])?"

kits={
	"DTL": "distribution",
	"RTL": "Retail",
	"DTL": "Disty",
}
kitsRx="("+"|".join(kits.keys())+")?"

packages={
	"B": "box",
	"C": "custom",
	"S": "custom",
	"W": "custom",
	"T": "clamshell",
}
packagesRx="("+"|".join(packages.keys())+")?"

modelTailRx=re.compile("^(.+)(?:"+kitsRx+packagesRx+regionsRx+")?$")

def parseModelTail(kit:str, package:str, region:str):
	dic={}
	if kit in kits:
		dic["kit"]=kits[kit]
	if package in packages:
		dic["package"]=packages[package]
	if (kit or package) and region in regions:
		dic["region"]=regions[region]
	return dic
	
def splitAndParseModelTail(model:str):
	try:
		(model, kit, package, region)=modelTailRx.match(model).groups()
		#print(model, kit, package, region)
		return (model, parseModelTail(kit, package, region))
	except:
		return (model, {})

import math
def alignWithBinary(decimalInGib:(int, float)):
	bytesInGib=10**9
	sectorSize=512
	alignSize=8*1024*2*sectorSize
	bytes=decimalInGib*bytesInGib
	sectors=round(bytes/alignSize)
	return sectors*alignSize/bytesInGib

vendorsRx="("+"|".join(vendors.keys())+")"
capacityRx="(\\dN|\\d{3}M|\\d{2,})"

formFactorsAndCapacityUnitsRx="["+"".join(formFactors.keys())+"]"
seriesRx="["+"".join(series.keys())+"]"

rpmBufferSizeTypeFamilyRx="(["+"".join(rpmBufferSizeTypeFamily.keys())+"])"
interfacesRx="(["+"".join(interfaces.keys())+"])"
customerIDsRx="(\\d{2})"


wdcRx=re.compile("^(?:wdc )?(.+)$")
modernRx=re.compile(
	vendorsRx+capacityRx+
	"("+formFactorsAndCapacityUnitsRx+seriesRx+")?"+
	rpmBufferSizeTypeFamilyRx+interfacesRx
)

def parseModelStr(model:str):
	#print(model)
	(v, capStr, ff_series, etc, ifc)=modernRx.match(model).groups()
	if ff_series:
		(ff, s) = (ff_series[0], ff_series[1])
	else:
		(ff, s) = (None, None)
	
	pc=None
	#print(v, capStr, ff, ff_series, ifc)
	if capStr[-1]=="N":
		pc=capStr[-1]
		capStr=capStr[:-1]
	elif ff in capacityUnits and ff in formFactors and s in series:
		if len(capStr) > 2:
			pc=capStr[-1]
			capStr=capStr[:-1]+"0"
	#else:
	#	capStr=capStr+ff+s
	#	ff=None
	#	s=None
	
	return (v, capStr, pc, ff, s, etc, ifc)

def WDDecoderInternal(model:str, learn:bool=False):
	model=wdcRx.match(model).group(1)
	
	try:
		(model, tail)=splitAndParseModelTail(model)
	except:
		pass
	res={}
	spl=model.find("-")
	if spl>1:
		(model, res["suffix"])=(model[0:spl],model[spl:])
		if res["suffix"][:2] in customerIDs and len(res["suffix"])>=2:
			res["customer"]=res["suffix"][:2]
		if len(res["suffix"])>=3:
			res["family_id"]=res["suffix"][2]
		if len(res["suffix"])>=4:
			res["customer_config_code"]=res["suffix"][3:]

	try:
		(vendorStr, capStr, productCode, ffCapUStr, seriesStr, etcCode, interfaceStr) = parseModelStr(model)
	except Exception as ex:
		#print(ex)
		raise ex
	#print(model, vendorStr, capStr, productCode, ffCapUStr, seriesStr, etcCode, interfaceStr)
	
	c=int(capStr)

	if ffCapUStr and seriesStr:
		multiplier=capacityUnits[ffCapUStr]
		res["form_factor"]=formFactors[ffCapUStr]
		res.update(series[seriesStr])
		if len(capStr)==1:
			c*=10
	else:
		multiplier=1

	if productCode:
		res["product_code"] = productCode

	res["vendor"]=vendors[vendorStr]
	res["capacity"]=c*multiplier/10
	res["capacity"]=alignWithBinary(res["capacity"])

	res.update(rpmBufferSizeTypeFamily[etcCode])
	
	res["interface"]=interfaces[interfaceStr]
	
	#fixes to violations of the code
	if interfaceStr == "S" and "segment" in res and res["segment"] == "Mobile":
		res["interface"]=IF(SATA150, pin_count=22)
	
	if res["interface"]["interface"]=="PATA":
		if etcCode in {"L", "E"}:
			res["buffer_size"]=2
		if etcCode in {"E"}:
			res["rpm"]=5400
	
	if tail and res:
		res.update(tail)
	
	if learn:
		mlVec=dict(
			zip(
				("vendorStr", "capStrLen", "productCode", "ffCapUStr", "seriesStr", "etcCode", "interfaceStr"),
				(vendorStr, len(capStr), productCode, ffCapUStr, seriesStr, etcCode, interfaceStr)
			)
		)
		mlVec.update(res)
		res = (res, mlVec)
	return res

def WDDecoder(model:str, predict:bool=False, vector:bool=False):
	if predict:
		from .ml.predictWD import predict
		(res, mlVec)=WDDecoderInternal(model, True)
		res.update(predict(mlVec, vector))
	else:
		if(vector):
			warnings.warn("ML is not used so no feature vectors for series. TODO:We need to one-hot encode it manully but we don't for now.")
		res=WDDecoderInternal(model, False)
	return res
