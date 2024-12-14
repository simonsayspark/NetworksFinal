from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Define upload folder
UPLOAD_FOLDER = 'C:/Users/samon/Downloads/nginx-1.27.3/nginx-1.27.3/html/files2'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    print("folder not found")
    os.makedirs(UPLOAD_FOLDER)

    print("UPLOAD_FOLDER is set to:", app.config['UPLOAD_FOLDER'])


# In-memory store for messages
messages = []

# Endpoint to fetch all files
@app.route('/files', methods=['GET'])
def get_files():
    try:
        print("trying to find folder")
        print("UPLOAD_FOLDER is set to:", app.config['UPLOAD_FOLDER'])
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify([{'filename': f} for f in files])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to serve a specific file
@app.route('/files/<path:filename>', methods=['GET'])
def serve_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Endpoint to upload a file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return jsonify({'success': True, 'message': 'File uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# New Endpoint to upload a file
@app.route('/upload-file', methods=['POST'])
def upload_new_file():
    # Check if the request contains the 'file' part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    # Retrieve the file from the request
    uploaded_file = request.files['file']

    # Check if the file has a valid filename
    if uploaded_file.filename == '':
        return jsonify({'error': 'No file selected for upload'}), 400

    # Ensure the UPLOAD_FOLDER exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Save the file
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({'success': True, 'message': 'File uploaded successfully', 'filename': uploaded_file.filename})
    except Exception as e:
        # Return an error if something goes wrong
        return jsonify({'error': f'Failed to upload file: {str(e)}'}), 500


# Endpoint to delete a file
@app.route('/delete/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'success': True, 'message': 'File deleted successfully'})
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to fetch all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

# Endpoint to send a new message
@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.get_json()  # Parse the incoming JSON request
        sender = data.get('sender')  # Extract sender field
        message = data.get('message')  # Extract message field

        # Validate inputs
        if not sender or not message:
            return jsonify({'error': 'Sender and message are required'}), 400

        # Save the message
        messages.append({'sender': sender, 'message': message})
        return jsonify({'success': True, 'message': 'Message sent successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Make the app accessible from other devices by listening on 0.0.0.0
    app.run(host='0.0.0.0', port=5000)
