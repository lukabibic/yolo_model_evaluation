import os
from vott_reader import get_vott_info
import urllib


def match_vott_to_yolo(vott_str):

    url = urllib.parse.unquote_plus(vott_str)
    url = url.replace(".png", ".txt")

    return url


if __name__ == '__main__':

    asset_txt_map = dict()

    info_map = get_vott_info()
    for asset_id in info_map:
        txt_file = match_vott_to_yolo(info_map[asset_id])
        yolo_path = os.path.join('yolo_detection_txt_files', txt_file)

        if os.path.isfile(yolo_path):
            print('file exists in folder')
            asset_txt_map[asset_id] = txt_file
        else:
            print('file does not exist in folder!')

    print(asset_txt_map)