from flask import Flask, request, jsonify
import os
import cv2
import gemini
import tamper
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


# Set the folder where images will be uploaded
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configuring allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return "Image analysis and tamper detection API"

@app.route('/analyze', methods=['POST'])
def analyze_image():
    # Check if the request contains the file
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    # Check if the file is empty
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check for allowed extensions
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save the file
        file.save(filepath)
        
        # Analyze the image with Gemini
        try:
            analysis_result = gemini.analyze_image(filepath)
            analysis_data = {"analysis_result": analysis_result}
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 400

        # Detect tampering in the image
        is_tampered, mask = tamper.detect_tampering(filepath)
        tamper_data = {
            "is_tampered": is_tampered
        }

        # If tampered, save the mask for visualization
        if is_tampered:
            mask_path = os.path.join(UPLOAD_FOLDER, f"{filename}_mask.png")
            cv2.imwrite(mask_path, mask)
            tamper_data["mask"] = mask_path
        
        # Return the combined result
        return jsonify({
            "analysis": analysis_data,
            "tamper": tamper_data
        }), 200
    
    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
