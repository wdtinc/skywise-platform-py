An Introduction to Platform
===========================

What is Platform?
-----------------
Platform is a distributed weather tile service that provides users access to WDT's expansive collection of raster and vector weather
tiles. Its primary use case is driving map layers, but it can be utilized for much more. If you know how to work with
Platform's native tile formats, ([GeoTiff]() and [MVT]()) you can build any kind of data store you want in a variety of
temporal and spatial resolutions. This library helps you plug Platform data into your Python app without worrying
about those low-level details.

- Want to build an app that serves time series data for a variety of user parameters?
- Want to ingest large amounts of model data into your big data system?
- Want to do historical analysis on an area of interest?
- Want to add beautiful (and highly accurate) weather layers to a map?

With Platform, you can do all of that.

How does it work?
-----------------
At the highest level of abstraction, all data in Platform belongs to a [Product](). Products vary by the
areas on the globe which they cover (known as their [coverage]()), the type of content they provide (precipitation,
temperature, etc), whether they're raster or vector, if they provide forecast or
historical data, and more. Platform also helps by giving you ways to figure out the best product to use for your
job. [More on that later.]()

Data for a product is stored as tiles

What does this library allow you to do?
---------------------------------------
- Work with Platform data using native Python data types.
- Ask for the data you want, and let the library make a large number number of calls to Platform asynchronously on your behalf.
- Work with popular Python data structures and visualization libraries in the scientific community.

What does it NOT do?
--------------------
