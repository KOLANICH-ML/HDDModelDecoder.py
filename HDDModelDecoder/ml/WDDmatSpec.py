__all__=("spec","predictableFeatures")

b="binary"
n="numerical"
c="categorical"
s="stop"
spec = {
	'Free Fall Sensor' : b,
	'buffer_size' : n,
	'capStrLen' : n,
	'capacity' : n,
	'comment' : s,
	'etcCode' : c,
	'seriesStr' : c,
	'ffCapUStr' : c,
	'form_factor' : c,
	'form_factor_height' : n,
	'interface_pin_count' : n,
	'interface_speed' : n,
	'interface_version' : s,
	'interface' : c,
	'interface_NCQ' : b,
	'interfaceStr' : c,
	'name' : s,
	'platters' : n,
	'product_code' : c,
	'rpm' : n,
	'sector_size' : n,
	'series' : c,
	'type' : s,
	'variable_rpm' : b,
	'vendor' : s,
	'vendorStr' : s,
	'segment': c,
}


predictableFeatures={
	#series name modifiers
	#'Pro' : b ,
	'Scorpio' : b ,
	'Caviar' : b ,
	#'NV' : b ,
	'GP' : b ,
	#'25' : b , # I guess it is related to form-factor
	#'16' : b
}

spec.update(predictableFeatures)
