


# GraminScore AI

GraminScore AI is a web-based application designed to automate the inspection of rural houses. Using Deep Learning, it analyzes user-uploaded images of homes (mud, concrete, thatch) and assigns a structural condition score. It also generates an official PDF report for government or personal records.

#  Key Features

Smart Validation: Automatically detects invalid images (e.g., cats, cars, selfies) and rejects them before analysis.

Component Scoring: Analyzes specific parts of the house (Roof, Walls, Door) using feature extraction.

AI Condition Score: Generates a 0-100 score indicating the structural health of the building.

PDF Report Generation: Creates a downloadable, professional audit report with the house image and detailed metrics.

Responsive UI: A modern, glassmorphism-based interface that works seamlessly on mobile devices.

# How the Model Works
The core of GraminScore is built on Transfer Learning using MobileNetV2.

Base Model: We use MobileNetV2 (pre-trained on ImageNet) as the feature extractor. This model is optimized for speed and efficiency, making it perfect for web deployment.

Preprocessing: Incoming images are resized to 224x224 pixels and normalized.

Two-Stage Pipeline:

Stage 1 (Object Detection): The generic MobileNetV2 checks if the image contains a "House," "Building," or "Architecture." If it detects a "Cat" or "Car," the image is rejected.

Stage 2 (Damage Assessment): If valid, the image is passed to our custom-trained top layers (stored in my_house_model.h5), which classify the texture and structural integrity (Good vs. Damaged).

Scoring: The probability output from the model is converted into a percentage score (0-100).



Manual house condition assessment is:
- Time-consuming  
- Subjective  
- Difficult to scale in rural and remote areas  

There is a need for a simple, image-based system that can assist officials and organizations in evaluating housing conditions more efficiently.


Solution:
GraminScore AI provides:
-  Image-based house validation using AI  
-  Component-wise analysis (roof, walls, doors)  
-  Automated condition scoring  
-  Downloadable PDF assessment report  
-  Soft warnings for non-rural or urban structures  

The system works with ordinary images captured using basic cameras or mobile phones.

Technologies Used:
- Python
- Flask - Web framework
- TensorFlow/Keras - Image classification (MobileNetV2)
- OpenCV (cv2) - Classical computer vision for condition scoring
- Pillow (PIL) - Image handling
- NumPy- Numerical processing
- ReportLab - PDF report generation
- HTML/CSS - Frontend UI


 Platform:
- Web Application
- Runs locally on a browser
- Can be deployed to cloud platforms (e.g., Render, Railway, Hugging Face Spaces)


Project Structure:

```text
GraminScore/
│
├─ app.py
├─ templates/
│   └─ index.html
├─ static/
│   └─ style.css
│   └─ main.js
├─ report.pdf
├─ requirements.txt
└─ README.md
```



Installation & Setup :

1. Install Python
 - Install Python 3.11 (64-bit)
 - TensorFlow does NOT support Python 3.14

   Verify:
    ```text
   py -3.11 --version
    ```

2. Create Virtual Environment
     ```text
   py -3.11 -m venv venv
     ```
   Activate:
   Windows
    ```text
   venv\Scripts\activate
     ```
   macOS / Linux
   ```text
   source venv/bin/activate
    ```

3. Install Dependencies
   ```text
   pip install flask tensorflow pillow numpy reportlab opencv-python
   ```

4. Run the Application
   ```text
   python app.py
    ```
   Open in browser:
   http://127.0.0.1:5000


Features:
1. Validates image file formats
2. Rejects non-house images (people, animals, plants, objects)
3. Identifies house components
4. Generates condition score (0–100)
5. Creates downloadable PDF report
6. Includes uploaded images in the report
7. Displays warnings for explicitly urban structures

Challenges Faced:
1. Lack of labeled datasets for rural house condition scoring
2. Time constraints during the hackathon
3. Initial false positives (non-house images classified as components)



Future Improvements:
1. Real-time mobile camera integration
2. GPS tagging and survey tracking
3. Multilingual support
4. Cloud deployment for large-scale use



Disclaimer:<br>
This project is a prototype created for demonstration and research purposes.<br>
Final decisions should always be verified by qualified professionals or authorities.

Team:<br>
Built with love during the  DUHacks 5.0 hackathon by<br> 
Team  - The Alchemist<br> 
Robertson Athokpam,
Thiyam Chingu Robaartt.
