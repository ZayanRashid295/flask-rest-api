from flask import Flask, request, jsonify
import requests
from minio import Minio
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# MinIO configuration
minio_client = Minio(
    '89.116.73.11:9001',
    access_key='SGUQ9tbnE7euXxRhh7Oi',
    secret_key='fUA62XKgE9MYttmPmVSRN9HnHI1gb26id3FRUPSD',
    secure=False
)

bucket_name = 'natutech'


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    storage = request.headers.get('Storage', 'minio')  # default to MinIO if not specified

    filename = secure_filename(file.filename)

    if storage.lower() == 'nextcloud':
        nextcloud_url = 'http://89.116.73.11:8081/remote.php/dav/files/Hugo'
        nextcloud_user = 'your_nextcloud_user'
        nextcloud_password = 'your_nextcloud_password'

        response = requests.put(
            f'{nextcloud_url}/{filename}',
            data=file,
            auth=(nextcloud_user, nextcloud_password)
        )
        if response.status_code == 201:
            return jsonify({'message': 'File uploaded to Nextcloud successfully'}), 201
        else:
            return jsonify({'error': 'Failed to upload to Nextcloud'}), 500
    else:
        try:
            minio_client.put_object(bucket_name, filename, file, file.content_length)
            return jsonify({'message': 'File uploaded to MinIO successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/files', methods=['GET'])
def list_files():
    storage = request.headers.get('Storage', 'minio')  # default to MinIO if not specified

    if storage.lower() == 'nextcloud':
        nextcloud_url = 'http://89.116.73.11:8081/remote.php/dav/files/Hugo'
        nextcloud_user = 'your_nextcloud_user'
        nextcloud_password = 'your_nextcloud_password'

        response = requests.propfind(
            nextcloud_url,
            auth=(nextcloud_user, nextcloud_password)
        )
        if response.status_code == 207:
            return response.content, 200  # Assuming XML response
        else:
            return jsonify({'error': 'Failed to list files from Nextcloud'}), 500
    else:
        try:
            objects = minio_client.list_objects(bucket_name)
            files = [obj.object_name for obj in objects]
            return jsonify({'files': files}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
