Tiles
=====
There are two types of tiles supported in `skywiseplatform`: GoogleMapsTile and BingMapsTile:

.. code-block:: python

   from skywiseplatform import Product

   # Get tiles for the latest frames
   product = Product.find('skywise-24hr-high-temperature-analysis')
   google_tiles = product.google_maps_tiles(0, 0, 1)
   bing_tiles = product.bing_maps_tiles('0')

   # Get tiles over a particular date range
   import arrow
   start = arrow.get().replace(days=-7).datetime
   end = arrow.get().replace(days=-1).datetime
   last_weeks_precip_tiles = product.google_maps_tiles(0, 0, 0, start=start, end=end)

-------------
Asynchronous
-------------

Sometimes, however, we may want to create tile requests on multiple products asynchronously and then map them together all at once rather than in two separate calls to increase performance. Let's look at an example of how we might request tiles for precipitation on both historical and forecast products. This can be useful if you are trying to accumulate tile values over a span of time that extends over multiple products:

.. code-block:: python

  from skywiseplatform import Product, map_requests

  precip_analysis = Product.find('skywise-24hr-precipitation-analysis')
  precip_forecast = Product.find('weatherops-24hr-precipitation-forecast')

  analysis_start = arrow.get().floor('day').replace(days=-7).datetime # A Week Ago
  analysis_end = analysis_start.replace(days=-1).datetime # Yesterday
  forecast_start = arrow.get().floor('day').datetime # Today
  forecast_end = forecast_start.replace(days=+7).datetime # A Week From Now

  analysis_tiles = precip_analysis.google_maps_tiles_async(0, 0, 1, start=analysis_start, end=analysis_end)
  forecast_tiles = precip_forecast.google_maps_tiles_async(0, 0, 1, start=forecast_start, end=forecast_end)

  tile_requests = []
  tile_requests.extend(analysis_tiles)
  tile_requests.extend(forecast_tiles)

  tiles = map_requests(tiles)

This approach can be used to arbitrarily make asynchronous calls on a number of different tiles, regardless of their originating product.


---------
Tile Sets
---------

To grab all tiles within an extent, you can use tile sets. Here's how we'd grab all tiles within the OKC metro over a period of time:

.. code-block:: python

  precip_analysis = Product.find('skywise-24hr-precipitation-analysis')

  okc_bounding_box = ((37.26, -94.17), (33.37, -103.49))

  start = arrow.get('2015-06-13').datetime
  end = arrow.get('2015-06-20').datetime
  tiles = precip_analysis.google_maps_tileset(okc_bounding_box, start=start, end=end)


We now have all tiles for our bounding box over our specified period. Note that we did not specify a zoom level for our tiles. By default, this call will use the native resolution of our product frames. If you do want a specific zoom level, you may pass the 'zoom' parameter into the function.

This list of tiles is jumbled together. Let's use our `group()` function to organize our tiles by their frame attribute's validTime:

.. code-block:: python

  start = arrow.get('2015-06-13').floor('day').datetime
  end = start.replace(days=+7).datetime
  tiles = precip_analysis.google_maps_tileset(okc_bounding_box, start=start, end=end)
  organized_tiles = tiles.group(['frame.validTime'])
  """
  { datetime(2015, 06, 13, ...): [<Tile 0>, <Tile 1>, ... <Tile N>],
    datetime(2015, 06, 14, ...): [<Tile 0>, <Tile 1>, ... <Tile N>],
    ...
    datetime(2015, 06, 20, ...): [<Tile 0>, <Tile 1>, ... <Tile N>]
  }
  """

From here, we can easily use other tools to stitch together the tiles.
