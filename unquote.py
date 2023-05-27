import os
from vott_reader import get_vott_info


def match_vott_to_yolo(vott_str):

    url = vott_str.replace("%", '_')
    url = url.replace(".png", ".txt")
    # print('YOLO URL = ' , url)
    # print(url == url_i_want)
    return url


if __name__ == '__main__':

    # folder_path = 'vott-json-export'
    #
    # # Get all files in the folder
    # files = []
    # for file_name in os.listdir(folder_path):
    #     file_path = os.path.join(folder_path, file_name)
    #     if os.path.isfile(file_path):
    #         files.append(file_name)
    #
    # # Print the list of files
    # for file_path in files:
    #     print(file_path)
    #     yolo_file = match_vott_to_yolo(file_path)
    #     yolo_path = os.path.join('yolo_detection_txt_files', yolo_file)
    #     if os.path.isfile(yolo_path):
    #         print('file exists in folder')
    #     else:
    #         print('file does not exist in folder!')

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