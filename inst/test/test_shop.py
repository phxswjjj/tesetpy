import cv2

from inst.scene import FeatureRule

shop_img = cv2.imread('inst/scene/img/test_shop.jpg')
pub_img = cv2.imread('inst/scene/img/test_pub.jpg')


def _match(rules: [FeatureRule], screen_img) -> bool:
    if not rules:
        return False

    for rule in rules:
        rule: FeatureRule
        if not rule.match(screen_img):
            return False
    return True

def test_collect_res():
    rule_stone = FeatureRule('shop_res_stone.jpg', 0.95)
    rule_magic = FeatureRule('shop_res_magic.jpg')
    assert _match([rule_stone, rule_magic], shop_img)

    loc_1st = rule_stone.get_loc_1st(shop_img)
    loc_center = rule_stone.get_loc_center(shop_img)
    assert loc_center == (loc_1st[0] + 11, loc_1st[1] + 5)
    assert loc_center[0] > 1530 and loc_center[0] < 1600
    assert loc_center[1] > 100 and loc_center[1] < 175

    assert not _match([rule_stone, rule_magic], pub_img)

