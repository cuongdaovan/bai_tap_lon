

im = cv2.imread("./car/IMG_0392.jpg")
im_gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
noise_removal = cv2.bilateralFilter(im_gray,9,75,75)
# equal_histogram = cv2.equalizeHist(noise_removal)
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
# morph_image = cv2.morphologyEx(equal_histogram,cv2.MORPH_OPEN,kernel,iterations=20)
# sub_morp_image = cv2.subtract(equal_histogram,morph_image)
# ret,thresh_image = cv2.threshold(sub_morp_image,0,255,cv2.THRESH_OTSU)
# canny_image = cv2.Canny(thresh_image,250,255)
# kernel = np.ones((3,3), np.uint8)
# dilated_image = cv2.dilate(canny_image,kernel,iterations=1)
# D:/CodePython/BSX/10.jpg