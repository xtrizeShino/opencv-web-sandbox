from flask import render_template, Response
import matplotlib.pyplot as plt
import io
import numpy as np
from web_root import app
from PIL import Image
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

# generate Histgram Image from input image
def generate_hist_image(image):
    # divide Image to RGB channels
    b, g, r = image[:,:,0], image[:,:,1], image[:,:, 2]
    # generate Histgram as each RGB
    hist_b = cv2.calcHist([b],[0],None,[256],[0,256])
    hist_g = cv2.calcHist([g],[0],None,[256],[0,256])
    hist_r = cv2.calcHist([r],[0],None,[256],[0,256])
    # write Plot
    plt.plot(hist_r, color='r', label="r")
    plt.plot(hist_g, color='g', label="g")
    plt.plot(hist_b, color='b', label="b")
    # set xlim, ylim
    plt.xlim(0, 255)
    # convert Histgram to numpy array
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    enc = np.array(Image.open(buf).convert('RGB'))
    plt.gca().clear()
    # resize
    enc = cv2.resize(enc, (320, 240))
    return enc

# Callback function for Image Proc            
def imageproc_resize_and_hist(image):
    # resize Image
    image = cv2.resize(image, (1024, 768))
    h, w = image.shape[:2]
    # put Histgram on Image
    enc = generate_hist_image(image)
    # set offset
    dx=10
    dy=10
    # set Matrix for affine
    M = np.array([[1, 0, dx],[0, 1, dy]], dtype=float)
    # put Image by warpAffine
    image = cv2.warpAffine(enc, M, (w, h), image, borderMode=cv2.BORDER_TRANSPARENT)
    # output image
    return image

# Streaming Contents
@app.route("/streams/video_feed")
def video_feed():
    # return Newest Multimedia data
    return Response(gen(Camera(imageproc_resize_and_hist)),
                    mimetype="multipart/x-mixed-replace; boundary=frame")