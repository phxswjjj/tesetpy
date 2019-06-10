from . import SceneBase, FeatureRule


class Pub(SceneBase):
    """酒館"""
    def feature_rules(self) -> [FeatureRule]:
        rules: [FeatureRule] = []
        # 左下角秘境
        rules.append(FeatureRule('trial_icon.jpg'))

        # 右下角店舖
        rules.append(FeatureRule('shop_icon.jpg'))
        
        return rules
