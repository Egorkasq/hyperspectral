import cv2
import os
import numpy as np


class HyperspectralImageStitch():

    def __init__(self, image_path, channel, spectr_size, down_up=True):

        self.image_path = image_path  # Дирректория с изображениями
        self.channel = channel  # Необоходимая частота спектра
        self.spectr_size = spectr_size  # ширина спектра в пикселях
        self.down_up = down_up          # движение просходит снизу вверх

    def computationOfChannelWidth(self):
        images = os.listdir(self.image_path)
        images.sort()
        img = cv2.imread(self.image_path + images[0], 1)
        start_channel = 0
        end_channel = img.shape[1]
        assert img is not None
        for num, i in enumerate(img[self.channel]):
            if (i != [0, 0, 0]).all():
                start_channel = num
                break
        reverse_image = np.flip(img[self.channel])

        for num, i in enumerate(reverse_image):
            if (i != [0, 0, 0]).all():
                end_channel = reverse_image.shape[0] - num
                break
        print(start_channel, end_channel)
        return start_channel, end_channel

    def hyperspectral_stitching(self):

        start_channel, end_channel = self.computationOfChannelWidth()
        images = os.listdir(self.image_path)
        images.sort()
        img = cv2.imread(self.image_path + images[0], 1)
        img = img[:, start_channel: end_channel, ]
        res_img = img[self.channel - self.spectr_size // 2:self.channel + self.spectr_size // 2, ]
        images.pop(0)

        for num, i in enumerate(images):
            img = cv2.imread(self.image_path + i, 1)
            img = img[:, start_channel: end_channel, ]
            line = img[self.channel - self.spectr_size // 2:self.channel + self.spectr_size // 2, ]
            if self.down_up:
                res_img = np.concatenate((line, res_img))
            else:
                res_img = np.concatenate((res_img, line))
            cv2.imshow('123', res_img)
            cv2.waitKey(0)
        return res_img


image = HyperspectralImageStitch('/home/error/PycharmProjects/Spiiran_files/hiperspectral/images/', 1380, 12, False)
image.hyperspectral_stitching()
cv2.imwrite('hyperspectral_image.jpg', 1)
