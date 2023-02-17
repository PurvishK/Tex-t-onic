import cv2

def load_image(path):
    img = cv2.imread(path,1)
    img = cv2.resize(img, (0,0), fx=0.8, fy=0.8)
    return img

def display_image(image,label="Image"):
    cv2.imshow(label, image)

def save_image(image,label="new_image.png",path=''):
    cv2.imwrite(path+label, image)