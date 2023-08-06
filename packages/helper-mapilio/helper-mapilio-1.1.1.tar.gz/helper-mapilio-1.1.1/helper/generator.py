import random
import re
import os
import numpy as np

from typing import Tuple


class Generator:

    @staticmethod
    def do_uuid():
        """

        :return uuid.uuid1().int % (10**6) # example output = 694874
        -------

        """

        return random.randint(100000, 99999999)

    @staticmethod
    def path_url_creator(gui: bool, cfg: dict, split_data: list, i: int, directory=None) -> Tuple[str, str, str]:
        """

        :param gui:
        :param cfg:
        :param split_data:
        :param i:
        :param directory:
        :return:
        """
        host = cfg.image.ip_remote if cfg.image.Remote else cfg.image.ip_local
        if gui:
            ip_path = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
            ip_check = bool(ip_path.match(directory))
            print("ip mi", ip_check)
            if ip_check:
                path = os.path.join(
                    "http://" + host + ":" + cfg.image.port + "/" + cfg.image.directory + ":",
                    str(split_data[i]["dirname"]), split_data[i]["filename"], split_data[i]["imgname"])
            else:
                path = os.path.join(directory, str(split_data[i]["dirname"]),
                                    split_data[i]["filename"],
                                    split_data[i]["imgname"])
        else:
            path = os.path.join(
                "http://" + host + ":" + cfg.image.port + "/" + cfg.image.directory + ":",
                str(split_data[i]["dirname"]), split_data[i]["filename"], split_data[i]["imgname"])
            outPath = os.path.join("exports")

        print('Image Path :', path)
        return host, path, outPath

    @staticmethod
    def data_separation(data: list, dividing_percentage: int) -> list:
        """
         Segmenting incoming data

        :param data: data to be processed
        :param dividing_percentage: percentage of data fragmented
        :return: predicted masks
        """
        percentage = int(len(data) / 100 * dividing_percentage)

        for i in range(0, len(data), percentage):
            # Create an index range for l of n items:
            yield data[i:i + percentage]

    @staticmethod
    def get_exif_information(img_info):
        """

        :param img_info: exif object
        :return: (lat, lon), orientation, (Height, Width), FocalLength, Altitude,
        """
        information = {}
        data = img_info.extract_exif()
        try:
            information["model"] = data["model"]
            information["coordx"] = data["gps"]["latitude"]
            information["coordy"] = data["gps"]["longitude"]
            information["width"] = data["width"]
            information["height"] = data["height"]

            # Focal Length
            fLen_obj = data["gps"]["FocalLength"]
            fLen_str = f"{fLen_obj}"
            fLen_arr = fLen_str.split("/")
            fLen = float(int(fLen_arr[0]) / int(fLen_arr[1]))
            information["FocalLength"] = fLen

            hor_width = data["height"] if data["orientation"] == 1 else data["width"]
            information["orientation"] = hor_width
            # Angle of View
            aFov = np.arctan(hor_width / (2 * fLen)) * (180 / np.pi)
            information["FoV"] = aFov
        except:
            raise Exception(f"Check the image Exif Data some missing values")

        for k, v in information.items():
            if information[k] is None:
                raise Exception(f"{k} is None")
            else:
                pass

        return information