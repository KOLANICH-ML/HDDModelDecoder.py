__all__=("SeagateDecoder",)
import re
from .interfaces import *
vendors={
	"ST": "Seagate",
	"MX": "Maxtor"
}

generations={
	"A": 1,
	"B": 2,
	"C": 3
}

segments={
	"DX": "Desktop Premium",
	"DM": "Mainstream",
	"DL": "Entry Level",
	"LX": "Laptop Premium",
	"LM": "Laptop Mainstream",
	"LT": "Laptop Thin",
	"MX": "Mission-Critical",
	"NM": "Enterprise?",#not sure
	"NX": "Nearline",
	"VX": "Surveillance",
	"VM": "DVR",
	"VN": "NAS?",#not sure
	"VT": "DVR Thin",
	"FX": "Enterprise SSD",
	"FM": "Enterprise SSD",
	"NE": "Enterprise NAS",
	"NC": "Enterprise Low Cost",
	"MP": "Enterprise Performance",
}

formFactors={
	"1": {"form_factor":3.5, "height":1.6},
	"2": {"form_factor":5.25, "height":1.6},
	"3": {"form_factor":3.5, "height":1},
	"4": {"form_factor":5.25, "height":3.25},
	"5": {"form_factor":3.5, "height":0.748},
	"6": {"form_factor":9},
	"7": {"form_factor":1.8},
	"8": {"form_factor":8},
	"9": {"form_factor":2.5, "height":0.748},
}


interfaces={
	"A": PATA,
	"ACE": PATA,
	"AS": SATA,
	"DC": {"interface":"Differential, SCA","pin_count":80}, #Single Connector Attachment
	"E": {"interface":"ESDI Interface"},
	"FC": IF(FC, pin_count=40, SCA=True),
	"J": {"interface":"SMD/SME-E Interface"},
	"K": {"interface":"IPI-2 Interface or Part of a Kit"},
	"LC": {"interface":"Low Voltage Differential, 80-pin SCA","pin_count":80, "SCA": True},
	"LW": {"interface":"Low Voltage Differential, 68-pin Wide SCSI Connector","pin_count":68},
	"N": IF(SCSI, comment="50-pin Narrow SCSI Connector", pin_count=50),
	"ND": IF(SCSI, comment="Differential, 50-pin Narrow SCSI Connector", pin_count=50),
	"NM": IF(SCSI, comment="50-pin Narrow SCSI Connector, Macintosh Compatible", pin_count=50),
	"NV": IF(SCSI, comment="50-pin Narrow SCSI Connector, Netware Ready", pin_count=50),
	"P": {"interface":"PCMCIA (PC Card) Interface"},
	"R": {"interface":"ST412/RLL Interface"},
	"S": {"interface":"Synchronized Spindle or Synchronous SCSI"},
	"W": IF(SCSI, comment="68-pin Wide SCSI Connector", pin_count=68),
	"WC": IF(SCSI, SCA=True, hot_swap=True, pin_count=80),
	"WD": IF(SCSI, comment="Differential, 68-pin Wide SCSI Connector", pin_count=68),
	"SS": SAS,
	"CS": SATA,
	"NS": SATA,
	"SV": SATA300,
	"ASG":SATA300,#?
	"SM2":SATA300,
	"SM3":SATA300,
	"AM2":PATA,
	"AM3":PATA
}
def SeagateDecoder(name:str):
	try:
		return SeagateDecodeFull(name)
	except:
		return SeagateDecodeSimplified(name)

vendorRx="("+"|".join(vendors.keys())+")"
interfacesRx="("+"|".join(interfaces.keys())+")"
rxFull=re.compile("^"+vendorRx+"(\d)(\d+?)"+interfacesRx+"$")
def SeagateDecodeFull(name:str):
	dic={}
	match=rxFull.match(name).groups()
	dic["vendor"]=vendors[match[0]]
	dic["form_factor"]=formFactors[match[1]]
	dic["capacity"]=int(match[2])/1000
	if len(match[3])==3 and match[3][-1]=="V":
		increasedCacheSize=True
		match[3]=match[3][:-1]
	dic["interface"]=interfaces[match[3]]
	return dic

segmentRx="("+"|".join(segments.keys())+")"
capacityRx="(\\d+)"
attrsRx="(\\d+)?"
generationRx="("+"|".join(generations.keys())+")?"
rxSimplified=re.compile("^"+vendorRx+capacityRx+segmentRx+attrsRx+generationRx+"$")
def SeagateDecodeSimplified(name:str):
	dic={}
	match=rxSimplified.match(name).groups()
	dic["vendor"]=vendors[match[0]]
	dic["capacity"]=int(match[1])
	if dic["capacity"]<=10:
		dic["capacity"]*=1000
	dic["segment"]=segments[match[2]]
	dic["attributes"]=match[3]
	if match[4]:
		dic["generation"]=generations[match[4]]
	return dic
