# Itemized Billing

This repository contains the codebase for a hospital bill detection project. The primary objective of this project is to develop a system that can automatically extract and process itemized billing information from hospital bills. This can be immensely useful in healthcare administration and cost analysis, making the billing process more efficient and transparent. The project is mainly developed using Python, with a focus on incorporating the PyTorch library for machine learning and computer vision tasks. Python 3.10 is the minimum required version for running this codebase.


[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/mit/)
[![Python Version](https://img.shields.io/badge/python-3.10-green)](https://www.python.org/downloads/)

## Table of Contents

1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
3. [Project Structure](#3-project-structure)
4. [Usage](#4-usage)
5. [Testing](#5-testing)
6. [CI](#6-ci)
7. [Contributing](#7-contribution)
8. [License](#8-license)
9. [Acknowledgments](#9-acknowledgments)


## 1 Introduction

This project extracts itemized billing data from hospital bills using a two-stage detection pipeline (table then rows) plus OCR and heuristic tabular reconstruction. It supports dataset creation from PDFs and produces Excel outputs for downstream analysis.


## 2 Installation

Prerequisites
- Python 3.10
- Poppler for PDF conversion (used by `pdf2image`)

Setup
1. Create and activate a Python 3.10 environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Ensure Poppler is installed and on your PATH. If not, set:
   - `POPPLER_PATH` to the Poppler `bin` directory (example Windows default is `C:\poppler-23.01.0\Library\bin`).


## 3 Project Structure

- `ItemizedBillingApp.py`: Main entry point for dataset creation and OCR workflow.
- `Conversion/Conversion.py`: PDF to image conversion.
- `Detect.py`: YOLOv8 inference for table and row detection.
- `OpticalCharacterRecognition.py`: PaddleOCR + tabular reconstruction.
- `TabularRule.py`: Heuristic rules to assemble rows/columns.
- `CVAT/`: Training and testing images.
- `table.pt`, `row.pt`: Trained YOLO weights for table and row detection.


## 4 Usage

Run the interactive app:

```bash
python ItemizedBillingApp.py
```

Option A: Create Dataset
- Choose `1. Create Dataset` and select PDF files.
- Output images are saved under `Conversion/images/<pdf_name>/`.

Option B: Run OCR
- Choose `2. Run OCR` and select input images.
- Outputs are saved under `OCR_Output/<image_name>_<timestamp>/` and include:
  - `image_to_data.xlsx` (raw OCR tokens)
  - `itemized_data.xlsx` (reconstructed table)

Example input/output
- Input: PDF hospital bills (for dataset creation) or table images (for OCR).
- Output: Annotated images plus Excel files in the OCR output folder.

Optional environment variables
- `POPPLER_PATH`: Path to Poppler `bin` directory for PDF conversion.
- `BILL_DIR`: Example directory for `name.py` batch renaming.
- `CLAIM_XLSX`: Example Excel file path for `name.py` batch renaming.
- `RENAME_DIR`: Example directory for `test.py` batch renaming.

Notes on portability
- The app uses `wxPython` for file dialogs, so it runs best in a desktop environment.
- Default paths in scripts are Windows flavored, but all can be overridden with environment variables listed above.


## 5 Testing

Run tests locally:

```bash
pytest
```

Test notes
- OCR unit tests skip if `paddleocr` is not installed.
- Core grouping logic is exercised via unit tests in `tests/`.


## 6 CI

GitHub Actions runs `pytest` with a minimal dependency set to keep the workflow fast.


## 7 Contribution

Contributions are welcome. Please open an issue or pull request describing the change and the expected impact.


## 8 License

This project is licensed under the [MIT License](LICENSE). 


## 9 Acknowledgments
