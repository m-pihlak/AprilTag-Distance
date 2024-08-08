import numpy as np
from shapely.geometry import Polygon

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

def percieved_size(corners, center):
    coeff = estimated_size_multiplier(corners, center)
    return Polygon(corners).area * coeff

def calibrate(apriltag_w, dist, corners, center):
    global focal_length
    
    apriltag_area = apriltag_w ** 2
    percieved_area = percieved_size(corners, center)

    focal_length = np.sqrt(percieved_area / apriltag_area) * dist

def apriltag_distance(apriltag_width, corners, center):
    apriltag_area = apriltag_width ** 2
    percieved_area = percieved_size(corners, center)

    return np.sqrt(apriltag_area / percieved_area) * focal_length