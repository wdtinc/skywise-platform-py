import requests_mock
from unittest import TestCase

from skywiseplatform import PlatformResource, Product
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
