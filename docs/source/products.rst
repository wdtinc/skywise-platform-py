Products
========

The Product class allows you to query platform products and provides convenience methods for accessing a product's other
resources.

Finding Products
----------------
Retrieving products is done using the `find()` method along with any combination of keyword filters. You can also find
a specific product using its id or name.

.. code-block:: python

   from skywiseplatform import Product

   all_products = Product.find()
   skywise_1hr_precip = Product.find('skywise-1hr-precipitation-analysis')

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
If you're only interested in products of a particular content type: precipitation, temperature, relative humidity, etc.

.. code-block:: python

   precip_products = Product.find(contentType='precipitation')
   temp_products = Product.find(contentType='temperature')
   rh_products = Product.find(contentType='relative-humidity')

--------
Coverage
--------
A product's coverage indicates the region for which it has frames. This is useful for filtering products down to an area
of interest. You can specify coverage using the geojson_ module.

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
Product's typically represent frames on an hourly or daily basis, but for radar products can be as often as every five
minutes. You can filter products by their aggregation period using integers to indicate the number of minutes in the period.
60 would indicate an hourly product and 1400 would indicate a daily product. You can also just say 'hourly' or 'daily'
for convenience.

.. code-block:: python

    radar_products = Product.find(aggregation=5)
    hourly_products = Product.find(aggregation='hourly')
    daily_products = Product.find(aggregation='daily')

