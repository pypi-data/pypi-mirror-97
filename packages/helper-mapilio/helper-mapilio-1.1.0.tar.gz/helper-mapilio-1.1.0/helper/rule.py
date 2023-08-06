import json

import numpy as np
from trianglesolver import solve, degree
from addict import Dict


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
    def is_right_or_left(**kwargs) -> bool:
        """
        Goal : detected objects must be same region each right or left.
        # theta1: float, heading1: float, theta2: float, heading2: float
        :param theta1: first object which seen by car angle
        :param heading1: moment car location angle according to north
        :param theta2: second object which seen by car angle
        :param heading2: moment car location angle according to north
        :return: gives answer as bool type objects left or right check
        """
        params = Dict(**kwargs)
        theta1 = params.theta1
        theta2 = params.theta2
        heading1 = params.heading1
        heading2 = params.heading2

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
    def get_label_name_or_id(labelId: int, config: dict):
        """
         this function has two assignment

        :param labelId: if labelId is **array** return classname else
                        labelId is **string** return classname id
        :param config:
        :return: object's name or id
        """

        with open(config.labeljson, 'r') as f:
            labelsDict = json.load(f)
            if isinstance(labelId, np.ndarray):
                return labelsDict.get(str(labelId))
            elif isinstance(labelId, str):
                for id, name in labelsDict.items():
                    if name == labelId:
                        return id
