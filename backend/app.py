from flask import Flask, request, jsonify
import base64
import numpy as np
import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)

app = Flask(__name__)

def detect_faces(image):
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = mp_face_detection.process(imgRGB)
    face_count = 0
    if results.detections:
        face_count = len(results.detections)
    return face_count


@app.route('/detect_faces', methods=['POST'])
def detect_faces_api():
    try:
        data = request.get_json()
        image_data = data['image']
        decoded_img = base64.b64decode(image_data)
        nparr = np.frombuffer(decoded_img, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        face_count = detect_faces(img)
        return jsonify({'face_count': face_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 

