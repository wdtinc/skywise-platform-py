import arrow
import requests_mock
from unittest import TestCase

from skywiserestclient import SkyWiseRequest
from skywiseplatform import (BingMapsTile, Datapoint, Forecast, ForecastFrame, GoogleMapsTile,
                             PlatformResource, Product, ProductFrame, Style)
from tests import load_fixture


class PlatformTest(TestCase):

    def setUp(self):
        PlatformResource.set_site('http://my.skywise.host')
        PlatformResource.set_user('my-skywise-user')
        PlatformResource.set_password('my-skywise-password')
        PlatformResource.set_use_session_for_async(True)

        self.adapter = requests_mock.Adapter()
        session = PlatformResource.get_session()
        session.mount('http://my.skywise.host', self.adapter)

        product_json = load_fixture('product')
        self.adapter.register_uri('GET', '/products/%s' % (product_json['id']),
                                  json=product_json)
        self.product = Product.find(product_json['id'])

    def _register_frames(self):
        frames_json = load_fixture('frames')
        self.adapter.register_uri('GET', '/products/%s/frames' % (self.product.id,),
                                  json=frames_json)
        return self.product.get_frames()


class ProductTest(PlatformTest):

    def test_get_styles(self):
        product_json = load_fixture('product')
        self.adapter.register_uri('GET', '/products/%s' % (product_json['id']),
                                  json=product_json)
        self.product = Product.find(product_json['id'])

        styles_json = load_fixture('styles')
        self.adapter.register_uri('GET', '/products/%s/styles' % (self.product.id,),
                                  json=styles_json)
        styles = self.product.get_styles()
        self.assertEquals(len(styles), 2)

    def test_get_frames(self):
        frames_json = load_fixture('frames')
        self.adapter.register_uri('GET', '/products/%s/frames' % self.product.id,
                                  json=frames_json)
        frames = self.product.get_frames()
        self.assertEquals(len(frames), 2)

    def test_get_forecast_frames(self):
        scenario = load_fixture('forecast_frame_scenario')

        product_json = scenario['product']
        self.adapter.register_uri('GET', '/products/my-forecast-product',
                                  json=product_json)

        forecasts = scenario['forecasts']
        self.adapter.register_uri('GET', '/products/my-forecast-product/forecasts',
                                  json=forecasts)

        frames = scenario['frames']
        self.adapter.register_uri('GET', '/forecasts/forecast-a/frames',
                                  json=frames['forecast-a'])
        self.adapter.register_uri('GET', '/forecasts/forecast-b/frames',
                                  json=frames['forecast-b'])

        product = Product.find(product_json['id'])
        frames = product.get_frames(start=arrow.get('2014-09-01').date(),
                                    end=arrow.get('2014-09-03').date())
        self.assertEqual(len(frames), 3)
        frames.sort(key=lambda f: f.validTime)
        self.assertEqual(frames[0].id, 'frame-a-1')
        self.assertEqual(frames[1].id, 'frame-b-1')
        self.assertEqual(frames[2].id, 'frame-b-2')

        frames = product.get_frames()
        self.assertEqual(len(frames), 2)
        frames.sort(key=lambda f: f.validTime)
        self.assertEqual(frames[0].id, 'frame-b-1')
        self.assertEqual(frames[1].id, 'frame-b-2')

    def test_bing_maps_tiles(self):
        frames = self._register_frames()

        tile_tiff = load_fixture('tile', extension='tiff')
        for frame in frames:
            self.adapter.register_uri('GET', '/frames/%s/tile/0' % (frame.id,),
                                      content=tile_tiff)

        tiles = self.product.bing_maps_tiles('0', use_session=True)
        self.assertEquals(len(tiles), 2)

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


class StyleTest(PlatformTest):

    def test_find(self):
        styles_json = load_fixture('styles')
        self.adapter.register_uri('GET', '/products/%s/styles' % (self.product.id,),
                                  json=styles_json)
        styles = Style.find(self.product.id)
        self.assertEquals(len(styles), 2)


class DataPointTest(PlatformTest):

    def test_find(self):
        frame = self._register_frames().pop()
        datapoint_json = load_fixture('datapoints').pop()
        self.adapter.register_uri('GET', '/frames/%s/datapoint/35.0/-97.0' % (frame.id,),
                                  json=datapoint_json)
        dp = Datapoint.find(frame, 35.0, -97.0)
        self.assertTrue(isinstance(dp, Datapoint))
        self.assertEqual(dp.value, 15.2)
        self.assertEqual(dp.pixel['row'], 52)
        self.assertEqual(dp.pixel['column'], 213)
        self.assertEqual(dp.frame.id, frame.id)

    def test_find_async(self):
        frame = self._register_frames().pop()
        dpr = Datapoint.find_async(frame, 35.0, -97.0)
        self.assertEqual(dpr.tags()['frame'].id, frame.id)


class ForecastTest(PlatformTest):

    def test_find(self):
        forecast_json = load_fixture('forecasts').pop()
        self.adapter.register_uri('GET', '/forecasts/%s' % (forecast_json['id']),
                                  json=forecast_json)
        forecast = Forecast.find(forecast_json['id'])
        self.assertEqual(forecast.initTime, arrow.get('2014-09-01T12:00:00Z').datetime)

    def test_find_by_product(self):
        forecasts_json = load_fixture('forecasts')
        self.adapter.register_uri('GET', '/products/%s/forecasts' % (self.product.id),
                                  json=forecasts_json)
        forecasts = Forecast.find(product_id=self.product.id)
        self.assertEqual(len(forecasts), 2)


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


class TileTest(PlatformTest):

    def test_find_google_maps_tile(self):
        tile_tiff = load_fixture('tile', extension='tiff')
        self.adapter.register_uri('GET', '/frames/%s/tile/8/0/1' % ('frame-id',),
                                  content=tile_tiff)
        tile = GoogleMapsTile.find('frame-id', 0, 1, 8)
        self.assertTrue(isinstance(tile, GoogleMapsTile))

    def test_find_google_maps_tile_async(self):
        tile_request = GoogleMapsTile.find_async('frame-id', 0, 1, 8)
        self.assertTrue(isinstance(tile_request, SkyWiseRequest))
        self.assertEqual(tile_request.tags()['x'], 0)
        self.assertEqual(tile_request.tags()['y'], 1)
        self.assertEqual(tile_request.tags()['z'], 8)

    def test_find_bing_maps_tile(self):
        tile_tiff = load_fixture('tile', extension='tiff')
        self.adapter.register_uri('GET', '/frames/%s/tile/023' % ('frame-id',),
                                  content=tile_tiff)
        tile = BingMapsTile.find('frame-id', "023")
        self.assertTrue(isinstance(tile, BingMapsTile))

    def test_find_bing_maps_tile_async(self):
        tile_request = BingMapsTile.find_async('frame-id', "023")
        self.assertTrue(isinstance(tile_request, SkyWiseRequest))
        self.assertEqual(tile_request.tags()['quadkey'], "023")

    def test_google_maps_tileset(self):
        tile_tiff = load_fixture('tile', extension='tiff')
        coordinates = []
        [[coordinates.append((x, y)) for y in range(99, 103)] for x in range(54, 61)]
        for coord in coordinates:
            self.adapter.register_uri('GET', '/frames/frame-id/tile/8/%i/%i' % (coord[0], coord[1]),
                                      content=tile_tiff)

        ne_corner = (37.063944, -94.400024)
        sw_corner = (33.559707, -103.189087)
        tiles = GoogleMapsTile.tileset('frame-id', (ne_corner, sw_corner), 8)
        self.assertEqual(len(tiles), 28)
        for tile in tiles:
            self.assertEqual(tile.z, 8)
            coordinates.remove((tile.x, tile.y))
        self.assertFalse(coordinates, 'Some coordinates did not have tiles.')
