from skywiseplatform import ForecastFrame, ProductFrame
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
        frames = self._register_frames()

        tile_tiff = load_fixture('tile', extension='tiff')
        for frame in frames:
            self.adapter.register_uri('GET', '/frames/%s/tile/0/0/0' % (frame.id,),
                                      content=tile_tiff)

        tiles = self.product.google_maps_tiles(0, 0, 0)
        self.assertEquals(len(tiles), 2)

    def test_google_maps_tiles_async(self):
        frames = self._register_frames()

        tile_requests = self.product.google_maps_tiles_async(0, 0, 0)
        self.assertEquals(len(tile_requests), 2)
        for tr in tile_requests:
            self.assertTrue(isinstance(tr, SkyWiseRequest))
            self.assertEqual(tr.tags()['product'].id, self.product.id)
            frame_match = False
            for frame in frames:
                if frame.id == tr.tags()['frame'].id:
                    frame_match = True
            self.assertTrue(frame_match)

    def test_bing_maps_tiles(self):
        frames = self._register_frames()

        tile_tiff = load_fixture('tile', extension='tiff')
        for frame in frames:
            self.adapter.register_uri('GET', '/frames/%s/tile/0' % (frame.id,),
                                      content=tile_tiff)

        tiles = self.product.bing_maps_tiles('0', use_session=True)
        self.assertEquals(len(tiles), 2)

    def test_get_datapoints(self):
        frames = self._register_frames()
        datapoints_json = load_fixture('datapoints')
        for i, frame in enumerate(frames):
            self.adapter.register_uri('GET', '/frames/%s/datapoint/35.0/-97.0' % (frame.id,),
                                      json=datapoints_json[i])
        datapoints = self.product.get_datapoints(35.0, -97.0)
        self.assertEqual(len(datapoints), 2)

    def test_get_datapoints_async(self):
        frames = self._register_frames()

        datapoint_requests = self.product.get_datapoints_async(35.0, -97.0)
        self.assertEquals(len(datapoint_requests), 2)
        for dp in datapoint_requests:
            self.assertTrue(isinstance(dp, SkyWiseRequest))
            self.assertEqual(dp.tags()['product'].id, self.product.id)
            frame_match = False
            for frame in frames:
                if frame.id == dp.tags()['frame'].id:
                    frame_match = True
            self.assertTrue(frame_match)
