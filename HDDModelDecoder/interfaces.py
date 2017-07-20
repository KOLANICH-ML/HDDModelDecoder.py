class InterfaceMeta(type):
	def __new__(cls:type, className:str, parents:tuple, attrs:dict, **kwargs):
		res=super().__new__(cls, className, parents, attrs, **kwargs)
		res.update(kwargs)
		return res

class IF(dict, metaclass=InterfaceMeta):
	def __call__(self, **kwargs):
		return self.__class__(**kwargs)  #shit, causes some troubles, don't use for now

FC=IF({}, interface="FC")

SCSI=IF({}, interface="SCSI")

USB=IF({}, interface="USB")
USB20=IF(USB, version=(2, 0))
USB30=IF(USB20, version=(3, 0))

SAS=IF(SCSI, interface="SAS")
SAS1=IF(SAS, speed=3., version=1)
SAS2=IF(SAS1, speed=6., version=2)
SAS3=IF(SAS2, speed=12., version=3)
SAS4=IF(SAS3, speed=22.5, version=4)

PATA=UATA=IF({}, interface="PATA", pin_count=40)
PATA33=UATA33=IF(PATA, speed=0.0333, version=4)
PATA66=UATA66=IF(PATA33, speed=0.0667, version=5)
PATA100=UATA100=IF(PATA66, speed=0.100, version=6)
PATA133=UATA133=IF(PATA100, speed=0.133, version=7)
PATA167=UATA167=IF(PATA133, speed=0.167)

CEATA=IF({}, interface="CE-ATA")

SATA=IF({}, interface="SATA")
SATA1=SATA150=IF(SATA, speed=1.5, version=(1,0))
SATA2=SATA300=IF(SATA1, speed=3., version=(2,0))
SATA3=SATA600=IF(SATA2, speed=6., version=(3,0))
SATA32=IF(SATA3, speed=16., version=(3, 2))
IF(SATA3, speed=6, pin_count=22)
IF(SATA3, speed=6, pin_count=20)
IF(SATA, pin_count=22)