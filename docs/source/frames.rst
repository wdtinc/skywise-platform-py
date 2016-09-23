Frames
======
Frames represent a product's state at a moment or over an interval in time.
Once you have a frame, you can retrieve any of its datapoints or tiles.

Frame Requests
--------------

Basic Usage
~~~~~~~~~~~
Here's how to request the latest frames for a product.

.. code-block:: python

    from skywiseplatform import Product

    product = Product.find('skywise-24hr-precip-analysis')
    frames  = product.frames()

If you want to retrieve frames over a date range, use the start/end keyword arguments.

.. code-block:: python

    frames = product.frames(start='2015-05-01', end='2015-05-31')

**date/datetime keyword arguments in `skywise-platform` can be anything parseable by the arrow library.**

Forecast Frames
~~~~~~~~~~~~~~~
Products with forecasts link all frames to a particular forecast. The `frames()` method on a forecast product will only return
frames for the latest forecast. If you'd like to retrieve frames for a different forecast, you'll first need to retrieve
your forecast of interest using the product's `forecasts()` method. This will return all active forecasts. Here's an example
of retrieving frames for the latest forecast as well as the oldest forecast:

.. code-block:: python

    forecast_product = Product.find('weatherops-24hr-precip-forecast')

    # Retrieving Frames using Product.frames()
    frames = forecast_product.frames()

    # Is synonymous with retrieving frames for the latest forecast
    latest_forecast = product.forecasts().pop()
    frames = latest_forecast.frames()

    # Retrieve Forecasts (sorted from oldest to latest)
    oldest_forecast = product.forecasts().pop(0)

    # Retrieve Frames from a Specific Forecast
    frames = oldest_forecast.frames()

Datapoints
----------
A datapoint represents the value of a product's frame at a particular point on the globe. This value is derived from
the highest resolution tile that contains the point. Using datapoints saves you from the hassle of pulling down the tile
containing your point and inspecting the value for yourself.

.. code-block:: python

    >>> import arrow
    >>> from skywiseplatform import Product
    >>> product = Product.find('skywise-24hr-high-temperature-analysis')
    >>> frames = product.frames()
    >>> datapoints = [frame.datapoint(35.46, -97.52) for frame in frames]
    >>> for dp in datapoints:
    ...     print "Frame %s - %s - %.3f %s" % (dp.frame.id, dp.validTime, dp.value, dp.unit['label'])
    ...
    Frame 1f421458-3498-4193-b9c9-88874102ca25 - 2016-09-14 00:00:00+00:00 - 32.487 °C
    Frame a90e6a01-2935-4f37-a7c2-825a0d4b5bd6 - 2016-09-15 00:00:00+00:00 - 27.084 °C
    Frame 907714bd-f33a-4707-aa1a-8aad5ed0cd7a - 2016-09-16 00:00:00+00:00 - 28.496 °C
    Frame 188bf605-f07d-4322-8e9c-ac7b356a52ea - 2016-09-17 00:00:00+00:00 - 28.560 °C
    Frame 35ec9859-1e43-4b25-85b9-9ff0d2419ffa - 2016-09-18 00:00:00+00:00 - 29.350 °C
    Frame c0e34b8d-0367-4b7d-83e8-c6e6fdea11ee - 2016-09-19 00:00:00+00:00 - 31.525 °C
    Frame 86d5a13d-119a-4a49-a48d-cf8df5f7ba56 - 2016-09-20 00:00:00+00:00 - 35.735 °C
    Frame 2fe7432d-b33b-494d-91f0-9d1015114db9 - 2016-09-21 00:00:00+00:00 - 34.587 °C
    Frame 5c2b8012-262f-43e1-984c-deb8b613b511 - 2016-09-22 00:00:00+00:00 - 31.879 °C
    Frame 003e4208-fd80-4561-a0e0-83af52a6273b - 2016-09-23 00:00:00+00:00 - 32.031 °C

Tiles
-----
You can request tiles for a frame using either a Google Maps XYZ-coordinate or with a Bing Maps quadkey. Here's how to
create a stack of tiles at a particular coordinate for your latest frames:

.. code-block:: python

   from skywiseplatform import Product

   # Get tiles for the latest frames
   product = Product.find('skywise-24hr-high-temperature-analysis')

   # Google Maps
   tiles = [frame.tile(x=0, y=0, z=1) for frame in product.frames()]

   # Bing Maps
   tiles = [frame.tile(quadkey="0") for frame in product.frames()]

Once you've received the tile, you can retrieve its contents using the `content()` method.

.. code-block:: python

    tile = tiles.pop()
    with open('my_tile.tiff', 'w') as f:
        f.write(tile.content())

Styles
~~~~~~
You can specify a style for your tile requests using either a style id or Style object:

.. code-block:: python

    # Grab the latest frame
    frame = product.frames().pop()

    # Use a Style object
    style = product.styles().pop()
    stylized_tile = frame.tile(x=0, y=0, z=1, style=style)

    # Use a style id
    stylized_tile = frame.tile(x=0, y=0, z=1, style="my-style-id")

Media Types
~~~~~~~~~~~
You can inspect which media types are available for your frame using the `mediaTypes` attribute:

.. code-block:: python

    >>> frame = product.frames().pop()
    >>> frame.mediaTypes
    ["image/jpeg", "image/png", "image/tiff"]

By default, tile requests will use "image/tiff" if it is available. You can also specify any of the media types supported by
the frame:

.. code-block:: python

    >>> png = frame.tile(x=0, y=0, z=1, media_type='image/png')
    >>> jpg = frame.tile(x=0, y=0, z=1, media_type='image/jpeg')

Async
-----
If you're needing to make a large number of tile or datapoint calls, requesting them one at a time will most likely be
too slow. You can fire off batches of tile calls using the async methods provided for both datapoints and tiles in conjunction
with `map_async()`:

.. code-block:: python

    from skywiseplatform import Product, map
    product = Product.find('skywise-24hr-high-temperature-analysis')
    frames = product.frames()

    # Request Multiple Tiles at Once
    tile_batch = [frame.tile_async(x=0, y=0, z=1) for frame in product.frames()]
    tiles = map_async(tile_batch)

    # Request Multiple Datapoints at Once
    dp_batch = [frame.datapoint_async(35.46, -97.52) for frame in frames]
    datapoints = map_async(dp_batch)
