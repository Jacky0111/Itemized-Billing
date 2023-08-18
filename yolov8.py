from ultralytics import YOLO

# ROOT_DIR =

# Load a model
model = YOLO('yolov8n.yaml')  # build a new model from scratch

# Use the model
results = model.train(data='config.yaml', epochs=10)  # train the model
