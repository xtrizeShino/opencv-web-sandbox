from flask import render_template, Response
from web_root import app
import cv2

class Camera:
    def __init__(self, callback):
        # Open Video device
        self.video = cv2.VideoCapture(0)
        self.imageproc = callback

    def __del__(self):
        # Close Video device
        self.video.release()

    def get_frame(self):
        # fetch new frame from Video device
        _, image = self.video.read()
        image = self.imageproc(image)
        if image is not None:
            # Set Quarity for compress with jpg
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), app.config['WEBCAM_QUARITY']]
            # Convert jpg on memory
            _, frame = cv2.imencode('.jpg', image, encode_param)
        else:
            # Video devices are not found.
            frame = None
        # return Image as jpg-binary 
        return frame

# HTML for put Streaming Contents
@app.route("/streams/stream")
def stream():
    return render_template("streams/stream.html")

# Generate Frame in Streaming Contents
def gen(camera):
    while True:
        # get Image as jpg-binary
        frame = camera.get_frame()
        if frame is not None:
            # update frame in Multimedia 
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n"
                   + frame.tobytes() + b"\r\n")

# Callback function for Image Proc            
def imageproc_x2(image):
    h, w = image.shape[:2]
    image = cv2.resize(image, (w*2, h*2))
    return image

# Streaming Contents
@app.route("/streams/video_feed")
def video_feed():
    # return Newest Multimedia data
    return Response(gen(Camera(imageproc_x2)),
                    mimetype="multipart/x-mixed-replace; boundary=frame")