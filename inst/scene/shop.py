from . import SceneBase, FeatureRule


class Shop(SceneBase):
    def feature_rules(self) -> [FeatureRule]:
        rules: [FeatureRule] = []
        # 左上角帳號
        rules.append(FeatureRule(155, 40, '#FFE7BB'))
        rules.append(FeatureRule(170, 42, '#FFE7BB'))

        # 左下角城鎮
        rules.append(FeatureRule(61, 878, '#D61400'))
        rules.append(FeatureRule(61, 885, '#FDF1A8'))

        # 右下角酒館
        rules.append(FeatureRule(1533, 877, '#DA8F58'))
        rules.append(FeatureRule(1536, 886, '#F7EFA5'))
        return rules