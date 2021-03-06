HDDModelDecoder.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[![TravisCI Build Status](https://travis-ci.org/KOLANICH/HDDModelDecoder.py.svg?branch=master)](https://travis-ci.org/KOLANICH/HDDModelDecoder.py)
![GitLab Build Status](https://gitlab.com/KOLANICH/HDDModelDecoder.py/badges/master/pipeline.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/HDDModelDecoder.py.svg)](https://coveralls.io/r/KOLANICH/HDDModelDecoder.py)
![GitLab Coverage](https://gitlab.com/KOLANICH/HDDModelDecoder.py/badges/master/coverage.svg)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/HDDModelDecoder.py.svg)](https://libraries.io/github/KOLANICH/HDDModelDecoder.py)

![Logo](https://gitlab.com/KOLANICH/HDDModelDecoder.py/raw/master/HDDModelDecoder_Logo.svg)

wheels:
* [using XGBoost for ML](https://gitlab.com/KOLANICH/HDDModelDecoder.py/-/jobs/artifacts/master/raw/wheels/HDDModelDecoder-CI_xgboost-py3-none-any.whl?job=build) (works without XGBoost, but ML-based predictions are unavailable)
* [pure python](https://gitlab.com/KOLANICH/HDDModelDecoder.py/-/jobs/artifacts/master/raw/wheels/HDDModelDecoder-CI_python-py3-none-any.whl?job=build) - not very implemented yet.


Decodes info hidden in HDD model names.

```python
print(HDDModelDecoder.decodeModel("ST4000DM004")) # {'vendor': 'Seagate', 'capacity': 4000, 'segment': 'Mainstream', 'attributes': '004'}
print(HDDModelDecoder.decodeModel("ST1000VX000")) # {'vendor': 'Seagate', 'capacity': 1000, 'segment': 'Surveillance', 'attributes': '000'}
print(HDDModelDecoder.decodeModel("ST500LM030")) # {'vendor': 'Seagate', 'capacity': 500, 'segment': 'Laptop Mainstream', 'attributes': '030'}
print(HDDModelDecoder.decodeModel("ST4000DM005")) # {'vendor': 'Seagate', 'capacity': 4000, 'segment': 'Mainstream', 'attributes': '005'}
print(HDDModelDecoder.decodeModel("ST95005620AS")) # {'vendor': 'Seagate', 'form_factor': {'form_factor': 2.5, 'height': 0.748}, 'capacity': 5005.62 (WRONG!), 'interface': 'SATA'}

print(HDDModelDecoder.decodeModel("HDN724040ALE640")) # {'vendor': 'HGST', 'family': 'Deskstar', 'series': 'NAS', 'rpm': 7200, 'top_capacity': 4000, 'capacity': 4000, 'generation_code': 'A', 'height': 1, 'interface': {'interface': 'SATA', 'speed': 6}, 'feature_code': '4', 'buffer_size': 64, 'data_security_mode': 'Instant Secure Erase'}
print(HDDModelDecoder.decodeModel("HDN724030ALE640")) # {'vendor': 'HGST', 'family': 'Deskstar', 'series': 'NAS', 'rpm': 7200, 'top_capacity': 4000, 'capacity': 3000, 'generation_code': 'A', 'height': 1, 'interface': {'interface': 'SATA', 'speed': 6}, 'feature_code': '4', 'buffer_size': 64, 'data_security_mode': 'Instant Secure Erase'}
print(HDDModelDecoder.decodeModel("HTS721010A9E630")) # {'vendor': 'HGST', 'family': 'Travelstar', 'series': 'Standard', 'rpm': 7200, 'top_capacity': 1000, 'capacity': 1000, 'generation_code': 'A', 'height': 0.374, 'interface': {'interface': 'SATA', 'speed': 6}, 'feature_code': '3', 'buffer_size': 32, 'data_security_mode': 'Instant Secure Erase'}
print(HDDModelDecoder.decodeModel("HTE721010A9E630")) # {'vendor': 'HGST', 'family': 'Travelstar', 'series': 'Enhanced Availability', 'rpm': 7200, 'top_capacity': 1000, 'capacity': 1000, 'generation_code': 'A', 'height': 0.374, 'interface': {'interface': 'SATA', 'speed': 6}, 'feature_code': '3', 'buffer_size': 32, 'data_security_mode': 'Instant Secure Erase'}
print(HDDModelDecoder.decodeModel("HUS726060ALE614")) # {'vendor': 'HGST', 'family': 'Ultrastar', 'series': 'Standard', 'rpm': 7200, 'top_capacity': 6000, 'capacity': 6000, 'generation_code': 'A', 'height': 1, 'interface': {'interface': 'SATA', 'speed': 6}, 'feature_code': '1', 'data_security_mode': 'Secure Erase (overwrite only)'}
print(HDDModelDecoder.decodeModel("HDP725025GLA380")) # {'vendor': 'HGST', 'family': 'Deskstar', 'series': 'P Series', 'rpm': 7200, 'top_capacity': 5000, 'capacity': 2500, 'generation_code': 'G', 'height': 1, 'interface': {'interface': 'SATA', 'speed': 3}, 'feature_code': '8', 'buffer_size': 8, 'data_security_mode': 'Instant Secure Erase'}
```

Sources of information
----------------------
* [HGST Datasheets](https://www.google.com/search?q=inurl%3Ahttps%3A%2F%2Fwww.hgst.com%2Fsites%2Fdefault%2Ffiles%2Fresources%2F+filetype%3Apdf+%22How+to+read%22+%22model+number%22)
* WD Manuals: [Model Number Format for OEM and Distribution Channels](https://www.wdc.com/wdproducts/library/Flyer/ENG/2579-001028.pdf) and [Legacy Model and Order Numbers](https://products.wdc.com/library/other/2579-701261.pdf)
* [Toshiba website](https://toshiba.semicon-storage.com/ap-en/design-support/partnumber/storage-products.html)
* ["Understanding Hard Drive Model Numbers" forum post](https://hardforum.com/threads/understanding-hard-drive-model-numbers.921544/)
* ["Western Digital hard drives - deciphering the extended model #" forum post](http://forums.storagereview.com/index.php?/topic/22131-western-digital-hard-drives-deciphering-the-extended-model/)
* [Samsung datasheets](https://www.google.com/search?q=inurl%3Ahttps%3A%2F%2Fwww.seagate.com%2F+samsung+datasheet+filetype%3Apdf) and [Product selection guides](https://www.google.com/search?q=site%3Asamsung.com+AND+%22product+selection+guide%22+AND+filetype%3Apdf+AND+7200)

Dependencies
------------
* [```Python >=3.4```](https://www.python.org/downloads/). [```Python 2``` is dead, stop raping its corpse.](https://python3statement.org/) Use ```2to3``` with manual postprocessing to migrate incompatible code to ```3```. It shouldn't take so much time. For unit-testing you need Python 3.6+ or PyPy3 because their ```dict``` is ordered and deterministic.

* **Optionally** [```xgboost```](https://github.com/dmlc/xgboost) ![Licence](https://img.shields.io/github/license/dmlc/xgboost.svg) [![PyPi Status](https://img.shields.io/pypi/v/xgboost.svg)](https://pypi.python.org/pypi/xgboost) [![TravisCI Build Status](https://travis-ci.org/dmlc/xgboost.svg?branch=master)](https://travis-ci.org/dmlc/xgboost) [![Libraries.io Status](https://img.shields.io/librariesio/github/dmlc/xgboost.svg)](https://libraries.io/github/dmlc/xgboost) [![Gitter.im](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/dmlc/xgboost), if you want non-HGST WD drives series.


Building
--------
For building with ML you will also need

* [```pandas```](https://github.com/pandas-dev/pandas) ![Licence](https://img.shields.io/github/license/pandas-dev/pandas.svg) [![PyPi Status](https://img.shields.io/pypi/v/pandas.svg)](https://pypi.python.org/pypi/pandas) [![TravisCI Build Status](https://travis-ci.org/pandas-dev/pandas.svg?branch=master)](https://travis-ci.org/pandas-dev/pandas) [![CodeCov Coverage](https://codecov.io/github/pandas-dev/pandas/coverage.svg?branch=master)](https://codecov.io/github/pandas-dev/pandas/) [![Libraries.io Status](https://img.shields.io/librariesio/github/pandas-dev/pandas.svg)](https://libraries.io/github/pandas-dev/pandas) [![Gitter.im](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/pydata/pandas)


* [```Chassis.py```](https://gitlab.com/KOLANICH/Chassis.py) ![Licence](https://img.shields.io/github/license/KOLANICH/Chassis.py.svg) [![PyPi Status](https://img.shields.io/pypi/v/Chassis.py.svg)](https://pypi.python.org/pypi/Chassis.py)
[![TravisCI Build Status](https://travis-ci.org/KOLANICH/Chassis.py.svg?branch=master)](https://travis-ci.org/KOLANICH/Chassis.py)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/Chassis.py.svg)](https://coveralls.io/r/KOLANICH/Chassis.py)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/Chassis.py.svg)](https://libraries.io/github/KOLANICH/Chassis.py)
[![Gitter.im](https://badges.gitter.im/Chassis.py/Lobby.svg)](https://gitter.im/Chassis.py/Lobby) and its dependencies

