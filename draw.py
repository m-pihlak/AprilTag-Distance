import cv2
import calculate

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
    distance = calculate.distance(corners, center, width, height)

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
def calculate_corners():
    corners = []
    for corner in result.corners:
        corners.append((int(corner[0]), 
                        int(corner[1])))

    return corners + [corners[0]]

"""
Draws a border around the AprilTags in the given image.
"""
def border():
    for i, corner1 in enumerate(corners[:-1]):
        corner2 = corners[i + 1]
        cv2.line(image, 
                corner1, corner2,
                (0, 255, 0), 2)


"""
Draws a circle on given coordinates
"""
def center_circle():
    cv2.circle(image, 
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
def center_line_text():
    cv2.putText(image,
                f"Distance: {distance}m",
                ((center[0] - bottom_center[0]) // 2 + bottom_center[0],
                (center[1] - bottom_center[1]) // 2 + bottom_center[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 255), 2 )