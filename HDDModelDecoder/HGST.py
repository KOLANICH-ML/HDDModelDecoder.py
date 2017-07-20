__all__=("HGSTDecoder",)
import re
from .interfaces import *

vendors={
	"H":"HGST",
	"W":"WD"
}
families={
	"U": "Ultrastar",
	"D": "Deskstar",
	"T": "Travelstar",
	"E": "Endurastar",
	"C": "CinemaStar",
	"M": "Microdrive",
	"S": "Shingled Magnetic Recording"
}

series = {
	"H": "Helium",
	"S": "Standard",
	"C": "Compact",
	"E": "Enhanced Availability",
	"A": "Auto",
	"T": "Two-disk",
	"N": "NAS",
	"P": "P Series"
}
heights={
	"L": 1,
	"7": 0.276,
	"9": 0.374,
	"5": 0.197,
	"S": 0.583
}

interfaces={
	"16": IF(SCSI, speed=0.160, pin_count=68),
	"18": IF(SCSI, speed=0.160, pin_count=80),
	"36": IF(SCSI, speed=0.320, pin_count=68),
	"38": IF(SCSI, speed=0.320, pin_count=80),
	"F2": IF(FC, speed=2, pin_count=40),
	"F4": IF({}, interface="FCAL", speed=4),
	"AT": PATA,
	"SA": SATA150,
	"A3": SATA300,
	"A6": SATA600,
	"E6": SATA600,#512e,
	"N6": SATA600,#4Kn
	"SS": SAS,
	"42": SAS3,#4Kn,
	"52": SAS3,#512e,
	"S6": SAS2,
}

securityModes={
	"0":"Instant Secure Erase",
	"1":"Bulk Data Encryption (SATA), TCG SED encryption (SAS)",
	"2": None, # reserved
	"4":"Secure Erase (overwrite only)",
	"5":"TCG encryption with FIPS (SAS)",
}

generationCodesToNumberOfPlatters={
	"P":1,
	"D":2,
	"V":3,
	"K":5,
	"A":8,
}
buffer_sizes={# MiB
	"0":None,#reserved
	"1":128,
	"2":2,
	"3":32,
	"4":64,
	"8":8,
	"6":16
}
featureCodes={
	"M": "Host-managed",
	"0": "Reserved",
	"L": "Legacy Pin 3 configuration",
}

coolSpin={
	"5C":{"variable_rpm":True}
}


vendorRx="(["+"".join(vendors.keys())+"])"
familiesRx="(["+"".join(families.keys())+"])"
seriesRx="(["+"".join(series.keys())+"])"
rpmRx="(\d{2}|"+"|".join(coolSpin.keys())+")"
capacityRx="(\d{2})"
generationCodesRx="(["+"".join(generationCodesToNumberOfPlatters.keys())+"])"
heightsRx="(["+"".join(heights.keys())+"])"
interfacesRx="("+"|".join(interfaces.keys())+")"
featureCodesRx="(["+"".join(buffer_sizes.keys())+"".join(featureCodes.keys())+"])"
securityModesRx="(["+"".join(securityModes.keys())+"])"
modelRx=re.compile(vendorRx+familiesRx+seriesRx+rpmRx+capacityRx+capacityRx+generationCodesRx+heightsRx+interfacesRx+featureCodesRx+securityModesRx)

def HGSTDecoder(model:str):
	"""Decoder for HGST and Hitachi drives
	for more details visit the search results of 
	https://www.google.com/search?q=inurl%3Ahttps%3A%2F%2Fwww.hgst.com%2Fsites%2Fdefault%2Ffiles%2Fresources%2F+filetype%3Apdf+%22How+to+read%22+%22model+number%22
	"""
	dic={}
	dic["vendor"]=vendors[model[0]]
	dic["family"]=families[model[1]]
	dic["series"]=series[model[2]]
	
	if model[3:5] not in coolSpin:
		dic["rpm"]=int(model[3:5])
		if dic["rpm"]<36:
			dic["rpm"]*=1000
		else:
			dic["rpm"]*=100
	else:
		dic.update(coolSpin[model[3:5]])
	
	capacityPowerOf10=100
	if model[1] == "S" :
	 	capacityPowerOf10*=10
	dic["top_capacity"]=int(model[5:7]) * capacityPowerOf10 #the capacity, in gigabytes, of the largest member of the drive family, divided by 10 (or 100).
	dic["capacity"]=int(model[7:9]) * capacityPowerOf10 #Capacity this model, GB
	dic["generation_code"]=model[9] # Generation code, although this value can also be used to identify the maximum number of platters in the drive family
	if dic["generation_code"] in generationCodesToNumberOfPlatters:
		dic["max_platters"]=generationCodesToNumberOfPlatters[dic["generation_code"]]
	
	dic["form_factor"]={}
	dic["form_factor"]["height"]=heights[model[10]]
	dic["interface"]=interfaces[model[11:13]]
	dic["feature_code"]=model[13]
	if dic["feature_code"] in buffer_sizes:
		dic["buffer_size"]=buffer_sizes[dic["feature_code"]]
	if dic["feature_code"] in featureCodes:
		dic["feature"]=featureCodes[dic["feature_code"]]
	
	if model[14] in securityModes:
		dic["data_security_mode"]=securityModes[model[14]]
	else:
		dic["data_security_mode"]=model[14]
	return dic
