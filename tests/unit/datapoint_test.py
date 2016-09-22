from skywiseplatform import Datapoint
from tests import load_fixture
from tests.unit import PlatformTest


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
