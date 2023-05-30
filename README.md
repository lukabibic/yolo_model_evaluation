# yolo_model_evaluation
 Python script which compares users' VoTT tagged images with the 
 Detections using YoloV5 model and performs validation and prints the results

# Workflow
- Model takes the project VoTT json file to get all the Assets for each image in project
- Runs a method which matches all the Assets with the Image name and gets the label (.txt) file that matches that Image name
-  Loops over detection (yolo) and regions (VoTT) and calculates IoU values (the percentage match of the bounding box coordinates)

# How to run
- change YOLO_FOLDER variable to match the folder path to your yolo tag files (.txt)
- change VOTT_ASSETS_FOLDER to match the folder path for your VoTT assets
- change VOTT_PROJECT_EXPORT_JSON_PATH to match file path for the project export .json

- Run comparison.py after changing the Global variables