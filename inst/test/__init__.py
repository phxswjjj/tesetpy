from inst.scene import FeatureRule


def match(rules: [FeatureRule], screen_img) -> bool:
    if not rules:
        return False

    for rule in rules:
        rule: FeatureRule
        if not rule.match(screen_img):
            return False
    return True
