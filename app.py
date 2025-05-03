from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Here you would implement your face recognition logic
        # For example:
        # detected_name, accuracy = perform_face_recognition(file_path)

        # For now, we'll use placeholder values
        detected_name = "John Doe"  # Replace with actual detection result
        accuracy = 95.7  # Replace with actual accuracy percentage

        # Move file to static folder for display
        static_file_path = os.path.join('static', 'uploads', filename)
        os.makedirs(os.path.dirname(static_file_path), exist_ok=True)

        # If file already exists in static folder, remove it
        if os.path.exists(static_file_path):
            os.remove(static_file_path)

        # Copy the file to static folder
        import shutil
        shutil.copy2(file_path, static_file_path)

        return render_template('result.html',
                               filename=filename,
                               person_name=detected_name,
                               accuracy=accuracy)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
