Datapoints
==========
A datapoint represents the value of a product's frame at a particular point on the globe. This value is derived from
the highest resolution tile that contains the point. This saves you from the hassle of pulling down a tile and inspecting
it yourself. There are a few ways to obtain datapoints.

Retrieving Datapoints
---------------------

----------
By Product
----------
The easiest way is through a product. Instead of worrying about the specific frames being used to call your datapoints,
just let your product object take care of that for you. Let's create a time series for a 7-day precipitation forecast of
OKC using datapoints:

.. code-block:: python

    >>> import arrow
    >>> from skywiseplatform import Product
    >>> product = Product.find('weatherops-24hr-precipitation-forecast')
    >>> start = arrow.get().floor('day').replace(days=+1)
    >>> end = arrow.get().floor('day').replace(days=+7)
    >>> datapoints = product.get_datapoints(35.46, -97.52, start=start, end=end)
    >>> for dp in datapoints:
    ...     print "Frame %s - %s - %.3f" % (dp.frame.id, dp.validTime, dp.value)
    Frame 8150dad4-a49c-4fc0-b188-18113cf9b826 - 2016-09-16 00:00:00+00:00 - 24.954
    Frame fd6eed60-2685-45ad-b47f-1be2d98ecd91 - 2016-09-15 00:00:00+00:00 - 6.221
    Frame 6de68003-6185-4600-adc3-ccecb816abb6 - 2016-09-14 00:00:00+00:00 - 0.634
    Frame 4b9af9e4-c717-415d-a464-b879fab05787 - 2016-09-13 00:00:00+00:00 - 0.000
    Frame 073d9ea0-f0e4-4d67-b240-291fdb2d4e85 - 2016-09-12 00:00:00+00:00 - 0.000
    Frame 5afa8fa5-9b0f-4d97-a3cf-4e8d155964b9 - 2016-09-11 00:00:00+00:00 - 26.137
    Frame ded6f3d4-856b-4ef9-aa5b-3c21561ce02f - 2016-09-10 00:00:00+00:00 - 0.901

-----------
By Frame Id
-----------
Alternatively, if you already have a frame object or id, you can use either with the Datapoint class directly.

.. code-block:: python

    >>> from skywiseplatform import Datapoint
    >>> datapoint = Datapoint.find('8150dad4-a49c-4fc0-b188-18113cf9b826', 35.46, -97.52)
    >>> datapoint.frame.id
    u'8150dad4-a49c-4fc0-b188-18113cf9b826'
    >>> datapoint.validTime
    datetime.datetime(2016, 9, 16, 0, 0, tzinfo=tzutc())
    >>> datapoint.value
    24.9543170929
