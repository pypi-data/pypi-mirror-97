from json import JSONEncoder

import cv2
import numpy as np
import urllib.request
from decimal import *


class Convertor:

    @staticmethod
    def url_to_image(url: str) -> np.ndarray:
        """
        # download the image, convert it to a NumPy array, and then read
        # it into OpenCV format
        :param url:
        :return:
        """

        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return image

    @staticmethod
    def tensorFaster_to_np(tensor):
        return tensor[0]["boxes"].cpu().numpy(), \
               tensor[0]["scores"].cpu().numpy(), \
               tensor[0]["labels"].cpu().numpy()

    @staticmethod
    def tensorMask_to_np(tensor):
        return tensor[0]["boxes"].detach().cpu().numpy(), \
               tensor[0]["scores"].detach().cpu().numpy(), \
               tensor[0]["labels"].detach().cpu().numpy(), \
               tensor[0]["masks"].squeeze().detach().cpu().numpy()

    @staticmethod
    def list_to_dict(data: list, config: dict) -> dict:
        """

        :param data:
        :param config:
        :return:
        """
        keys = config.columnKeys

        return dict(zip(keys, data))

    @staticmethod
    class Bunch(object):
        def __init__(self, adict):
            self.__dict__.update(adict)

    @staticmethod
    class numpy_array_encoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return JSONEncoder.default(self, obj)

    @staticmethod
    def decimal_fix(number):
        getcontext().rounding = ROUND_DOWN
        return Decimal(number).quantize(Decimal(10) ** -9)

    def intersection_float_to_decimal(self, lat1, lon1, lat2, lon2):
        """

        Parameters
        ----------
        lat1
        lon1
        lat2
        lon2

        Returns points convert decimal format
        -------

        """
        lat1 = self.decimal_fix(lat1)
        lon1 = self.decimal_fix(lon1)
        lat2 = self.decimal_fix(lat2)
        lon2 = self.decimal_fix(lon2)

        return lat1, lon1, lat2, lon2