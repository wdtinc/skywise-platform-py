Resources
=========

Everything requested by the skywise-platform is either a JSON resource or an Image resource.

----
JSON
----
Any resource that is not a tile is a JSON resource. You can inspect the data of any returned JSON resource using the
`json()` method. This will return a Python dictionary containing the raw serialized values returned from Platform.

.. code-block:: python

    >>> from skywiseplatform import Product
    >>> product = Production.find('weatherops-1hr-precipitation-forecast')
    >>> product.json()
    {
       u'styles':u'/products/170835d2-e9fe-11e4-b02c-1681e6b88ec1/styles',
       u'aggregationPeriodInMinutes':60,
       u'contentType':u'precipitation',
       u'name':u'weatherops-1hr-precipitation-forecast',
       u'frames':None,
       u'forecasts':u'/products/170835d2-e9fe-11e4-b02c-1681e6b88ec1/forecasts',
       u'source':u'weatherops',
       u'startTime':   u'2016-09-08T01:00:00   Z',
       u'coverage':{
          u'geometry':'{"type": "MultiPolygon", "coordinates": [[[[-179.5, -89.5], [-179.5, 89.5], [179.5, 89.5], [179.5, -89.5], [-179.5, -89.5]]]]}',
          u'type':u'Feature'
       },
       u'styleableLayers':[
          {
             u'attributes':[

             ],
             u'type':u'raster',
             u'name':u'precipitation',
             u'unit':{
                u'description':u'millimeters',
                u'label':u'mm'
             }
          }
       ],
       u'endTime':   u'2016-09-16T00:00:00   Z',
       u'id':u'170835d2-e9fe-11e4-b02c-1681e6b88ec1',
       u'description':u'WeatherOps 1-hour quantitative precipitation forecast'
    }

You can access top-level variables directly via object attributes:

.. code-block:: python

    >>> product.id
    u'170835d2-e9fe-11e4-b02c-1681e6b88ec1'
    >>> product.startTime
    datetime.datetime(2016, 9, 8, 1, 0, tzinfo=tzutc())
    >>> product.coverage
    {
       u'geometry':{
          u'type':u'MultiPolygon',
          u'coordinates':[
             [[(-179.5, -89.5),
               (-179.5, 89.5),
               (179.5, 89.5),
               (179.5, -89.5),
               (-179.5, -89.5)]]
          ]
       },
       u'type':u'Feature'
    }

Notice that when used in this way, the client deserializes the response values into more user-friendly formats. In this
case we get native Python datetime objects for start/endTime and geojson for our coverage.

------
Images
------
All tile requests are images. This library does not currently support products with MVTs. You can read in bytes for the
requested image using the `content()` method.

.. code-block:: python

    >>> tile = product.google_maps_tiles(0, 0, 0).pop()
    >>> with open('tile.tiff', 'w') as f:
    ...    f.write(tile.content())

You can then open up your tiff to inspect the data directly. We'll talk about tile methods in more depth later on.

----------
group_by()
----------
Almost all requests made with the client result in a list of resources being returned. The `group_by()` method makes it
easy to organize your results. `group_by()` allows you to specify an attribute shared by all elements in your resource
list and returns a dictionary that groups the resources by that attribute. Here's an example of how we could group all of
our Products by their content type attribute:

```python
    >>> from skywiseplatform import Product
    >>> products = Product.find()
    >>> products
    [<Product skywise-1hr-dewpoint-temperature-analysis>, ..., <Product weatherops-tropical-wind-speed-forecast>]
    >>> products[0].contentType
    u'dewpoint'
    >>> products.group('contentType')
    {
       u'dewpoint':[
          <Product skywise-1hr-dewpoint-temperature-analysis>,
          <Product skywise-southamerica-1hr-dewpoint-temperature-analysis>,
          <Product weatherops-1hr-dewpoint-temperature-forecast>,
          <Product weatherops-superconus-1hr-dewpoint-temperature-forecast>
       ],
       ...,
       u'wind-speed':[
          <Product skywise-1hr-wind-speed-analysis>,
          <Product skywise-southamerica-1hr-wind-speed-analysis>,
          <Product weatherops-1hr-wind-speed-forecast>,
          <Product weatherops-superconus-1hr-wind-speed-forecast>,
          <Product weatherops-tropical-wind-speed-forecast>
       ]
    }
```
