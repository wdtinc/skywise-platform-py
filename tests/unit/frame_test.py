from skywiseplatform import ForecastFrame, ProductFrame, map_async
from tests import load_fixture
from tests.unit import PlatformTest


class FrameTest(PlatformTest):

    def test_product_frame(self):
        frames_json = load_fixture('frames')
        self.adapter.register_uri('GET', '/products/%s/frames' % (self.product.id,),
                                  json=frames_json)
        frames = ProductFrame.find(self.product.id)
        self.assertTrue(len(frames), 2)

    def test_forecast_frame(self):
        frames_json = load_fixture('frames')
        self.adapter.register_uri('GET', '/forecasts/%s/frames' % ('forecast-id',),
                                  json=frames_json)
        frames = ForecastFrame.find('forecast-id')
        self.assertTrue(len(frames), 2)

    def test_google_maps_tiles(self):
        frame = self._register_frames().pop()
        tile_tiff = load_fixture('tile', extension='tiff')
        self.adapter.register_uri('GET', '/frames/%s/tile/1/0/0' % frame.id,
                                  content=tile_tiff)
        tile = frame.tile(x=0, y=0, z=1)
        self.assertIsNotNone(tile.content())

    def test_google_maps_tiles_async(self):
        frames = self._register_frames()
        tile_tiff = load_fixture('tile', extension='tiff')
        for frame in frames:
            self.adapter.register_uri('GET', '/frames/%s/tile/1/0/0' % frame.id,
                                      content=tile_tiff)
        tile_batch = [frame.tile_async(x=0, y=0, z=1) for frame in frames]
        tiles = map_async(tile_batch)
        self.assertEqual(len(tiles), len(frames))

    def test_bing_maps_tiles(self):
        frame = self._register_frames().pop()
        tile_tiff = load_fixture('tile', extension='tiff')
        self.adapter.register_uri('GET', '/frames/%s/tile/0' % frame.id,
                                  content=tile_tiff)
        tile = frame.tile(quadkey="0")
        self.assertIsNotNone(tile.content())

    def test_bing_maps_tiles_async(self):
        frames = self._register_frames()
        tile_tiff = load_fixture('tile', extension='tiff')
        for frame in frames:
            self.adapter.register_uri('GET', '/frames/%s/tile/0' % frame.id,
                                      content=tile_tiff)
        tile_batch = [frame.tile_async(quadkey="0") for frame in frames]
        tiles = map_async(tile_batch)
        self.assertEqual(len(tiles), len(frames))

    def test_datapoints(self):
        frame = self._register_frames().pop()
        datapoint_json = load_fixture('datapoint')
        self.adapter.register_uri('GET', '/frames/%s/datapoint/35.0/-97.0' % frame.id,
                                  json=datapoint_json)
        datapoint = frame.datapoint(35.0, -97.0)
        self.assertEqual(datapoint.value, 0.296531558)

    def test_datapoints_async(self):
        frames = self._register_frames()
        datapoint_json = load_fixture('datapoint')
        for frame in frames:
            self.adapter.register_uri('GET', '/frames/%s/datapoint/35.0/-97.0' % frame.id,
                                      json=datapoint_json)
        datapoint_batch = [frame.datapoint_async(35.0, -97.0) for frame in frames]
        datapoints = map_async(datapoint_batch)
        self.assertEqual(len(datapoints), len(frames))
