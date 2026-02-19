from flask import Flask, request, jsonify, send_file
from typing import Any
from emojify import emojify
from PIL import Image
import io
app: Flask = Flask(__name__)

@app.route('/api/emojify', methods=['POST'])
def handle_post() -> tuple[Any, int]:
    """Handle POST request with integer and jpg image"""
    try:
        # Get integer parameter
        if 'granularity' not in request.form:
            return jsonify({'status': 'error', 'message': 'Missing granularity parameter'}), 400
        try:
            granularity = int(request.form['granularity'])
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Granularity parameter must be a valid integer'}), 400
        
        # Get image file
        if 'image' not in request.files:
            return jsonify({'status': 'error', 'message': 'Missing image file'}), 400
        image_file = request.files['image']   # type is FileStorage
        
        # Validate that file is a jpg
        if image_file.filename == '':
            return jsonify({'status': 'error', 'message': 'No image file selected'}), 400
        if not image_file.filename.lower().endswith(('.jpg', '.jpeg')):
            return jsonify({'status': 'error', 'message': 'Image must be a jpg/jpeg file'}), 400

        # Call the emojify function
        image: Image = Image.open(image_file)
        emojified_image: Image = emojify(image, granularity)

        # Return the emojified image to the user
        # Save the image into a BytesIO object
        in_memory_bytes_buffer = io.BytesIO()
        emojified_image.save(in_memory_bytes_buffer, format='JPEG')
        # Reset the stream position to the beginning
        in_memory_bytes_buffer.seek(0)
        # Return the image from memory
        return (send_file(in_memory_bytes_buffer, mimetype='image/jpeg'), 200)

        # Process the data here
        # response: dict[str, Any] = {
        #     'status': 'success',
        #     'message': 'Data received successfully',
        #     'integer': granularity,
        #     'image_filename': image_file.filename
        # }
        
        return emojified_image, 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/test', methods=['GET'])
def test() -> tuple[Any, int]:
    """Test endpoint"""
    return jsonify({'message': 'api is running'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
