# yolo_model_evaluation
 Python script which compares users' VoTT tagged images with the Detections using YoloV5 model

# Workflow
- Model takes the project VoTT json file to get all the Assets for each image in project
- Runs a method which matches all the Assets with the Image name and gets the label (.txt) file that matches that Image name
-  Loops over detection (yolo) and regions (VoTT) and calculates IoU values (the percentage match of the bounding box coordinates)
