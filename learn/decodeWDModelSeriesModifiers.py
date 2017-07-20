__all__=("decodeWDModelSeriesModifiers", )

import re
series = ('RED', 'Green', 'Purple', 'Gold', 'Black', 'Blue' , 'AV', 'RE\\d?', 'RE16', 'Xe' , 'S25', 'SE16', 'SE', 'WD450AA line', 'Protege', '(?:Veloci)?Raptor', 'My Passport', 'UltraSlim')
seriesRx = re.compile("("+ "|".join(series)+")" )
modifiersSplitRx=re.compile("\\W")

def decodeWDModelSeriesModifiers(s):
	r={}
	m=seriesRx.search(s)
	if m:
		#print(m , m.groups() )
		r["series"] = m.groups()[0]
		s=s[:m.span()[0]]+ s[m.span()[1]:]
	else:
		r["series"] = "Old Caviar"
	for m in modifiersSplitRx.split(s):
		try:
			r["form_factor"]=int(m)/10
			continue
		except:
			pass
		if m:
			r[m]=True
	return r
