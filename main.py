from flask import Flask, request, jsonify
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

app = Flask(__name__) 

# Configure your S3 credentials and bucket name
S3_BUCKET = os.getenv('S3_BUCKET_NAME')
S3_KEY = os.getenv('AWS_ACCESS_KEY_ID')
S3_SECRET = os.getenv('AWS_SECRET_KEY')
S3_REGION = os.getenv('AWS_REGION')

s3_client = boto3.client('s3', 
                         aws_access_key_id=S3_KEY, 
                         aws_secret_access_key=S3_SECRET, 
                         region_name=S3_REGION)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    try:
        s3_client.upload_fileobj(file, S3_BUCKET, file.filename)
        return jsonify({'message': 'Upload successful!'}), 200
    except NoCredentialsError:
        return jsonify({'message': 'Credentials not available'}), 500
    except PartialCredentialsError:
        return jsonify({'message': 'Incomplete credentials'}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
