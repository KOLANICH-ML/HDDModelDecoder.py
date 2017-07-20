__all__=("SamsungDecoder",)
import re
from .interfaces import *
from collections import OrderedDict

sPostfixes={
	"N": {"interface":UATA133, "series":"P80"},
	"S": {"interface":SATA,},
	"C": {"interface":SATA,},
}

def SamsungDecoderS(prefix:str, number:str, postfix:str):
	dic={}
	dic.update(sPostfixes[postfix[-1]])
	
	if dic["interface"]["interface"]=="SATA":
		dic["buffer_size"]=8
	if postfix[-1]=="N" or postfix[-1]=="C":
		dic["capacity"]=int(number[0:2])*10
	else:
		dic["capacity"]=int(number[1])*10
	dic["heads"]=int(postfix[0:-1])
	return dic

segments={
	"D": "Desktop",
	"M": "Mobile",
	"E": "Enterprise"
}

postfixes=OrderedDict(( # regex working depends on the order
	("HI", {"interface": SATA300, "rpm": 5400}),
	("HJ", {"interface": SATA300, "rpm": 7200}),
	("GJ", {"interface": SATA300, "rpm": 7200}),
	("HX", {"interface": USB20, "rpm": 5400}),
	("IX", {"interface": USB20, "rpm": 5400}), # may be wrong
	("JX", {"interface": USB20, "rpm": 5400}), # may be wrong
	("JI", {"interface": SATA300, "rpm": 5400}),
	('HA', {"interface": IF(PATA, ZIF=True), "rpm": 3600}),
	('GA', {"interface": IF(PATA, ZIF=True), "rpm": 3600}), # may be wrong
	('GB', {"interface": IF(PATA, ZIF=True), "rpm": 4200}), # may be wrong
	('GI', {"interface": SATA300, "rpm":  None}), # may be wrong, trouble with rpm
	('HB', {"interface": IF(PATA, ZIF=True), "rpm": 4200}),
	('THB', {"interface": IF(PATA, ZIF=True), "rpm": 4200}),
	('HC', {"interface": PATA, "rpm": 5400}),
	('II', {"interface": SATA300, "rpm": 5400}),
	('IJ', {"interface": SATA300, "rpm": 7200}),
	('JB', {"interface": IF(PATA, ZIF=True), "rpm": 4200}),
	('TJB', {"interface": IF(PATA, ZIF=True), "rpm": 4200}), # may be wrong
	('JJ', {"interface": SATA300, "rpm": 7200}),
	('JQ', {"interface": CEATA, "rpm": 4200}),
	('UJQ', {"interface": CEATA, "rpm": 4200}), # may be wrong
	('LD', {"interface": UATA100, "rpm": 7200}),
	('LI', {"interface": SATA300, "rpm": 5400}),
	('LJ', {"interface": SATA300, "rpm": 7200}),
	('MBB', {"interface": SATA300, "rpm": 5400}),
	('RHF', {"interface": SATA300, "rpm": 5400}),
	('RJF', {"interface": SATA300, "rpm": 5400}),
	('SI', {"interface": SATA300}),
	('SJ', {"interface": SATA300, "rpm": 7200}),
	('UI', {"interface": SATA300}),
	('UJ', {"interface": SATA300, "rpm": 7200}),
	('VHF', {"interface": SATA300, "rpm": 5400}),
	('VJF', {"interface": SATA300, "rpm": 5400}),
	('WI', {"interface": SATA300}),
))

def SamsungDecoderH(prefix:str, number:str, postfix:str):
	dic={}
	dic["segment"]=segments[prefix[-1]]
	dic.update(postfixes[postfix])
	return dic

def SamsungDecoderHS(prefix:str, number:str, postfix:str):
	dic={}
	dic.update(postfixes[postfix])
	return dic

prefixes={
	'HD': SamsungDecoderH ,
	'HE': SamsungDecoderH ,
	'HM': SamsungDecoderH ,
	'HN-M': SamsungDecoderH,
	'HS':SamsungDecoderHS,
	'SP': SamsungDecoderS
}

prefixesRx="("+"|".join(prefixes)+")"
postfixesRx="("+"|".join(postfixes)+"|\\d["+"".join(sPostfixes)+"])"
modelRx=re.compile(prefixesRx+"(\\d{2,3})"+postfixesRx )
def SamsungDecoder(model:str):
	model = model.upper()
	m = (prefix, num, postfix) = modelRx.match(model).groups()
	dic = prefixes[prefix](*m)
	dic["vendor"] = "Samsung"
	return dic