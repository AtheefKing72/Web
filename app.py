from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import io

app = Flask(__name__)

# Ensure upload and converted directories exist
UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return "No file uploaded", 400

    image_file = request.files['image']
    output_format = request.form.get('format')
    resize_width = request.form.get('width')
    resize_height = request.form.get('height')

    if not image_file or not output_format:
        return "Invalid input", 400

    try:
        # Open image
        img = Image.open(image_file)

        # Resize if dimensions provided
        if resize_width and resize_height:
            img = img.resize((int(resize_width), int(resize_height)))

        # Convert image
        converted_io = io.BytesIO()
        img.save(converted_io, format=output_format.upper())
        converted_io.seek(0)

        return send_file(
            converted_io,
            mimetype=f"image/{output_format.lower()}",
            as_attachment=True,
            download_name=f"converted_image.{output_format.lower()}"
        )
    except Exception as e:
        return f"Conversion error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
