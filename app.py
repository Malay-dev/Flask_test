# Import necessary libraries
from flask import Flask, render_template, Response
import cv2
import get_qr
# import recog_face
# Initialize the Flask app
app = Flask(__name__)


def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/test')
def test():
    camera = cv2.VideoCapture(0)
    return Response(get_qr.capture_qr(camera=camera), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/face')
# def face():
#     return Response(recog_face.face(camera=camera), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
