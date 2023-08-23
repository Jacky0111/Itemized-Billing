from ultralytics import YOLO


if __name__ == '__main__':
    model = YOLO('yolov8s.yaml')  # build a new model from scratch

    results = model.train(data='config.yaml', epochs=50, workers=2)  # train the model

