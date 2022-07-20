"""
本文件获得正面的模型图
"""



import cv2
import numpy as np


img = cv2.imread("eg.jpg")



src_list = [(547, 144), (1322, 118), (1380, 836), (485, 877)]
"""
for i, pt in enumerate(src_list):
    cv2.circle(img, pt, 5, (0, 0, 255), -1)
    cv2.putText(img,str(i+1),(pt[0]+5,pt[1]+10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)"""
pts1 = np.float32(src_list)

w,h = 753,753


pts2 = np.float32([[0, 0], [0, w - 2], [h - 2, w - 2], [h - 2, 0]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(img, matrix, (h, w))
result = np.rot90(result)
result = cv2.flip(result, 0)

cv2.imshow("Perspective transformation", result)
cv2.waitKey(0)

cv2.imwrite("model1.jpg",result)