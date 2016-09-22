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
containing your point and inspecting the value for yourself. Here, we'll retrieve the latest precip data points for OKC:

.. code-block:: python

    >>> import arrow
    >>> from skywiseplatform import Product
    >>> product = Product.find('skywise-24hr-precipitation-analysis')
    >>> frames = product.frames()
    >>> datapoints = [frame.datapoint(35.46, -97.52) for frame in frames]
    >>> for dp in datapoints:
    ...     print "Frame %s - %s - %.3f" % (dp.frame.id, dp.validTime, dp.value)
    Frame 8150dad4-a49c-4fc0-b188-18113cf9b826 - 2016-09-16 00:00:00+00:00 - 24.954
    Frame fd6eed60-2685-45ad-b47f-1be2d98ecd91 - 2016-09-15 00:00:00+00:00 - 6.221
    Frame 6de68003-6185-4600-adc3-ccecb816abb6 - 2016-09-14 00:00:00+00:00 - 0.634
    Frame 4b9af9e4-c717-415d-a464-b879fab05787 - 2016-09-13 00:00:00+00:00 - 0.000
    Frame 073d9ea0-f0e4-4d67-b240-291fdb2d4e85 - 2016-09-12 00:00:00+00:00 - 0.000
    Frame 5afa8fa5-9b0f-4d97-a3cf-4e8d155964b9 - 2016-09-11 00:00:00+00:00 - 26.137
    Frame ded6f3d4-856b-4ef9-aa5b-3c21561ce02f - 2016-09-10 00:00:00+00:00 - 0.901

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
with `map()`:

.. code-block:: python

    from skywiseplatform import Product, map
    product = Product.find('skywise-24hr-high-temperature-analysis')
    frames = product.frames()

    # Request Multiple Tiles at Once
    tile_batch = [frame.tile_async(x=0, y=0, z=1) for frame in product.frames()]
    tiles = map(tile_batch)

    # Request Multiple Datapoints at Once
    dp_batch = [frame.datapoint_async(35.46, -97.52) for frame in frames]
    datapoints = map(dp_batch)
