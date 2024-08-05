from imutils.video import VideoStream
import imutils
import time
import cv2

import apriltag_detector

"""
Changes the AprilTag detector's used family.
"""
def use_family(family):
    print("[INFO] setting AprilTag family...")
    apriltag_detector.use_family(family)

"""
Creates the AprilTag detector.
"""
def create_detector():
    print("[INFO] creating AprilTag detector...")
    apriltag_detector.create_detector()

"""
Starts the video stream.
"""
def start_stream():
    print("[INFO] starting video stream...")
    global vs
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

"""
Runs the video stream.
"""
def run_stream():
    print("[INFO] running video stream...")
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=500)

        apriltag_detector.draw_corners_around_image(frame)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            break

"""
Cleans up after the video stream.
"""
def stop_stream():
    print("[INFO] stopping video stream...")
    cv2.destroyAllWindows()
    vs.stop()

"""
Runs all the video stream methods in order (except setting the tag family).
"""
def stream():
    create_detector()
    start_stream()
    run_stream()
    stop_stream()