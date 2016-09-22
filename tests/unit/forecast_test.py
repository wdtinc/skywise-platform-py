import arrow

from skywiseplatform import Forecast
from tests import load_fixture
from tests.unit import PlatformTest


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

    def test_get_frames(self):
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

    def test_forecast_order_newest_to_oldest(self):
        raise Exception()
