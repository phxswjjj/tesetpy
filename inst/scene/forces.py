from . import SceneBase, FeatureRule


class ForcesWarQueue(SceneBase):
    """勢力戰爭-籌備/戰爭準備"""

    def feature_rules(self) -> [FeatureRule]:
        rules: [FeatureRule] = []
        # 中上標題
        rules.append(FeatureRule('forceswar_title.jpg'))

        return rules


class ForcesWarExec(SceneBase):
    """勢力戰爭-進行-籌備 or 戰爭"""

    def feature_rules(self) -> [FeatureRule]:
        rules: [FeatureRule] = []
        # 左上標題
        rules.append(FeatureRule('forceswar_exec_title.jpg'))

        return rules


class ForcesWarExecStep1(ForcesWarExec):
    """勢力戰爭-進行-籌備"""

    def feature_rules(self) -> [FeatureRule]:
        rules: [FeatureRule] = super().feature_rules()
        # 左側頁籤
        rules.append(FeatureRule('forceswar_exec_step1.jpg'))

        return rules


class ForcesWarExecStep2(ForcesWarExec):
    """勢力戰爭-進行-戰爭"""

    def feature_rules(self) -> [FeatureRule]:
        rules: [FeatureRule] = super().feature_rules()
        # 左側頁籤
        rules.append(FeatureRule('forceswar_exec_step2.jpg'))

        return rules
