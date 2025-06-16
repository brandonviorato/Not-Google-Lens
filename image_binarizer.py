import cv2

# Pre-process image through binarization (make grayscale)
def binarize(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image_path = './temp/gray.jpg'
    
    cv2.imwrite(gray_image_path, gray_image)

    return gray_image_path