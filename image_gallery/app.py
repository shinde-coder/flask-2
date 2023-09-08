from flask import Flask, render_template, request, redirect, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Get a list of uploaded image filenames
    image_files = File.query.all()
    return render_template('index.html', image_files=image_files)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            # Check if the UPLOAD_FOLDER directory exists, and create it if not
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_file = File(filename=filename)
            db.session.add(new_file)
            db.session.commit()
    return redirect('/')

@app.route('/uploaded_files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download_image/<file_id>')
def download_image(file_id):
    file = File.query.get(file_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)

@app.route('/delete_image/<file_id>')
def delete_image(file_id):
    file = File.query.get(file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(file_path)
    db.session.delete(file)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
