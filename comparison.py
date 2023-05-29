import json
import os

from shapely.geometry import box

from unquote import match_vott_to_yolo
from vott_reader import get_vott_info

LABEL_FILE = open("class_labels.json")
CLASS_LABELS = json.load(LABEL_FILE)

YOLO_FOLDER = 'yolo_detection_txt_files_2'
VOTT_ASSETS_FOLDER = 'vott_assets/'

# Decide if you want to change vase label to bottle label
# Reason why: When the YOLO model doesn't detect a bottle, it most often detects a vase
# This could be solved by curated training
CHANGE_VASE_LABEL_To_BOTTLE_LABEL = False


# Function to calculate IoU (Intersection over Union)
def calculate_iou(boxA, boxB):

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

    if CHANGE_VASE_LABEL_To_BOTTLE_LABEL:
        CLASS_LABELS["75"] = 'bottle'

    for line in lines:
        line = line.strip().split(' ')
        label_num = line[0]
        # if label == 39:
        #     label = 'bottle'
        # elif label == 75:
        #     print('FOUND VASE, COULD CONSIDER AS BOTTLE')
        #     label = 'Bottle'
        # else:
        #     label = CLASS_LABELS[label]
        label = CLASS_LABELS[label_num]

        x, y, w, h = map(float, line[1:5])
        confidence = float(line[5])

        # x_center = x * 1024
        # y_center = y * 1024
        # width_original = w * 1024
        # height_original = h * 1024

        # x_top_left = (x_center - width_original / 2)
        # y_top_left = (y_center - height_original / 2)

        # detections.append({
        #     'label': label,
        #     'x': x_top_left,
        #     'y': y_top_left,
        #     'w': w * 1024,
        #     'h': h * 1024,
        #     'confidence': confidence
        # })

        detections.append({
            'label': label,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
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

    width = data['asset']['size']['width']
    height = data['asset']['size']['height']

    for region in regions:
        label = region['tags'][0]
        x = region['boundingBox']['left']
        y = region['boundingBox']['top']
        w = region['boundingBox']['width']
        h = region['boundingBox']['height']

        x_center = x + w / 2
        y_center = y + h / 2

        x = x_center/width
        y = y_center/height

        w = w / width
        h = h / width

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

iou_list = []

yolo_detected_object_per_image_list = []
vott_objects_per_image_list = []

correct_count = 0
incorrect_count = 0

for asset_id in info_map:
    txt_file = match_vott_to_yolo(info_map[asset_id])
    yolo_path = os.path.join(YOLO_FOLDER, txt_file)

    if os.path.isfile(yolo_path):
        # print('file exists in folder')
        asset_txt_map[asset_id] = txt_file
    else:
        # print('file does not exist in folder!')
        vott_file_path = VOTT_ASSETS_FOLDER + asset_id + '-asset.json'

        # Read VOTT tagged regions
        vott_tagged_regions = read_vott_tagged(vott_file_path)
        vott_tagged_regions_size = len(vott_tagged_regions)

        vott_objects_per_image_list.append(vott_tagged_regions_size)

        pass

try:

    for asset_id in asset_txt_map:

        yolo_file_path = YOLO_FOLDER + '/' + asset_txt_map[asset_id]
        vott_file_path = 'vott_assets/' + asset_id + '-asset.json'

        if not os.path.exists(vott_file_path):
            # print('Asset file does not exist')
            pass

        else :
            # Read YOLO detections
            yolo_detections = read_yolo_detection(yolo_file_path)
            yolo_detections_size = len(yolo_detections)

            yolo_detected_object_per_image_list.append(yolo_detections_size)

            # Read VOTT tagged regions
            vott_tagged_regions = read_vott_tagged(vott_file_path)
            vott_tagged_regions_size = len(vott_tagged_regions)

            vott_objects_per_image_list.append(vott_tagged_regions_size)

            print('Detection = ', yolo_detections)
            print('Region = ', vott_tagged_regions)

            if yolo_detections_size == 1 and vott_tagged_regions_size == 1:

                # Compare detections and tagged regions
                for detection in yolo_detections:
                    for region in vott_tagged_regions:
                        # Compare detection and region based on label and bounding box
                        # print('Detection = ', detection)
                        # print('Region = ', region)

                        if str.lower(detection['label']) == str.lower(region['label']):
                            print('CORRECT DETECTION')
                            correct_count += 1
                            iou = calculate_iou(detection, region)

                            # Print IoU for demonstration
                            print(f"IoU: {iou}")
                        elif detection['label'] != region['label']:
                            print('INCORRECT DETECTION, detected object = ', detection['label'])
                            incorrect_count += 1

                            iou = calculate_iou(detection, region)
                            # Print IoU for demonstration
                            print(f"IoU: {iou}")

                        iou_list.append(iou)

                    # Perform comparison and evaluation calculations here
                    # You can calculate metrics like IoU, precision, recall, etc.
            elif yolo_detections_size == vott_tagged_regions_size:

                # Sort detections and regions based on the combined ('x', 'y') value
                sorted_detections = sorted(yolo_detections, key=lambda d: (d['x'], d['y']))
                sorted_regions = sorted(vott_tagged_regions, key=lambda r: (r['x'], r['y']))

                # Now you can iterate over the sorted lists and compare the corresponding detections and regions
                for detection, region in zip(sorted_detections, sorted_regions):
                    if str.lower(detection['label']) == str.lower(region['label']):
                        print('CORRECT DETECTION')
                        correct_count += 1

                        iou = calculate_iou(detection, region)

                        # Print IoU for demonstration
                        print(f"IoU: {iou}")
                    elif detection['label'] != region['label']:
                        print('INCORRECT DETECTION, detected object = ', detection['label'])
                        incorrect_count += 1

                        iou = calculate_iou(detection, region)
                        # Print IoU for demonstration
                        print(f"IoU: {iou}")

                    iou_list.append(iou)

            else:

                # Initialize a list to store the closest matching region for each detection
                matching_regions = []

                # Iterate over each detection
                for detection in yolo_detections:
                    best_iou = 0  # Initialize the best IoU to 0
                    best_region = None  # Initialize the best matching region as None

                    # Calculate IoU between the detection and each region
                    for region in vott_tagged_regions:
                        iou = calculate_iou(detection, region)  # Replace with your IoU calculation function

                        # Update the best IoU and best matching region if the current IoU is higher
                        if iou > best_iou:
                            best_iou = iou
                            best_region = region

                    # Add the best matching region to the list
                    matching_regions.append(best_region)

                # Now you can iterate over the detections and matching_regions lists and compare the corresponding objects
                for i, detection in enumerate(yolo_detections):
                    print('DETECTION = ', detection)
                    print('MATCHING REGION = ', matching_regions[i])

                    if str.lower(detection['label']) == str.lower(matching_regions[i]['label']):
                        print('CORRECT DETECTION')
                        correct_count += 1

                        iou = calculate_iou(detection, matching_regions[i])

                        # Print IoU for demonstration
                        print(f"IoU: {iou}")
                    elif str.lower(detection['label']) == str.lower(matching_regions[i]['label']):
                        print('INCORRECT DETECTION, detected object = ', detection['label'])
                        incorrect_count += 1

                        iou = calculate_iou(detection, matching_regions[i])
                        # Print IoU for demonstration
                        print(f"IoU: {iou}")

                    iou_list.append(iou)

        print()
        print()
        print()
except Exception as e:
    print(e)

if len(iou_list) > 0:
    print('AVERAGE IOU IN MODEL = ', sum(iou_list)/len(iou_list))

print('YOLO objects count for all images = ', sum(yolo_detected_object_per_image_list))
print('ACTUAL objects count for all images = ', sum(vott_objects_per_image_list))

print('VOTT FILES COUNT = ', len(vott_objects_per_image_list))
print('YOLO DIDNT DETECT ANY OBJECTS ON THIS AMOUNT OF IMAGE FILES = ', len(vott_objects_per_image_list) - len(yolo_detected_object_per_image_list))

print('CORRECT DETECTIONS COUNT = ', correct_count)
print('INCORRECT DETECTIONS COUNT = ', incorrect_count)

if correct_count + incorrect_count > 0:
    print(f'PERCENTAGE OF YOLO TAGGED OBJECTS CORRECTLY DETECTED = {correct_count/(correct_count + incorrect_count) * 100}%')
    print(f'PERCENTAGE OF ALL OBJECTS CORRECTLY DETECTED = {correct_count / sum(vott_objects_per_image_list) * 100}%')
