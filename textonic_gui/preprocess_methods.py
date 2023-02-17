import cv2
from image_helper_functions import *
import numpy as np
from skimage.transform import hough_line, hough_line_peaks
from skimage.transform import rotate
from skimage.feature import canny
from skimage.io import imread
from skimage.color import rgb2gray
# import matplotlib.pyplot as plt
from scipy.stats import mode

def grayscale(image, path):
    if(len(image.shape)>=3):
        # convert to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        save_image(image,"_grayscaled.png",path)
    return image

def edge_detection(image):
    kernel = np.ones((5,5),'uint8')
    image = cv2.dilate(image,kernel,iterations=1)
    edges = cv2.Canny(image, 100, 70)
    return edges

def morphology(image):
    # threshold
    thresh = cv2.threshold(image, 190, 255, cv2.THRESH_BINARY)[1]

    # apply morphology
    kernel = np.ones((7,7), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((9,9), np.uint8)
    morph = cv2.morphologyEx(morph, cv2.MORPH_ERODE, kernel)
    return morph

def contour_detection(image):
    # convert to grayscale
    # convert to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # threshold
    thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)[1]\

    # apply morphology
    kernel = np.ones((7,7), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((9,9), np.uint8)
    morph = cv2.morphologyEx(morph, cv2.MORPH_ERODE, kernel)

    # get largest contour
    contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    area_thresh = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > area_thresh:
            area_thresh = area
            big_contour = c


    # get bounding box
    x,y,w,h = cv2.boundingRect(big_contour)

    # draw filled contour on black background
    mask = np.zeros_like(gray)
    mask = cv2.merge([mask,mask,mask])
    cv2.drawContours(mask, [big_contour], -1, (255,255,255), cv2.FILLED)

    # apply mask to input
    result1 = image.copy()
    result1 = cv2.bitwise_and(result1, mask)

    # crop result
    result2 = image[y:y+h, x:x+w]
    return result2


def skew_correction(image):
    # convert to edges
    # Classic straight-line Hough transform between 0.1 - 180 degrees.
    tested_angles = np.deg2rad(np.arange(0.1, 180.0))
    h, theta, d = hough_line(edge_detection(image), theta=tested_angles)
    
    # find line peaks and angles
    accum, angles, dists = hough_line_peaks(h, theta, d)
    
    # round the angles to 2 decimal places and find the most common angle.
    most_common_angle = mode(np.around(angles, decimals=2))[0]
    
    # convert the angle to degree for rotation.
    skew_angle = np.rad2deg(most_common_angle - np.pi/2)
    print(skew_angle[0])
    # skewed_img=rotate(image, skew_correction(image), cval=1)
    return skew_angle[0]


def blur_correction(image):
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen_img = cv2.filter2D(image, -1, sharpen_kernel)
    return sharpen_img

def shadow(image):
    dilated_img = cv2.dilate(image, np.ones((7,7), np.uint8)) 
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(image, bg_img)
    norm_img = diff_img.copy() # Needed for 3.x compatibility
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    _, thr_img = cv2.threshold(norm_img, 230, 0, cv2.THRESH_TRUNC)
    cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    return thr_img

def denoise(image):
    dst = cv2.fastNlMeansDenoisingColored(image, None, 11, 6, 7, 21)
    denoised_img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    return denoised_img