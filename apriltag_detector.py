from pupil_apriltags import Detector
import cv2

"""
Changes the AprilTag detector's used family.
"""
def use_family(family):
    global apriltag_family
    apriltag_family = family

"""
Using given parameters, initializes to AprilTag detector
"""
def create_detector():
    global detector
    detector = Detector(families=apriltag_family)

"""
From the AprilTag detector's results
creates a list of corners which is easy
to create lines between in a single loop.

Detector returns corners:
A(x, y), 
B(x, y), 
C(x, y),
...    ,
N(x, y)

Function returns corners:
A(int(x), int(y)), 
B(int(x), int(y)), 
C(int(x), int(y)),
...              , 
N(int(x), int(y))
"""
def calculate_corners(result):
    corners = []
    for corner in result.corners:
        corners.append((int(corner[0]), 
                        int(corner[1])))

    return corners + [corners[0]]

"""
Draws a circle on given coordinates
"""
def draw_circle(image, X, Y):
    cv2.circle(image, 
                (X, Y),
                5, (0, 0, 255), -1)

"""
Writes text on given coordinates.
"""
def write_text(image, X, Y, text):
    cv2.putText(image, 
                text, 
                (X, Y - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 2)

"""
Finds AprilTags in image.
Uses the detector created with create_detector() and 
detects AprilTags from the family defined with use_family(family),
or "tag36h11", if not defined.
"""
def find_apriltags(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = detector.detect(gray)
    return results