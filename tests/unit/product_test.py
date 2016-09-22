from skywiseplatform import Product
from tests import load_fixture
from tests.unit import PlatformTest


class ProductTest(PlatformTest):

    def test_find(self):
        products_json = load_fixture('products')
        self.adapter.register_uri('GET', '/products', json=products_json)
        products = Product.find()
        self.assertEqual(len(products), 63)

    def test_find_with_id(self):
        product_json = load_fixture('product')
        self.adapter.register_uri('GET', '/products/%s' % (product_json['id']),
                                  json=product_json)
        product = Product.find(product_json['id'])
        self.assertIsNotNone(product.id)

    def test_styles(self):
        product_json = load_fixture('product')
        self.adapter.register_uri('GET', '/products/%s' % (product_json['id']),
                                  json=product_json)
        product = Product.find(product_json['id'])

        styles_json = load_fixture('styles')
        self.adapter.register_uri('GET', '/products/%s/styles' % (product.id,),
                                  json=styles_json)
        styles = self.product.styles()
        self.assertEquals(len(styles), 2)

    def test_forecasts(self):
        forecast_product_json = load_fixture('forecast_product')
        self.adapter.register_uri('GET', '/products/%s' % forecast_product_json['id'],
                                  json=forecast_product_json)
        forecast_product = Product.find(forecast_product_json['id'])

        forecasts_json = load_fixture('forecasts')
        self.adapter.register_uri('GET', '/products/%s/forecasts' % forecast_product.id,
                                  json=forecasts_json)
        forecasts = forecast_product.forecasts()
        self.assertEqual(len(forecasts), 2)

    def test_analysis_frames(self):
        product_json = load_fixture('product')
        self.adapter.register_uri('GET', '/products/%s' % (product_json['id']),
                                  json=product_json)
        product = Product.find(product_json['id'])

        frames_json = load_fixture('frames')
        self.adapter.register_uri('GET', '/products/%s/frames' % product.id,
                                  json=frames_json)
        frames = product.frames()
        self.assertEquals(len(frames), 2)

    def test_forecast_frames(self):
        forecast_product_json = load_fixture('forecast_product')
        self.adapter.register_uri('GET', '/products/%s' % forecast_product_json['id'],
                                  json=forecast_product_json)
        forecast_product = Product.find(forecast_product_json['id'])

        forecasts_json = load_fixture('forecasts')
        self.adapter.register_uri('GET', '/products/%s/forecasts' % forecast_product.id,
                                  json=forecasts_json)

        frames_json = load_fixture('frames')
        self.adapter.register_uri('GET', '/forecasts/92267afc-1e72-4408-a94b-62b40881ea4e/frames',
                                  json=frames_json)
        frames = forecast_product.frames()
        self.assertEqual(len(frames), 2)
