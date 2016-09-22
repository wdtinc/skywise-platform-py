Products
========

The Product class allows you to query platform products and provides convenience methods for accessing a product's other
resources.

Retrieving products is done using the `find()` method along with any combination of keyword filters. You can also find
a specific product using its id or name.

.. code-block:: python

   from skywiseplatform import Product

   # Retrieve All Products
   all_products = Product.find()

   # Retrieve a Specific Product
   skywise_1hr_precip = Product.find('skywise-1hr-precipitation-analysis')

Filters
-------

---------
Start/End
---------
This allows you to request only products that have frames within your period of interest. You can use a valid ISO-8601
string, Python's native datetime objects, or anything else that is parseable by arrow_.

.. _arrow: http://crsmithdev.com/arrow/

.. code-block:: python

    import arrow

    analysis_products_2015 = Product.find(start='2015-01-01',  end=arrow.get('2015-12-31').datetime)
    forecast_products = Product.find(start=arrow.get(), end=arrow.get().replace(days=+7))

------------
Content Type
------------
Precipitation, temperature, and relative humidity are examples of content types.

.. code-block:: python

   precip_products = Product.find(contentType='precipitation')
   temp_products = Product.find(contentType='temperature')
   rh_products = Product.find(contentType='relative-humidity')

Here's a quick way to use `group()` to list out all content types currently in use:

.. code-block:: python

    >>> Product.find().group('contentType').keys()
    [u'wind-direction', u'temperature', u'dewpoint', u'wind-speed',
    u'solar-radiation', u'low-temperature', u'high-temperature',
    u'wind-speed-probability', u'reflectivity', u'wind-gust', u'evapotranspiration',
    u'precipitation', u'relative-humidity']

--------
Coverage
--------
A product's coverage indicates the region on the globe for which it has frames. This is useful for filtering products
down to an area of interest. You can specify coverage using the geojson_ module.

.. _geojson: https://pypi.python.org/pypi/geojson/

.. code-block:: python

    from geojson import Point, Polygon

    okc = Point((35.482309, -97.534994))
    products = Product.find(coverage=okc)

    ireland = Polygon([[(-11.55, 55.53), (-11.73, 51.45), (-5.14, 51.59), (-5.44, 55.45), (-11.55, 55.53)]])
    products = Product.find(coverage=ireland)

------------------
Aggregation Period
------------------
You can filter products by their aggregation period using integers to indicate the number of minutes in the period.
You can also just say 'hourly' or 'daily' for convenience.

.. code-block:: python

    hourly_products = Product.find(aggregation=60)
    daily_products = Product.find(aggregation='daily')

Styles
------
The `styles()` method will return all of a products styles:

.. code-block:: python

    >>> product = Product.find('skywise-contoured-na-base-reflectivity-mosaic')
    >>> [style.name for styles in product.styles()]
    [<Style skywise-contoured-na-base-reflectivity-mosaic-precip-typed>,
     <Style skywise-contoured-na-base-reflectivity-mosaic-default>]

These can be used with prerendered image formats (jpeg/png) [in conjunction with tile requests]().
