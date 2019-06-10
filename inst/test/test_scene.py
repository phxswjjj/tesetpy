import cv2

from inst.scene import FeatureRule, SceneBase
from inst.scene.pub import Pub
from inst.scene.shop import Shop

shop_img = cv2.imread('inst/scene/img/test_shop.jpg')
pub_img = cv2.imread('inst/scene/img/test_pub.jpg')

def _match(s: SceneBase, screen_img) -> bool:
    rules = s.feature_rules()
    if not rules:
        return False
    
    for rule in rules:
        rule: FeatureRule
        if not rule.match(screen_img):
            return False
    return True

def test_shop():
    shop = Shop()
    assert _match(shop, shop_img)
    assert not _match(shop, pub_img)

def test_pub():
    pub = Pub()
    assert _match(pub, pub_img)
    assert not _match(pub, shop_img)
