import cv2

from inst.scene import FeatureRule

from . import match

shop_img = cv2.imread('inst/scene/img/test_shop.jpg')
shop2_img = cv2.imread('inst/scene/img/test_shop2.jpg')
pub_img = cv2.imread('inst/scene/img/test_pub.jpg')

def test_collect_res():
    rule_stone = FeatureRule('shop_res_stone.jpg', 0.95)
    rule_magic = FeatureRule('shop_res_magic.jpg')
    assert match([rule_stone, rule_magic], shop_img)
    assert match([rule_stone, rule_magic], shop2_img)

    loc_1st = rule_stone.get_loc_1st(shop_img)
    loc_center = rule_stone.get_loc_center(shop_img)
    assert loc_center == (loc_1st[0] + 11, loc_1st[1] + 5)
    assert loc_center[0] > 1530 and loc_center[0] < 1600
    assert loc_center[1] > 100 and loc_center[1] < 175

    assert not match([rule_stone, rule_magic], pub_img)

def test_item_completed():
    rule_item_completed = FeatureRule('item_completed.jpg', 0.95)
    assert not rule_item_completed.match(shop_img)
    assert rule_item_completed.match(shop2_img)
