# -*- coding: utf8 -*-
import os

from PIL import Image


def filter_image_size(image_path: str, min_width: float, min_height: float):
    """
    筛选掉指定大小范围的image
    """
    image = Image.open(image_path)
    width, height = image.size
    if width < min_width or height < min_height:
        return True
    else:
        return False


def filter_main(image_path: str):
    min_width = 224
    min_height = 224
    for font_dir in os.listdir(image_path):
        font_path = os.path.join(image_path, font_dir)
        for font_file in os.listdir(font_path):
            font_file_path = os.path.join(font_path, font_file)
            if filter_image_size(font_file_path, min_width, min_height):
                print(f"image file {font_file_path} is not satisfied, remove it.")
                os.remove(font_file_path)


if __name__ == '__main__':
    pass
    # path = "E:\\PycharmProjects\\font-identifier\\train_test_images\\train"
    # min_width = 224
    # min_height = 224
    # for font_dir in os.listdir(path):
    #     font_path = os.path.join(path, font_dir)
    #     for font_file in os.listdir(font_path):
    #         font_file_path = os.path.join(font_path, font_file)
    #         if filter_image_size(font_file_path, min_width, min_height):
    #             print(font_file_path)
