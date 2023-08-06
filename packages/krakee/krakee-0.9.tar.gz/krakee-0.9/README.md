[![PyPI version](https://badge.fury.io/py/krakee.svg)](https://badge.fury.io/py/krakee)
# krakee

[Kraken](https://kraken.com) Exchange API with a thin pandas Dataframe wrap.

Krakee allows interacting with the Kraken API and handling data using Pandas' dataframes.

### Installation
```
pip install krakee
```

### Example

```python
from krakee import Krakee

kr = Krakee()
print(kr.asset_pairs().XXBTZEUR)
...
altname
XBTEUR
wsname
XBT / EUR
aclass_base
currency
base
XXBT
...
Name: XXBTZEUR, dtype: object
```
### Main features

* Data handling using Dataframes
* Cached public API requests to build/test on top of Kraken API without annoying them too much
* Extra validation of API parameters
* Order builder to create/validate trades in the private API
* Public/Private Kraken API integration, you can freely fetch public data without an account

Krakee is built on top of:
* krakenex
* pykrakenapi
* pandas

