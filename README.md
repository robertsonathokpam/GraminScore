# GraminScore AI

GraminScore AI is a web-based application designed to automate the inspection of rural houses. Using Deep Learning, it analyzes user-uploaded images of homes (mud, concrete, thatch) and assigns a structural condition score. It also generates an official PDF report for government or personal records.

## Key Features

- **Smart Validation** — Automatically detects invalid images (e.g., cats, cars, selfies) and rejects them before analysis.
- **Component Scoring** — Analyzes specific parts of the house (Roof, Walls, Door) using feature extraction.
- **AI Condition Score** — Generates a 0–100 score indicating the structural health of the building.
- **PDF Report Generation** — Creates a downloadable, professional audit report with the house image and detailed metrics.
- **Responsive UI** — A modern, glassmorphism-based interface that works seamlessly on mobile devices.

## How the Model Works

The core of GraminScore is built on **Transfer Learning** using MobileNetV2.

1. **Base Model**: MobileNetV2 (pre-trained on ImageNet) is used as the feature extractor. Optimized for speed and efficiency, making it ideal for web deployment.
2. **Preprocessing**: Incoming images are resized to 224×224 pixels and normalized.
3. **Two-Stage Pipeline**:
   - **Stage 1 (Object Detection)**: The generic MobileNetV2 checks if the image contains a house, building, or architecture. Non-house images (cats, cars, etc.) are rejected.
   - **Stage 2 (Damage Assessment)**: Valid images are passed to custom-trained top layers (`my_house_model.h5`), which classify the structural integrity (Good vs. Damaged).
4. **Scoring**: The probability output is converted into a percentage score (0–100).

## Problem Statement

Manual house condition assessment is:
- Time-consuming
- Subjective
- Difficult to scale in rural and remote areas

There is a need for a simple, image-based system that can assist officials and organizations in evaluating housing conditions more efficiently.

## Solution

GraminScore AI provides:
- Image-based house validation using AI
- Component-wise analysis (roof, walls, doors)
- Automated condition scoring
- Downloadable PDF assessment report
- Soft warnings for non-rural or urban structures

The system works with ordinary images captured using basic cameras or mobile phones.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core language |
| Flask | Web framework |
| TensorFlow / Keras | Image classification (MobileNetV2) |
| Pillow (PIL) | Image handling |
| NumPy | Numerical processing |
| ReportLab | PDF report generation |
| HTML / CSS / JS | Frontend UI |

## Project Structure

```
GraminScore/
├── app.py                      # Flask application
├── templates/
│   └── index.html              # Frontend UI
├── static/
│   ├── style.css               # Styles
│   └── main.js                 # Client-side logic
├── model_training/
│   ├── training_model.py       # Model training script
│   └── dataset/                # Training data
├── generated_reports/          # PDF reports (auto-created)
├── temp_images/                # Uploaded images (auto-created)
├── my_house_model.h5           # Trained model (see setup)
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.11 (64-bit) — TensorFlow does **not** support Python 3.14

Verify:
```bash
py -3.11 --version
```

### 1. Clone the Repository
```bash
git clone https://github.com/robertsonathokpam/GraminScore.git
cd GraminScore
```

### 2. Create Virtual Environment
```bash
py -3.11 -m venv venv
```

Activate:
- **Windows**: `venv\Scripts\activate`
- **macOS / Linux**: `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the Model (Required on first setup)
```bash
cd model_training
python training_model.py
```
This will generate `my_house_model.h5`. Move it to the project root:
```bash
mv my_house_model.h5 ../
```

### 5. Run the Application
```bash
python app.py
```
Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Features

1. Validates image file formats (JPG, PNG, WEBP)
2. Rejects non-house images (people, animals, vehicles, objects)
3. Identifies house components (roof, wall, door)
4. Generates condition score (0–100)
5. Creates downloadable PDF report
6. Includes uploaded images in the report
7. Displays warnings for skipped/invalid files

## Challenges Faced

1. Lack of labeled datasets for rural house condition scoring
2. Time constraints during the hackathon
3. Initial false positives (non-house images classified as components)

## Future Improvements

1. Real-time mobile camera integration
2. GPS tagging and survey tracking
3. Multilingual support
4. Cloud deployment for large-scale use

## Disclaimer

This project is a prototype created for demonstration and research purposes.
Final decisions should always be verified by qualified professionals or authorities.

## Team

Built during the **DUHacks 5.0** hackathon by **Team The Alchemist**:

- **[Robertson Athokpam](https://github.com/robertsonathokpam)** — Co-Developer
- **[Rahkhuo Edward](https://github.com/RahkhuoEdward)** — Co-Developer
- **[Thiyam Chingu Robaartt](https://github.com/Thiy3640)** — Co-Developer

## License

This project is licensed under the [MIT License](LICENSE).
