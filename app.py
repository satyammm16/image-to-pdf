from flask import Flask, render_template, request, send_file, send_from_directory
from PIL import Image
import io

app = Flask(__name__)

PAGE_SIZES = {
    'A4': (595, 842),      # points (1 pt = 1/72 inch)
    'Letter': (612, 792)
}

QUALITY_MAP = {
    'high': 95,
    'medium': 75,
    'low': 50
}

# Google verification route
@app.route('/google9b580fd35a95a6b4.html')
def serve_verification():
    return send_from_directory('static', 'google9b580fd35a95a6b4.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    images = request.files.getlist('images')
    page_size_key = request.form.get('page_size', 'A4')
    quality_key = request.form.get('quality', 'high')

    if not images:
        return "No images uploaded", 400

    page_width, page_height = PAGE_SIZES.get(page_size_key, PAGE_SIZES['A4'])
    quality = QUALITY_MAP.get(quality_key, 95)

    pdf_pages = []

    for img_file in images:
        img = Image.open(img_file).convert('RGB')

        # Resize image to fit page size, maintaining aspect ratio
        img.thumbnail((page_width, page_height))

        # Create a blank white background image for page
        page = Image.new('RGB', (page_width, page_height), 'white')

        # Calculate position to center the image
        x = (page_width - img.width) // 2
        y = (page_height - img.height) // 2
        page.paste(img, (x, y))

        pdf_pages.append(page)

    pdf_bytes = io.BytesIO()
    pdf_pages[0].save(pdf_bytes, format='PDF', save_all=True, append_images=pdf_pages[1:], quality=quality)
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, mimetype='application/pdf', download_name='converted.pdf')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
