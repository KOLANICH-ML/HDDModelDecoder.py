__all__=("MyTSV",)
import re
sepRx=re.compile("\t+ *")
commentRx=re.compile("#.+$")
DictT=dict
def myTSV(fileName):
	with fileName.open("rt", encoding="utf-8") as f:
		lines=[commentRx.sub("", l).strip() for l in f]
	lines=[sepRx.split(l) for l in lines if l]
	header=tuple((s.replace(" ", "_").lower() for s in lines[0]))
	lines=[DictT(zip(header, (tok.strip() for tok in l))) for l in lines[1:] if l]
	return lines
