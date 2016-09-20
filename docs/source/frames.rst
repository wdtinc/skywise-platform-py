Frames
======
A frame represents a product's state at a moment or over an interval in time.

Basic Frame Requests
--------------------
Here's how to request the latest frames for any product.

.. code-block:: python

    from skywiseplatform import Product

    product = Product.find('skywise-24hr-precip-analysis')
    frames  = product.get_frames()

If you want to retrieve frames over a date range, use the start/end keyword arguments. To retrieve all of the
daily precip frames in the month of May 2015:

.. code-block:: python

    frames = product.get_frames(start='2015-05-01', end='2015-05-31')

Forecast Frames
---------------
If you're just interested in frames for the latest forecast, you can retrieve them just as you would any analysis product.
The client will use the latest forecast when making frames requests in this manner:

.. code-block:: python

    product = Product.find('weatherops-24hr-precipitation-forecast')
    frames = product.get_frames()

Nothing new here. The main thing to know is that under the hood, we're actually getting frames for the latest
forecast.

If we're using a start/end range, the client will fulfill the frames request using any active forecasts on the product,
prioritizing the most current and working backward. That means that if your requested period overlaps two forecasts, the
client will leverage frames from both to fulfill the request.

If you only need to retrieve frames for a particular forecast, forecast resources also support the `get_frames()`
method:

.. code-block:: python

    # Obtain a forecast from the product
    product = Product.find('weatherops-24hr-precipitation-forecast')
    forecasts = product.get_forecasts()
    forecast = forecasts.pop()
    frames = forecast.get_frames()

    # Request the forecast directly
    from skywiseplatform import Forecast
    forecast = Forecast.find('my-forecast-uuid')
    frames = forecast.get_frames()
