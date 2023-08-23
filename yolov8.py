from ultralytics import YOLO


if __name__ == '__main__':
    model = YOLO('yolov8n.yaml')  # build a new model from scratch

    results = model.train(data='config.yaml', epochs=10)  # train the model

