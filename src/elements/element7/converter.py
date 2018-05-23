# import cv2
# import numpy as np
#
# inp = input()
# blue = inp[2]
# green = inp[1]
# red = inp[0]
#
# color = np.uint8([[[blue, green, red]]])
# hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
#
# hue = hsv_color[0][0][0]
#
# print("Lower bound is :"),
# print("[" + str(hue - 10) + ", 100, 100]\n")
#
# print("Upper bound is :"),
# print("[" + str(hue + 10) + ", 255, 255]")
