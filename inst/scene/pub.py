from . import FeatureRule, SceneBase
from .shop import Shop


class Pub(SceneBase):
    """酒館"""

    def feature_rules(self) -> [FeatureRule]:
        rules: [FeatureRule] = []
        # 左下角秘境
        rules.append(FeatureRule('trial_icon.jpg'))

        # 右下角店舖
        rules.append(FeatureRule('shop_icon.jpg'))

        return rules

    def fetch_scene_paths(self, cls: 'SceneBase') -> [FeatureRule]:
        if cls == Shop:
            yield FeatureRule('shop_icon.jpg')
        
        # default
        yield FeatureRule('shop_icon.jpg')
