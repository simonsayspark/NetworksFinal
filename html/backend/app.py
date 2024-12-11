import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database setup
db = SQLAlchemy(app)

# Define a model for file records
class FileRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=True)  # To store file content

    def __repr__(self):
        return f"<File {self.filename}>"

# Create the database tables
with app.app_context():
    db.create_all()

# Define the folder containing dummy files
DUMMY_FOLDER = "C:/Users/samon/Downloads/nginx-1.27.3/nginx-1.27.3/html/dummy_files"

# Add files from the folder to the database
@app.route('/add_files', methods=['POST'])
def add_files_to_db():
    if not os.path.exists(DUMMY_FOLDER):
        return jsonify({"error": "Dummy folder not found."}), 403
    

    for filename in os.listdir(DUMMY_FOLDER):
        filepath = os.path.join(DUMMY_FOLDER, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                content = file.read()
                # Check if the file already exists in the database
                existing_file = FileRecord.query.filter_by(filename=filename).first()
                if not existing_file:
                    new_file = FileRecord(filename=filename, content=content)
                    db.session.add(new_file)

    db.session.commit()
    return jsonify({"message": "Files added to the database successfully."})

# List all files from the database
@app.route('/files', methods=['GET'])
def list_files():
    files = FileRecord.query.all()
    return jsonify([{'id': file.id, 'filename': file.filename, 'content': file.content} for file in files])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
