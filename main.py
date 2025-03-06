from flask import Flask, request, jsonify
from google.cloud import storage
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/face-swap', methods=['POST'])
def face_swap():
    data = request.json
    source_url = data.get('source_url')
    target_url = data.get('target_url')
    output_path = data.get('output_path')

    # Basic validation
    if not source_url or not target_url or not output_path:
        return jsonify({"error": "Missing required fields"}), 400

    local_source_path = f"/tmp/source_{uuid.uuid4()}.png"
    local_target_path = f"/tmp/target_{uuid.uuid4()}.mp4"
    local_output_path = f"/tmp/output_{uuid.uuid4()}.mp4"

    storage_client = storage.Client()
    bucket = storage_client.bucket("facesync-452817.appspot.com")  # Adjust or parse the bucket name
    bucket.blob(source_url).download_to_filename(local_source_path)
    bucket.blob(target_url).download_to_filename(local_target_path)

    try:
        subprocess.check_call([
            "python3", "run.py",
            "--source", local_source_path,
            "--target", local_target_path,
            "--output", local_output_path
            # Add any extra flags as needed
        ], cwd="/app/roop")
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to run roop", "details": str(e)}), 500

    # Upload the processed output
    output_blob = bucket.blob(output_path)
    output_blob.upload_from_filename(local_output_path)

    # Then replace the placeholder return with a success message:
    return jsonify({
        "message": "Face swap completed successfully",
        "output_path": output_path
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 