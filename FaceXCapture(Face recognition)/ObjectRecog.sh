echo
cd 
cd Desktop
cd object-detection-deep-learning
python3 -m venv venv && source venv/bin/activate
python deep_learning_object_detection.py --image images/example_01.jpg --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
kill
