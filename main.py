from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/face-swap', methods=['POST'])
def face_swap():
    # For now, just return a placeholder response
    data = request.json
    return jsonify({
        "message": "Placeholder face swap completed!",
        "received": data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 