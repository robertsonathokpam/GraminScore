import os
import cv2
import tensorflow as tf
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from datetime import datetime

app = Flask(__name__)

# ------------------ FOLDERS ------------------
UPLOAD_FOLDER = "temp_images"
# Ensure we clean up old PDFs/images or just overwrite
REPORT_PATH = "report.pdf" 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------ LOAD MODELS ------------------
# 1. Generic Model (MobileNetV2) for Object Detection
try:
    classifier_model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=True)
    decode_predictions = tf.keras.applications.mobilenet_v2.decode_predictions
    preprocess_input_mobilenet = tf.keras.applications.mobilenet_v2.preprocess_input
    print("✅ Generic Model Loaded")
except Exception as e:
    print(f"❌ Error loading Generic Model: {e}")

# 2. Custom Damage Model (Your trained .h5 file)
try:
    damage_model = tf.keras.models.load_model("my_house_model.h5")
    print("✅ Custom Damage Model Loaded")
except Exception as e:
    print(f"❌ Error loading Custom Model: {e}")
    damage_model = None

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------ VALIDATION LOGIC ------------------
def is_valid_house_image(img_pil):
    # Resize for MobileNet
    img_resized = img_pil.resize((224, 224))
    x = np.array(img_resized)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input_mobilenet(x)

    preds = classifier_model.predict(x)
    decoded = decode_predictions(preds, top=5)[0]

    # Enhanced Keyword Lists
    house_keywords = ["house", "home", "building", "hut", "bungalow", "cottage", "barn", "thatch", "ruins", "monastery", "castle"]
    component_keywords = ["roof", "door", "window", "wall", "patio", "lumber"]
    non_house_keywords = ["person", "man", "woman", "face", "dog", "cat", "car", "truck", "food", "text", "pattern"]

    is_house = False
    explicit_non_house = False
    detected_labels = []

    for _, label, _ in decoded:
        label = label.lower()
        detected_labels.append(label)
        
        if any(bad in label for bad in non_house_keywords):
            explicit_non_house = True
        if any(good in label for good in house_keywords + component_keywords):
            is_house = True

    # Final Decision
    if explicit_non_house:
        return False, detected_labels # It's a cat/car
    if is_house:
        return True, detected_labels
    
    return False, detected_labels # Unknown object

# ------------------ COMPONENT DETECTION ------------------
def detect_component(labels):
    # Decide which part of the house this image focuses on
    labels_str = " ".join(labels).lower()
    if "roof" in labels_str or "thatch" in labels_str or "tile" in labels_str:
        return "roof"
    if "door" in labels_str:
        return "door"
    if "window" in labels_str:
        return "window" # We'll group window with wall usually, or keep separate
    return "wall" # Default fallback

# ------------------ SCORING LOGIC ------------------
def get_ai_score(img_pil):
    if damage_model is None: return 0
    
    # Resize for Custom Model (MobileNetV2 expects 0-1 float inputs if trained with 1./255)
    img = img_pil.resize((224, 224))
    img_array = np.array(img)
    img_array = img_array / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)

    prediction = damage_model.predict(img_array)
    # Assuming Class 1 = Good, Class 0 = Bad
    score = int(prediction[0][0] * 100)
    return score

def get_detailed_description(score):
    if score >= 80:
        return "The structure appears to be in Excellent condition. No significant structural defects, cracks, or weathering were detected. The walls and roof appear intact and stable."
    elif score >= 60:
        return "The structure is in Good condition. Minor signs of wear or weathering may be present, but the structural integrity appears sound. Routine maintenance is recommended."
    elif score >= 40:
        return "The structure is in Average/Fair condition. There are visible signs of degradation, potential surface cracks, or material fatigue. Immediate inspection is advised to prevent further damage."
    else:
        return "The structure appears to be in Poor/Damaged condition. Significant defects, cracks, or collapse risks were detected. Urgent structural intervention or reconstruction may be required."

# ------------------ ROUTES ------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    images = request.files.getlist("images")
    if not images or images[0].filename == "":
        return render_template("index.html", error="Please upload an image.")

    # Data Containers
    roof_scores, wall_scores, door_scores = [], [], []
    valid_images_paths = []
    skipped_files = [] # To tell user about rejected files
    
    for file in images:
        if not allowed_file(file.filename):
            continue

        # Load Image
        try:
            img_pil = Image.open(file).convert("RGB")
        except:
            skipped_files.append(f"{file.filename} (Corrupt file)")
            continue

        # 1. Validate (Is it a house?)
        is_valid, labels = is_valid_house_image(img_pil)
        
        if not is_valid:
            # Add to skipped list with reason
            reason = labels[0] if labels else "Unknown"
            skipped_files.append(f"{file.filename} (Detected: {reason})")
            continue

        # Save valid image for PDF
        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        img_pil.save(save_path)
        valid_images_paths.append(save_path)

        # 2. Score
        score = get_ai_score(img_pil)

        # 3. Categorize
        comp = detect_component(labels)
        if comp == "roof": roof_scores.append(score)
        elif comp == "door": door_scores.append(score)
        else: wall_scores.append(score) # Walls and generic views

    # --- CALCULATE RESULTS ---
    if not valid_images_paths:
        return render_template("index.html", error="No valid house images found.", skipped=skipped_files)

    # Helper to average list or return None
    def avg(lst): return int(sum(lst)/len(lst)) if lst else None

    final_roof = avg(roof_scores)
    final_wall = avg(wall_scores)
    final_door = avg(door_scores)

    # Overall Score (Average of whatever components we found)
    components_found = [s for s in [final_roof, final_wall, final_door] if s is not None]
    overall_score = int(sum(components_found) / len(components_found)) if components_found else 0
    
    # Description
    description = get_detailed_description(overall_score)

    # --- GENERATE PDF ---
    generate_pdf(REPORT_PATH, valid_images_paths[0], overall_score, final_roof, final_wall, final_door, description)

    return render_template("index.html", 
                           score=overall_score,
                           roof=final_roof if final_roof is not None else "Data Not Available",
                           walls=final_wall if final_wall is not None else "Data Not Available",
                           door=final_door if final_door is not None else "Data Not Available",
                           desc=description,
                           skipped=skipped_files)

def generate_pdf(path, image_path, score, roof, wall, door, desc):
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "GraminScore Analysis Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 75, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Draw Image (The first valid house image)
    try:
        # Aspect ratio math to fit image nicely
        img = ImageReader(image_path)
        img_w, img_h = img.getSize()
        aspect = img_h / float(img_w)
        display_width = 400
        display_height = display_width * aspect
        
        # Don't let it get too tall
        if display_height > 300:
            display_height = 300
            display_width = display_height / aspect
            
        c.drawImage(image_path, 100, height - 400, width=display_width, height=display_height)
    except Exception as e:
        c.drawString(100, height - 200, "[Error displaying image]")

    # Scores Section
    y_pos = height - 450
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y_pos, f"Overall GraminScore: {score}/100")
    
    y_pos -= 30
    c.setFont("Helvetica", 14)
    
    # Helper to print score or N/A
    def fmt(val): return f"{val}/100" if val is not None else "Data Not Available (Not Visible)"
    
    c.drawString(70, y_pos, f"• Wall Condition: {fmt(wall)}"); y_pos -= 20
    c.drawString(70, y_pos, f"• Roof Condition: {fmt(roof)}"); y_pos -= 20
    c.drawString(70, y_pos, f"• Door Condition: {fmt(door)}"); y_pos -= 40

    # Description Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos, "Assessment Description:")
    y_pos -= 20
    c.setFont("Helvetica", 12)
    
    # Text wrapping for long description
    text_object = c.beginText(50, y_pos)
    text_object.setFont("Helvetica", 12)
    # Split text into chunks for simple wrapping (approx 80 chars)
    words = desc.split()
    line = []
    for word in words:
        if len(" ".join(line + [word])) < 80:
            line.append(word)
        else:
            text_object.textLine(" ".join(line))
            line = [word]
    text_object.textLine(" ".join(line))
    c.drawText(text_object)

    c.save()

@app.route("/download")
def download():
    return send_file(REPORT_PATH, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
