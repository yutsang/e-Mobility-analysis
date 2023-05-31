import cv2
import numpy as np# Load image
img = cv2.imread('path/to/image.jpg')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blur, 50, 150)

# Display the result
cv2.imshow('Edges', edges)
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()



