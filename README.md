
# AI-Based Grading System using Python & OpenCV (OCR) 🎓📝

An automated paper checker and AI-driven grading system built with Python, OpenCV, and Optical Character Recognition (OCR) to evaluate and grade student answer scripts efficiently and accurately.

---

## 📌 Project Overview

Manual grading of physical answer sheets is time-consuming and prone to human error or inconsistency. This Final Year Project (FYP) introduces an automated paper-checking system that digitizes answer script evaluation using computer vision and OCR. By leveraging image processing algorithms, the system extracts handwritten or printed text, compares it against benchmark answer keys, and calculates grades automatically—achieving **90% accuracy** while reducing manual evaluation time by **35%**.

---

## 🛠️ Key Features

* **Automated Document Processing:** Preprocesses scanned answer scripts using OpenCV (noise reduction, thresholding, and perspective transformation).
* **OCR Text Extraction:** Accurately extracts handwritten and printed responses from evaluated answer sheets.
* **Intelligent Scoring & Feedback:** Evaluates extracted text against preset master keys to compute scores instantly.
* **User-Friendly Interface:** Integrated UI (`ocr_ui.py`) and API backend (`ocr_api.py`) for seamless interaction and batch processing.

---

## 📁 Repository Structure

```text
├── checker.py            # Core paper grading and evaluation logic
├── ocr_api.py            # API endpoint for OCR processing and scoring integration
├── ocr_ui.py             # User Interface for uploading and reviewing answer scripts
├── requirements.txt      # Python dependencies
├── .env                  # Environment configuration
├── LICENSE               # MIT License
└── README.md             # Project Documentation

```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed on your system along with Tesseract OCR (if required by your OCR setup).

### Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/mussabafridi/AI-based-grading-system-using-Python-OpenCV-OCR-FYP-.git](https://github.com/mussabafridi/AI-based-grading-system-using-Python-OpenCV-OCR-FYP-.git)

```


2. **Navigate to the project directory:**
```bash
cd AI-based-grading-system-using-Python-OpenCV-OCR-FYP-

```


3. **Install required dependencies:**
```bash
pip install -r requirements.txt

```



---

## 💻 Usage

1. **Run the UI Application:**
```bash
python ocr_ui.py

```


2. **Run the API Backend:**
```bash
python ocr_api.py

```


3. **Execute Core Evaluation Script:**
```bash
python checker.py

```



---

## 📊 Results & Impact

* **Accuracy:** Achieved a **90% evaluation accuracy** against manual grading standards.
* **Efficiency:** Reduced processing time by **35%**, enabling rapid assessment of large script batches.

---

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE).



```
