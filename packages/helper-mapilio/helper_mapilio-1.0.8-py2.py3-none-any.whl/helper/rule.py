import json

import numpy as np
from trianglesolver import solve, degree


class Utilities:

    @staticmethod
    def is_match(matched_objects: list) -> bool:
        """
        matched_objects matched objects twice
        :param matched_objects:
        :return: check out length bool type
        """
        if len(matched_objects) > 0:
            return True
        else:
            return False

    @staticmethod
    def is_between(t1max: bool, t2max: bool) -> bool:
        """
        the aim check between each detected thetas

        :param t1max: t1max is thetas max 1  between defined angle wide in config
        :param t2max: t2max is thetas max 1  between defined angle wide in config
        :return: check cross match as bool type
        """
        return True if (t1max and t2max) else False

    @staticmethod
    def is_right_or_left(theta1: float, heading1: float, theta2: float, heading2: float) -> bool:
        """
        Goal : detected objects must be same region each right or left.

        :param theta1: first object which seen by car angle
        :param heading1: moment car location angle according to north
        :param theta2: second object which seen by car angle
        :param heading2: moment car location angle according to north
        :return: gives answer as bool type objects left or right check
        """
        if theta1 <= heading1 and theta2 <= heading2:
            return True
        elif theta1 >= heading1 and theta2 >= heading2:
            return True
        else:
            return False

    @staticmethod
    def check_validity(a, b, c):
        """
         Triangle rule checks
        it's triangle edged as a, b, c
         5 < C / degree < 20 must be otherwise return false

        :param a: detected point and **first** car position edge
        :param b: detected point and **second** car position edge
        :param c: first and second car edge
        :return: if is not triangle and C degree over the defined variable return False.
        """

        a, b, c, A, B, C = solve(a, b, c)
        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            if not 5 < (C / degree) < 20:
                return False
        return True

    @staticmethod
    def get_label_name_or_id(labelid: int, config: dict):
        """
         this function has two assignment
            if labelid is **array** return classname
            if labelid is **string** return classname id

        :param labelid:
        :param config:
        :return: object's name or id
        """

        with open(config.labeljson, 'r') as f:
            labelsDict = json.load(f)
            if isinstance(labelid, np.ndarray):
                return labelsDict.get(str(labelid))
            elif isinstance(labelid, str):
                for id, name in labelsDict.items():
                    if name == labelid:
                        return id

    @staticmethod
    def rule_apply(c: int) -> float:
        """

        :param c: how many car detected object for example;
         DUR traffic sign 3 panorama has detected c is 3
        :return: confidence ratio between 1 and 100
        """
        confidence_rate = (1 - 1 / c) if c else "{} can't null".format({c})

        return confidence_rate