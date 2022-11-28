import cv2

image = cv2.imread("checker.png")

# converting BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#cv2.imshow('image', image_rgb)
cv2.imwrite('floors.png', image_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()
