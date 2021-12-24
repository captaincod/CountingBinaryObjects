import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

full_rect = np.array([[1, 1, 1, 1],
                      [1, 1, 1, 1],
                      [1, 1, 1, 1],
                      [1, 1, 1, 1]])

punched_down_rect = np.array([[1, 1, 1, 1],
                              [1, 1, 1, 1],
                              [1, 0, 0, 1],
                              [1, 0, 0, 1]])
punched_right_rect = np.rot90(punched_down_rect)
punched_up_rect = np.rot90(punched_right_rect)
punched_left_rect = np.rot90(punched_up_rect)


def match(a, mask):
    if np.all(a == mask):
        return True
    return False


def count_objects(img):
    full_rects = 0
    punched_right_rects = 0
    punched_left_rects = 0
    punched_up_rects = 0
    punched_down_rects = 0
    for y in range(0, img.shape[0] - 1):
        for x in range(0, img.shape[1] - 1):
            sub = img[y:y + 4, x:x + 4]
            sub = sub & 1
            if match(sub, full_rect) or match(sub, np.rot90(full_rect)):
                full_rects += 1
                continue
            if match(sub, punched_right_rect):
                punched_right_rects += 1
                continue
            if match(sub, punched_left_rect):
                punched_left_rects += 1
                continue
            if match(sub, punched_up_rect):
                punched_up_rects += 1
                continue
            if match(sub, punched_down_rect):
                punched_down_rects += 1
                continue
    punched_rects = [punched_right_rects, punched_left_rects, punched_up_rects, punched_down_rects]
    return full_rects, *punched_rects


image = np.load('ps.npy').astype('uint')
labeled = label(image)

output = open('results.txt', 'w')
output.write(f'Всего объектов на изображении: {np.max(labeled)}\n')

result = count_objects(labeled)
for i in range(len(result)):
    output.write(f'Объектов {i+1} типа:: {result[i]}\n')

output.close()

"""
plt.figure()
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(labeled)
plt.show()
"""