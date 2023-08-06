# Gaode - 高德 API

Gaode SDK for Python, which based on https://lbs.amap.com/api/webservice/summary/

### Install

```shell script
pip install gaode
```

### Usage

All API supported! please visit **[Supported methods](https://lbs.amap.com/api/webservice/guide/api/georegeo)** for more information!

```python
from gaode import Gaode

token = "TOKEN"
word = "饸饹"
gd = Gaode(token)
ret = gd.place_text(word=word)  # Limited to use `keyword arguments`
```

```json
{
    "count": "0",
    "info": "OK",
    "infocode": "10000",
    "pois": [],
    "status": "1",
    "suggestion": {
        "cities": [
            {
                "name": "西安市",
                "num": "1849"
            },
            ...
        ],
        "keywords": []
    }
}
```