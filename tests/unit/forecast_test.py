import arrow

from skywiseplatform import Product
from skywiseplatform.forecast import Forecast, ProductForecast
from tests import load_fixture
from tests.unit import PlatformTest


class ForecastTest(PlatformTest):

    def test_find(self):
        forecast_json = load_fixture('forecasts').pop()
        self.adapter.register_uri('GET', '/forecasts/%s' % (forecast_json['id']),
                                  json=forecast_json)
        forecast = Forecast.find(forecast_json['id'])
        self.assertEqual(forecast.id, u'ed5e547b-ab1d-4e84-885e-3a7d3dec9b93')

    def test_find_by_product(self):
        forecasts_json = load_fixture('forecasts')
        self.adapter.register_uri('GET', '/products/%s/forecasts' % (self.product.id),
                                  json=forecasts_json)
        forecasts = ProductForecast.find(self.product.id)
        self.assertEqual(len(forecasts), 3)

    def test_frames(self):
        product_json = load_fixture('forecast_product')
        self.adapter.register_uri('GET', '/products/%s' % product_json['id'],
                                  json=product_json)
        product = Product.find(product_json['id'])

        forecasts_json = load_fixture('forecasts')
        self.adapter.register_uri('GET', '/products/%s/forecasts' % product.id,
                                  json=forecasts_json)
        forecast = product.forecasts().pop()
        self.assertEqual(forecast.id, u'4a61c817-3fc0-4dec-80ab-25936d73b2d7',
                         'Last forecast in list should be the most current.')

        frames_json = load_fixture('forecast_frames')
        self.adapter.register_uri('GET', '/forecasts/%s/frames' % forecast.id,
                                  json=frames_json)
        frames = forecast.frames()
        self.assertEqual(len(frames), 10)
