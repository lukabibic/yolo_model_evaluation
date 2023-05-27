import json
import os

from shapely.geometry import box

from unquote import match_vott_to_yolo
from vott_reader import get_vott_info


# Function to calculate IoU (Intersection over Union)
def calculate_iou(boxA, boxB):
    # # Convert YOLOv5 normalized coordinates to pixel coordinates
    # # img_width, img_height = 1024, 1024  # Replace with the actual image dimensions
    # x1 = int(boxA['x'])
    # y1 = int(boxA['y'])
    # w1 = int(boxA['w'])
    # h1 = int(boxA['h'])
    #
    # # Calculate the coordinates of the VOTT tagged region
    # x2 = int(boxB['x'])
    # y2 = int(boxB['y'])
    # w2 = int(boxB['w'])
    # h2 = int(boxB['h'])
    #
    # # Calculate the intersection coordinates
    # x_intersection = max(x1, x2)
    # y_intersection = max(y1, y2)
    # w_intersection = min(x1 + w1, x2 + w2) - x_intersection
    # h_intersection = min(y1 + h1, y2 + h2) - y_intersection
    #
    # # Calculate the areas of intersection and union
    # intersection = w_intersection * h_intersection
    # area1 = w1 * h1
    # area2 = w2 * h2
    # union = area1 + area2 - intersection
    #
    # # Calculate the IoU value
    # iou = intersection / union
    #
    # return iou

    # Convert boxes to Shapely Polygon objects
    poly1 = box(boxA['x'], boxA['y'], boxA['x'] + boxA['w'], boxA['y'] + boxA['h'])
    poly2 = box(boxB['x'], boxB['y'], boxB['x'] + boxB['w'], boxB['y'] + boxB['h'])

    # Calculate intersection area
    intersection = poly1.intersection(poly2).area

    # Calculate union area
    union = poly1.union(poly2).area

    # Calculate IoU
    iou = intersection / union

    return iou


# Function to read YOLO detection text file
def read_yolo_detection(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    detections = []
    for line in lines:
        line = line.strip().split(' ')
        label = int(line[0])
        if label == 39:
            label = 'Bottle'
        elif label == 75:
            print('FOUND VASE, COULD CONSIDER AS BOTTLE')
            label = 'Bottle'
        x, y, w, h = map(float, line[1:5])
        confidence = float(line[5])

        x_center = x * 1024
        y_center = y * 1024
        width_original = w * 1024
        height_original = h * 1024

        x_top_left = (x_center - width_original / 2)
        y_top_left = (y_center - height_original / 2)


        # multiply normalized coordinates by image size
        # detections.append({
        #     'label': label,
        #     'x': x * 1024 / 32,
        #     'y': y * 1024 / 32,
        #     'w': w * 1024,
        #     'h': h * 1024,
        #     'confidence': confidence
        # })

        detections.append({
            'label': label,
            'x': x_top_left,
            'y': y_top_left,
            'w': w * 1024,
            'h': h * 1024,
            'confidence': confidence
        })

    return detections


# Function to read VOTT tagged JSON file
def read_vott_tagged(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # regions = data['assets'][data['asset']['id']]['regions']
    regions = data['regions']
    tagged_regions = []
    for region in regions:
        label = region['tags'][0]
        x = region['boundingBox']['left']
        y = region['boundingBox']['top']
        w = region['boundingBox']['width']
        h = region['boundingBox']['height']
        tagged_regions.append({
            'label': label,
            'x': x,
            'y': y,
            'w': w,
            'h': h
        })

    return tagged_regions

asset_txt_map = dict()

info_map = get_vott_info()
yolo_folder = 'yolo_detection_txt_files_2'
for asset_id in info_map:
    txt_file = match_vott_to_yolo(info_map[asset_id])
    yolo_path = os.path.join(yolo_folder, txt_file)

    if os.path.isfile(yolo_path):
        # print('file exists in folder')
        asset_txt_map[asset_id] = txt_file
    else:
        # print('file does not exist in folder!')
        pass

try:

    for asset_id in asset_txt_map:


        # yolo_file_path = 'yolo_detection_txt_files/DALL_C2_B7E_202023-05-08_2015.19.47_20-_20Plastic_20bottle.txt'
        # vott_file_path = '220bcda86685baa05eae3d0d5eb5d608-asset.json'
        yolo_file_path = yolo_folder + '/' + asset_txt_map[asset_id]
        vott_file_path = 'vott_assets/' + asset_id + '-asset.json'

        if not os.path.exists(vott_file_path):
            # print('Asset file does not exist')
            pass

        else :
            # Read YOLO detections
            yolo_detections = read_yolo_detection(yolo_file_path)
            yolo_detections_size = len(yolo_detections)

            # Read VOTT tagged regions
            vott_tagged_regions = read_vott_tagged(vott_file_path)
            vott_tagged_regions_size = len(vott_tagged_regions)


            # print('Detection = ', yolo_detections)
            # print('Region = ', vott_tagged_regions)

            if yolo_detections_size == 1 and vott_tagged_regions_size == 1:

                # ADJUST Y TO BE THE SAME AS VOTT FOR TESTING PURPOSE
                # yolo_detections[0]['y'] = vott_tagged_regions[0]['y']
                # yolo_detections[0]['x'] = vott_tagged_regions[0]['x']

                # Compare detections and tagged regions
                for detection in yolo_detections:
                    for region in vott_tagged_regions:
                        # Compare detection and region based on label and bounding box
                        print('Detection = ', detection)
                        print('Region = ', region)

                        if str.lower(detection['label']) == str.lower(region['label']):
                            print('CORRECT DETECTION')
                            iou = calculate_iou(detection, region)

                            # Print IoU for demonstration
                            print(f"IoU: {iou}")
                        elif detection['label'] != region['label']:
                            print('INCORRECT DETECTION, detected object = ', detection['label'])

                            iou = calculate_iou(detection, region)
                            # Print IoU for demonstration
                            print(f"IoU: {iou}")

                    # Perform comparison and evaluation calculations here
                    # You can calculate metrics like IoU, precision, recall, etc.
            elif yolo_detections_size == vott_tagged_regions_size:
                yolo_bottles_count, vott_bottles_count = 0, 0
                print('SAME SIZE BUT COMPARISON LOGIC MISSING')
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                for detection in yolo_detections:
                    for region in vott_tagged_regions:

                        if str.lower(detection['label']) == 'bottle':
                            yolo_bottles_count += 1
                        vott_bottles_count += 1

                print('SAME SIZE FOUND THIS MANY BOTTLES:', yolo_bottles_count)

                print('Yolo found this many bottles : ', yolo_bottles_count)
                print('Actual bottle count from VoTT : ', vott_bottles_count)
            else:
                print('Yolo tagged this many objects in photos : ', yolo_detections_size)
                print('Actual count of tagged objects using VoTT : ', vott_tagged_regions_size)

                yolo_bottles_count = 0
                other_objects_count = 0
                for detection in yolo_detections:
                    if str.lower(detection['label']) == 'bottle':
                        print('Some bottle detected')
                        yolo_bottles_count += 1
                    else:
                        print('Wrong object detected = ', detection['label'])
                        other_objects_count += 1
        print()
        print()
        print()
except Exception as e:
    print(e)