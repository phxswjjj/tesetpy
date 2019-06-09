from . import SceneBase, FeatureRule


class Shop(SceneBase):
    def feature_rules(self) -> [FeatureRule]:
        rules: [FeatureRule] = []
        # 左下角城鎮
        rules.append(FeatureRule('town_icon.jpg'))

        # 右下角酒館
        
        return rules