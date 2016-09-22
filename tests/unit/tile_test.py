from skywiserestclient import SkyWiseRequest
from skywiseplatform import BingMapsTile, GoogleMapsTile
from tests import load_fixture
from tests.unit import PlatformTest


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
