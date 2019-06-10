from . import SceneBase, FeatureRule


class Shop(SceneBase):
    """店舖"""
    def feature_rules(self) -> [FeatureRule]:
        rules: [FeatureRule] = []
        # 左下角城鎮
        rules.append(FeatureRule('town_icon.jpg'))

        # 右下角酒館
        rules.append(FeatureRule('pub_icon.jpg'))
        
        return rules