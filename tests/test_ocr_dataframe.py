import numpy as np
import pytest

pytest.importorskip("paddleocr")

import OpticalCharacterRecognition as ocr_module


def test_image_to_data_dataframe_structure(monkeypatch):
    class DummyOCR:
        def __init__(self, *args, **kwargs):
            pass

        def ocr(self, img, cls=True):
            return [
                [
                    ([(0, 0), (10, 0), (10, 5), (0, 5)], ("ABC", 0.95)),
                    ([(20, 0), (30, 0), (30, 5), (20, 5)], ("123", 0.9)),
                ]
            ]

    monkeypatch.setattr(ocr_module, "PaddleOCR", DummyOCR)

    img = np.zeros((10, 10, 3), dtype=np.uint8)
    df = ocr_module.OCR.imageToData(img, DummyOCR())

    assert list(df.columns) == ["left", "top", "width", "height", "conf", "text"]
    assert df.shape[0] == 2
    assert df.loc[0, "text"] == "ABC"
    assert df.loc[1, "text"] == "123"


def test_image_to_data_empty_result(monkeypatch):
    class DummyOCR:
        def __init__(self, *args, **kwargs):
            pass

        def ocr(self, img, cls=True):
            return []

    monkeypatch.setattr(ocr_module, "PaddleOCR", DummyOCR)

    img = np.zeros((10, 10, 3), dtype=np.uint8)
    df = ocr_module.OCR.imageToData(img, DummyOCR())

    assert list(df.columns) == ["left", "top", "width", "height", "conf", "text"]
    assert df.shape[0] == 0
