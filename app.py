from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/emojify', methods=['POST'])
def handle_post():
    """Handle POST request with integer and jpg image"""
    try:
        # Get integer parameter
        if 'granularity' not in request.form:
            return jsonify({'status': 'error', 'message': 'Missing granularity parameter'}), 400
        
        try:
            integer_value = int(request.form['granularity'])
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Granularity parameter must be a valid integer'}), 400
        
        # Get image file
        if 'image' not in request.files:
            return jsonify({'status': 'error', 'message': 'Missing image file'}), 400
        
        image_file = request.files['image']
        
        # Validate that file is a jpg
        if image_file.filename == '':
            return jsonify({'status': 'error', 'message': 'No image file selected'}), 400
        
        if not image_file.filename.lower().endswith(('.jpg', '.jpeg')):
            return jsonify({'status': 'error', 'message': 'Image must be a jpg/jpeg file'}), 400
        
        # Process the data here
        response = {
            'status': 'success',
            'message': 'Data received successfully',
            'integer': integer_value,
            'image_filename': image_file.filename
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({'message': 'api is running'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
