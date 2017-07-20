__all__=("ToshibaDecoder",)

import re
from .interfaces import *

heights={
	"A": 1,
	"B": 0.591,
	"D": 0.374,
	"F": 0.276,
	"Q": 0.591,
	"U": 0.276
}

options={
	"A": "4K Native (4Kn) AF",
	"AY": "4K Native (4Kn) AF and SIE ( Sanitize Instant Erase )",
	"B": "FIPS 140-2",
	"C": "Automotive",
	"E": "512 B sector emulation",
	"EY": "512 B Emulation (512e) AF and SIE ( Sanitize Instant Erase )",
	"H": "SSHD",
	"N": "512 B Native (512n) Format",
	"NY": "512 B Native (512n) Format and SIE ( Sanitize Instant Erase )",
	"P": "4K Native (4Kn) AF",
	"Q": "512 B Emulation (512e) AF",
	"V": "Video Stream",
	"VS": "Security Pairing",
	"W": "Wipe Technology",
	"B": "Enterprise Model",
	"D": "SED",
	"F": "Free Fall Sensor",
	"G": "Wipe Technology",
	"R": "Enterprise SED",
}

interfaces1={
	#"A": {"interface":"PATA or SATA"}, #need a lamba here to determine the interface?
	"A": SATA, #need a lamba here to determine the interface?
	#"S": {"interface":"SAS or SATA"},
	"S": SAS,
	"P": {"interface":"PCIe"},
	"R": SAS,
	"C": CEATA,
}

interface_speeds={
	"0": "6.0 or 12.0 Gbit/s (on most families only 6)",
	"D": 6,
	"E": 12,
}
rpm={
	"A": 4200,
	"B": 5400,
	"C": 7200,
	"E": 10500,
	"X": 15000,
}
endurances={
	"H": "High Endurance",
	"L": "Read Intensive (DWPD up to 0.5)",
	"M": "Mid Endurance",
	"R": "Read Intensive (DWPD up to 1)",
	"V": "Value Endurance",
}


optionsRx="("+"|".join(options.keys())+")"
heightRx="(["+"".join(heights.keys())+"])"
rpmEndRx="(["+"".join(rpm.keys())+"]|["+"".join(endurances.keys())+"])"
enduranceRx="(["+"".join(endurances.keys())+")"


firstKindFamilies={
	"AL": "Enterprise Performance HDD",
	"DT": "Desktop HDD, Video Stream HDD",
	"MC": "Enterprise Cloud HDD",
	"MD": "3.5-inch HDD",
	"MG": "Enterprise Capacity HDD",
	"MG": "Enterprise Capacity HDD",
	"MN": "NAS HDD",
	"MQ": "Mobile SSHD, Mobile Thin SSHD, Mobile HDD, Mobile Thin HDD, Video Stream HDD, Large Capacity HDD for External Storage, Automotive HDD",
	"PX": "Enterprise High Endurance SSD, Enterprise Mid Endurance SSD, Enterprise Value Endurance SSD, Enterprise Read Intensive SSD",
	"THN":"Client SSD, Enterprise Value Endurance SSD, Enterprise Read Intensive SSD",
}

firstKindFamiliesRx="("+"|".join(firstKindFamilies.keys())+")"
firstKindSeriesRx=r"(\w{2})"
firstKindInterfaceRx="(["+"".join(interfaces1.keys())+"])"
firstKindinterface_speedRx="(["+"".join(interface_speeds.keys())+"])"
firstKindCapacityRx=r"(\d{2,3})"

firstKindRx=re.compile(
	firstKindFamiliesRx+firstKindSeriesRx+firstKindInterfaceRx+rpmEndRx+heightRx+firstKindCapacityRx+
	firstKindinterface_speedRx+"?"+
	optionsRx+"?"
)

def firstKindParse(model:str):
	dic={}
	m=firstKindRx.match(model).groups()
	dic["family"]=firstKindFamilies[m[0]]
	dic["series"]=m[1]
	dic["interface"]=dict(interfaces1[m[2]])
	
	if m[3] in rpm:
		dic["rpm"]=rpm[m[3]]
	if m[3] in endurances:
		dic["endurance"]=endurances[m[3]]

	dic["form_factor"]={}
	dic["form_factor"]["height"]=heights[m[4]] 
	capStr=m[5]
	if len(capStr)<3:
		factor=100
	else:
		factor=10
	dic["capacity"]=int(capStr)*factor
	dic["interface"]["speed"]=m[6]
	dic["options"]=m[7]
	if dic["options"] in options:
		dic["options"]=options[dic["options"]]
	return dic


productLines={
	"B": "Enterprise Performance HDD",
	"J": "Mobile HDD",
	"H": "Mobile HDD",
}
formFactors={
	"2": 2.5,
	"3": 3.5
}
interfaces2etc={
	"AC": {"interface":{"interface":"PATA"}, "rpm":4200, "Support":"24×7", "Wide Temperature Support":True},
	"AH": {"interface": {"interface":"PATA"}, "rpm":5400,},
	"AT": {"interface": {"interface":"PATA"}, "rpm":4200,},
	"BH": {"interface": {"interface":"SATA"}, "rpm":5400,},
	"BJ": {"interface": {"interface":"SATA"}, "rpm":7200,},
	"BK": {"interface": {"interface":"SATA"}, "rpm":7200, "Support":"24×7"},
	"BS": {"interface": {"interface":"SATA"}, "rpm":5400, "Support":"24×7"},
	"CH": {"interface": {"interface":"SATA"}, "rpm":5400, "Security Feature":True},
	"CJ": {"interface": {"interface":"SATA"}, "rpm":7200, "Security Feature":True},
	"FC": {"interface": {"interface":"FC", "speed":2}},
	"FD": {"interface": {"interface":"FC", "speed":4}},
	"NP": {"interface": {"interface":"SCSI", "speed":0.320, "pin_count":68}},
	"NC": {"interface": {"interface":"SCSI", "speed":0.320, "pin_count":80}},
	"RC": {"interface": {"interface":"SAS"}},
}
productLineRx="(["+"".join(productLines.keys())+"])"
secondKindSeriesRx=r"(\w{2})"
formFactorRx="(["+"".join(formFactors.keys())+"])"
secondKindCapacityRx=r"(\d{3})"
secondKindEtcRx="("+"|".join(interfaces2etc.keys())+")"
secondKindRX=re.compile("(M)"+productLineRx+secondKindSeriesRx+formFactorRx+secondKindCapacityRx+secondKindEtcRx)
def secondKindParse(model:str):
	dic={}
	m=firstKindRx.match(model).groups()
	dic["model"]=m[0]
	dic["line"]=m[1]
	dic["series"]=m[2]
	dic["form_factor"]=m[3]
	dic["capacity"]=int(m[4])
	dic.update(interfaces2etc[m[5]])
	return dic

capacityUnits={
	"G": 1,
	"T": 1000
}
thirdKindFamilies={
	"MK": "1.8-inch HDD, Enterprise Performance HDD, Enterprise Capacity HDD, Enterprise SSD, Mobile HDD, Industrial HDD, Automotive HDD",
}
formFactorRPMHeightEtc={
	"K": {"form_factor":3.5,"rpm":7200},
	"C": {"form_factor":2.5,"rpm":7200, "Automotive":True},
	"M": {"form_factor":2.5,"rpm":5400, "height": 0.5},
	"R": {"form_factor":2.5,"rpm":15000},
	"S": {"form_factor":2.5, "rpm":4200, "height": 0.374},
	"X": {"form_factor":2.5, "rpm":5400, "height": 0.374},
	"Y": {"form_factor":2.5, "rpm":7200, "height": 0.374},
	"Z": {"form_factor":2.5, "type":"SSD"},
	"A": {"form_factor":1.8, "height":0.197, "rpm":3600},
	"B": {"form_factor":1.8, "height":0.315, "rpm":3600},
	"G": {"form_factor":1.8, "height":0.315, "rpm":5400},
	"H": {"form_factor":1.8, "height":0.315, "rpm":4200},
	"L": {"form_factor":1.8, "height":0.197, "rpm":4200},
}

def thirdKindParse(m):
	dic={}
	dic["family"]=thirdKindFamilies[m[0:2]]
	dic["capacity"]=int(m[2:4])*capacityUnits[m[6]]
	dic["series"]=m[4:6]
	dic["interface"]=interfaces1[m[7]]
	dic.update(formFactorRPMHeightEtc[m[8]])
	if len(m)>9:
		if m[9:] in options:
			dic["options"]=options[m[9:]]
		else:
			dic["options"]=m[9:]
	return dic

fourthKindFamilies={
	"THN":"Client SSD, Enterprise Value Endurance SSD, Enterprise Read Intensive SSD",
}

ssdDetails={
	"8N": {"M.2":"2280-D2-B-M", "interface": "SATA",},
	"AM": {"form_factor":1.8, "interface": "micro SATA"},
	"BS": {"form_factor":2.5,  "height":0.374, "interface": "SATA"},
	"CS": {"form_factor":2.5,  "height":0.276, "interface": "SATA"},
	"DN": {"M.2":"2280-D2-B-M", "interface": "SATA"}, 
	"MC": {"interface": "mSATA"}, 
	"MM": {"form_factor":1.8,  "caseless": True, "interface": "mSATA"}, 
	"MS": {"form_factor":2.5,  "caseless": True, "interface": "SATA"}, 
	"PU": {"M.2":"2280-S2-M", "interface": "PCIE"}, 
	"SX": {"M.2":"2230-S3/4-B-M", "interface": "PCIE"}, 
	"TY": {"M.2":"1620", "interface": "PCIE Signal"},
	"VN": {"M.2":"2280-S2-B-M", "interface": "SATA"}, 
	"VX": {"M.2":"2280-S3/4-B-M", "interface": "PCIE"}, 
}

ssdType={
	"SF": "SED",
	"SN": "Non-SED"
}

nonDigitRx=re.compile(r"([^\d])")
unitAndPLP={
	"G":(1,False),
	"T":(1000,False),
	"P":(1,True),
	"Q":(1000,True),
}

def decodeSSDCapacityAndPLP(capStr:str):
	m=nonDigitRx.match(capStr).group(1)
	cap=float(capStr.replace(m, "."))
	factor, plp = unitAndPLP[m]
	cap*=factor
	cap=(1<<(int(cap)-1).bit_length()) # Thanks to https://stackoverflow.com/questions/14267555/how-can-i-find-the-smallest-power-of-2-greater-than-n-in-python
	return {"capacity":cap,"PLP":plp}


def fourthKindParse(m:str):
	dic={"type":"SSD"}
	dic["family"]=fourthKindFamilies[m[0:3]]
	dic["model_type"]=ssdType[m[3:5]]
	dic["controller_type"]=m[5]
	dic.update(decodeSSDCapacityAndPLP(m[6:10]))
	dic.update(ssdDetails[m[10:12]])
	dic["nand_type"]=m[12]
	if dic["M.2"]:
		pass #todo: decode M.2 NGF
	return dic

fifthKindFamilies={
	"D":{"series":"P", "segment":"high-performance", "buffer_size":64},
	"U":{"series":"V", "segment":"streaming", "buffer_size":64},
	"J":{"series":"L", "segment":"mobile", "buffer_size":8},
	"K":{"series":"L", "segment":"mobile", "buffer_size":8},
	"F":{"series":"X", "segment":"high-performance", "buffer_size":128},
	"E":{"series":"X", "segment":"high-performance", "buffer_size":128},
	"G":{"series":"N", "segment":"high-reliability", "buffer_size":256},
	"N":{"series":"N", "segment":"high-reliability", "buffer_size":128},
	"Q":{"series":"N", "segment":"high-reliability", "buffer_size":128},
	"T":{"series":"S", "segment":"surveillance"}
}
fifthKindRetailBulk={
	"V":"bulk",
	"T":"retail",
	"5":"?",
}

fifthKindCapacityFactors={
	"A": 10
}

fifthKindFamiliesRx="(["+"".join(fifthKindFamilies.keys())+"])"
fifthKindRetailBulkRx="(["+"".join(fifthKindRetailBulk.keys())+"])"
fifthKindRx=re.compile(r'HDW'+fifthKindFamiliesRx+'(\\d)(\\d)(\\d|['+"".join(fifthKindCapacityFactors.keys())+'])(?:([EU])([Z])([S])'+fifthKindRetailBulkRx+'([A]))?')
def fifthKindParse(m:str):
	dic={}
	m=fifthKindRx.match(m).groups()
	dic.update(fifthKindFamilies[m[0]])
	#unkn=int(m[1])
	cap1=int(m[2])
	try:
		cap2=int(m[3])
		cap=cap1*10+cap2
		capFactor=1
	except:
		capFactor=fifthKindCapacityFactors[m[3]]
		cap=cap1*10
	
	dic["capacity"]=cap*capFactor*100
	
	if m[7] is not None:
		dic["shipping"]=fifthKindRetailBulk[m[7]]
		#dic["series"]=
		#dic["interface"]=
	return dic

def ToshibaDecoder(model:str):
	"""Decoder for Toshiba drives
	for more details visit https://toshiba.semicon-storage.com/ap-en/design-support/partnumber/storage-products.html
	"""
	for p in [firstKindParse, secondKindParse, thirdKindParse, fourthKindParse, fifthKindParse]:
		try:
			res = p(model)
			res["vendor"] = "Toshiba"
			return res
		except:
			pass
	