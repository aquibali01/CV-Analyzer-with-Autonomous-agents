# from flask import Flask, request, render_template
# import os

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def upload_form():
#     return render_template('upload.html')

# @app.route('/', methods=['POST'])
# def upload_file():
#     file = request.files['file']
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return 'File uploaded successfully'
#     else:
#         return 'Invalid file format'

# if __name__ == '__main__':
#     app.run(debug=True)

import redis
import uuid
from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

redis_client = redis.Redis(host='localhost', port=6379, db=0)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        # Generate unique ID for the file
        file_id = str(uuid.uuid4())

        # Save the file to the uploads folder
        filename = file_id + '.' + file.filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Store the file ID in Redis
        redis_client.set(file_id, filename)

        return jsonify({'status': 'success', 'file_id': file_id})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)

