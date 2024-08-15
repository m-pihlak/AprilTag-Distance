import cv2
import calculate
import numpy as np

"""
Sets the image which pictures are drawn on.
"""
def use_image(img):
    global image, width, height, bottom_center
    image = img
    height, width = image.shape[:2]
    bottom_center = (width // 2, height)

"""
Sets the result used for drawing
"""
def use_result(r):
    global result, corners, center, distance
    result = r
    corners = calculate_corners()
    center = (int(result.center[0]), int(result.center[1]))

"""
From the April Tag detector's results
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
def calculate_corners():
    corners = []
    for corner in result.corners:
        corners.append( (int(corner[0]),
                         int(corner[1])) )
    return np.array(corners, dtype=np.int32)

"""
Draws a border around the April Tags in the given image.
"""
def border():
    border_corners = np.append(corners, [corners[0]], 0)
    for i, corner1 in enumerate(border_corners[:-1]):
        corner2 = border_corners[i + 1]
        cv2.line(image, 
                corner1, corner2,
                (0, 255, 0), 2)
    


"""
Draws a circle on given coordinates
"""
def center_circle():
    cv2.circle( image, 
                center,
                5, (0, 0, 255), -1)

"""
Writes the tag family on given coordinates.
"""
def tag_family():
    cv2.putText(image, 
                result.tag_family.decode("utf-8"), 
                (center[0], center[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 2)
"""
Draws lines connecting results
"""
def center_line():
    cv2.line(image, 
             bottom_center, 
             center,
             (0, 0, 255), 2)

"""
Writes distance on center line.
"""
def distance_text():
    cv2.putText(image,
                f"Distance: {round(calculate.apriltag_distance(result.tag_id, corners, center))}mm",
                ((center[0] + bottom_center[0]) // 2,
                (center[1] + bottom_center[1]) // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 255), 2 )

"""
Calibrates April Tag distance calculator
"""
def calibrate(dist):
    # Shows the April Tag cutout.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(image.shape[:2], dtype="uint8")

    cv2.fillPoly(mask, 
                 [np.array(corners, dtype=np.int32)], 
                 (255, 255, 255))
    
    masked = cv2.bitwise_and(gray, gray, mask=mask)
    cv2.imshow("masked", masked)
    """
    calculate.calibrate(result.tag_id, dist, corners, center)