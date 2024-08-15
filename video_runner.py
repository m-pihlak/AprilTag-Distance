from imutils.video import VideoStream
import imutils
import time
import cv2

import apriltag_detector
import draw

"""
Changes the April Tag detector's used family.
"""
def use_family(family):
    print("[INFO] setting April Tag family...")
    apriltag_detector.use_family(family)

"""
Creates the April Tag detector.
"""
def create_detector():
    print("[INFO] creating April Tag detector...")
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

        results = apriltag_detector.find_apriltags(frame)

        draw.use_image(frame)
        for result in results:
            draw.use_result(result)
            draw.border()
            draw.center_circle()
            draw.tag_family()
            draw.center_line()
            draw.distance_text()

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            break

"""
Calibrates values for April Tag distance.
"""
def calibrate_values(dist):
    print("[INFO] calibrating video stream...")
    print("[INFO] make sure April Tag id is April Tag size in mm")
    print(f"[INFO] place April Tag {dist}mm away")
    print("[INFO] press 'r' key when ready.")
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=500)

        results = apriltag_detector.find_apriltags(frame)

        draw.use_image(frame)
        
        if (len(results) > 0):
            result = results[0]
            draw.use_result(result)
            draw.calibrate(dist)
            draw.border()
            draw.center_circle()

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            break


"""
Cleans up after the video stream.
"""
def stop_stream():
    print("[INFO] stopping video stream...")
    cv2.destroyAllWindows()
    vs.stop()


"""
Calibrates the April Tag detector distance calculator.
"""
def calibrate(dist):
    start_stream()
    calibrate_values(dist)
    stop_stream()


"""
Runs all the video stream methods in order.
"""
def stream():
    start_stream()
    run_stream()
    stop_stream()