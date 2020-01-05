#import packages
from imutils.video import VideoStream
from easydict import EasyDict
import argparse
import imutils
import numpy as np
import time
import datetime
import math

# construct argument parser and parse arguments
args = EasyDict({
    "min_area": 1000
})

# read from webcam
vs = VideoStream(src=0).start()
time.sleep(2.0)

# initialise first frame in video stream
firstFrame = None
start = datetime.datetime.now()

# loop over video frames
while True:
    # grab current frame
    frame = vs.read()
    frame = cv2.flip(frame, 1)

	# resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
    if ((datetime.datetime.now() - start).seconds % 1.1 == 0):
        firstFrame = gray

    left = frame[0:0, 250:280]
    right = frame[250:0, 500:280]

    # compute the absolute difference between the current frame and
	# first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    printbox = None

	# loop over the contours
    for c in cnts:
		# if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

		# compute the bounding box for the contour and draw it on the frame,
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 1)
        printbox = box

    # draw template box
    # cv2.line(frame, (200, 120), (200, 240), (255, 0, 0), 2)
    cv2.line(frame, (0, 120), (50, 120), (255, 0, 0), 2)
    cv2.line(frame, (50, 120), (50, 240), (255, 0, 0), 2)
    # cv2.line(frame, (120, 240), (200, 240), (255, 0, 0), 2)
    cv2.line(frame, (50, 240), (130, 240), (255, 0, 0), 2)
    # cv2.line(frame, (120, 240), (110, 280), (255, 0, 0), 2)
    cv2.line(frame, (130, 240), (140, 280), (255, 0, 0), 2)

    # print total area of bounding boxes
    # cv2.rectangle(frame, (5, 10), (85, 25), (0, 0, 0), -1)

	# show the frame and record if the user presses a key
    cv2.imshow("Tracker", frame)
    key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

    elif key == ord("t"):

        k = box[2][0] - box[0][0]
        l = box[2][1] - box[0][1]
        m = box[3][0] - box[0][0]
        n = box[3][1] - box[0][1]

        o = math.atan(n/m)
        o = math.degrees(o)
        o = -o

        p = math.atan(l/k)
        p = math.degrees(p)
        p = -p

        q = (p+o)/2

        print(o)
        print(p)
        print(q)

        if q >= -10 and q <= 20:
            print("T")
        elif q >= 30 and q <= 60:
            print("V")
        elif q >= 70 and q <= 100:
            print("I")

        firstFrame = gray

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()