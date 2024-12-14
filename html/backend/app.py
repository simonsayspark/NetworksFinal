from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Store messages in-memory (simple list)
messages = []

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
