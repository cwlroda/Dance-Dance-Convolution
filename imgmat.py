import sys
import numpy
import cv2

numpy.set_printoptions(threshold=sys.maxsize)

frame = cv2.imread("/Users/cwlroda/Desktop/I100.png", 1)
# frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
print(frame)

numpy.save("I100", frame)

img = numpy.load("/Users/cwlroda/Desktop/Python/DDC/I100.npy")

cv2.imshow("DDC", img)
cv2.waitKey(0)
cv2.destroyAllWindows() 