[![Build Status](https://travis-ci.org/wdtinc/skywise-platform-py.svg?branch=master)](https://travis-ci.org/wdtinc/skywise-platform-py)

# Overview
A Python client library for the SkyWise Platform API. For an overview, examples, and more, [read the docs]().

# Installation

## Prerequisites

- [Python 2.7](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/)

```bash
pip install skywise-platform
```

> **Windows Users**
> You will most likely need to install **gevent** beforehand. You can typically find the latest wheel [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#gevent).

## Configure App ID/Key
The easiest (and recommended) way to configure authentication to the API is by setting the following environment variables:

```bash
SKYWISE_PLATFORM_APP_ID='{YOUR_APP_ID}'
SKYWISE_PLATFORM_APP_KEY='{YOUR_APP_KEY}'
```

Otherwise, you'll need to set your App ID/Key explicitly in your app/script before making API calls:

```python
from skywiseplatform import PlatformResource

PlatformResource.set_user('{YOUR_APP_ID}')
PlatformResource.set_password('{YOUR_APP_KEY}')
```

## Try It Out
Let's test out our install by requesting the latest Product listing:

```python
import json
from skywiseplatform import Product

products = Product.find()
for p in products:
    print p.name
```

Your output should look something similar to this:

```bash
skywise-1hr-dewpoint-temperature-analysis
skywise-1hr-evapotranspiration-short-analysis
skywise-1hr-evapotranspiration-short-forecast
skywise-1hr-evapotranspiration-tall-analysis
skywise-1hr-evapotranspiration-tall-forecast
...
weatherops-tropical-64kt-wind-probability-forecast
weatherops-tropical-precipitation-forecast
weatherops-tropical-wind-direction-forecast
weatherops-tropical-wind-gust-forecast
weatherops-tropical-wind-speed-forecast
```

# Links
- [skywise-platform-py docs]()
- [Platform HTTP Interface docs]()
