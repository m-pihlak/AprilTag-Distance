import numpy as np
from shapely.geometry import Polygon

"""
Using the square's corners' and center coordinates,
finds the estimate on how much the square should be multiplied
to reach top view size.
Example:
Visible:
    _________
   /        /
  /        /
 /________/
Visible area = vS
Top view:
___________
|         |
|         |
|         |
|_________|
Top view area = tS
tS = coeff * vS
Method gives estimation of coeff.

Since the center point of the square will be offset on the projection
depending on the angle of the square, then the offset from center
will give an estimation on how much the square is rotated in some direction.

Using both diagonals, it gives a decent estimation on how much of the square's
projection needs to be added so it reaches full size.

If the square is rotated only by 1 diagonal, then it will not give a good
estimate on how much the area has changed, since the center point will 
stay relatively in the center. That is why using both the diagonals'
coefficients and dividing the larger by the other will give another
estimation on the turning. Since the coefficients are small, adding
1 to them avoids big coefficients from divisions. After the division
the 1 is subtracted.

Finally the diagonals' coefficients are added together and multiplied by 100
and rounded (similarly the division coefficient is multiplied by 100 and rounded)
and squared to get an estimation on how much the projection should be increased
to reach full size.

Final result is the larger between the sum and the div, divided by 100
and incremented by 1 to create a multiplier which is used to estimate the
full area.
"""
def estimated_size_multiplier(corners, center):
    a, b, c, d = corners
    
    diag1_half1 = np.linalg.norm( a - center )
    diag1_half2 = np.linalg.norm( c - center )

    diag2_half1 = np.linalg.norm( b - center )
    diag2_half2 = np.linalg.norm( d - center )

    diag1_coeff = abs( diag1_half1 - diag1_half2 ) / ( diag1_half1 + diag1_half2 )
    diag2_coeff = abs( diag2_half1 - diag2_half2 ) / ( diag2_half1 + diag2_half2 )
    
    diag_div_coeff = 1
    if diag1_coeff < diag2_coeff:
        diag_div_coeff = ( 1 + diag2_coeff ) / ( 1 + diag1_coeff) - 1
    else:
        diag_div_coeff = ( 1 + diag1_coeff ) / ( 1 + diag2_coeff) - 1

    diag_coeff1 = round( 100 * ( diag1_coeff + diag2_coeff ) ) ** 2
    diag_coeff2 = round( 100 * diag_div_coeff ) ** 2

    diag_coeff = max( diag_coeff1, diag_coeff2 ) / 100

    return diag_coeff + 1

"""
Uses the estimated size multiplier to get the coeff to multiply the area.
Uses the shapely package to calculate the polygon's area from it's corners.
Returns the result of multiplying the area and coefficient.
"""
def percieved_size(corners, center):
    coeff = estimated_size_multiplier(corners, center)
    return Polygon(corners).area * coeff

"""
Uses an April Tag, it's distance from the camera and the projection's
corners and center to get the focal length of the camera.
This serves as a means of calibration for the program.
"""
def calibrate(apriltag_w, dist, corners, center):
    global focal_length
    
    apriltag_area = apriltag_w ** 2
    percieved_area = percieved_size(corners, center)

    focal_length = np.sqrt(percieved_area / apriltag_area) * dist

"""
Using the April Tag's width and projection's corners' and center coordinates,
finds the distance of the projection from the camera.
Uses the focal_length value gotten from calibration.
"""
def apriltag_distance(apriltag_width, corners, center):
    apriltag_area = apriltag_width ** 2
    percieved_area = percieved_size(corners, center)

    return np.sqrt(apriltag_area / percieved_area) * focal_length