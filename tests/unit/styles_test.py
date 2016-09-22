from skywiseplatform import Style
from tests import load_fixture
from tests.unit import PlatformTest


class StyleTest(PlatformTest):

    def test_find(self):
        styles_json = load_fixture('styles')
        self.adapter.register_uri('GET', '/products/%s/styles' % (self.product.id,),
                                  json=styles_json)
        styles = Style.find(self.product.id)
        self.assertEquals(len(styles), 2)
