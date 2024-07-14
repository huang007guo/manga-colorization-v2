import os

import numpy as np
import cv2
from filetype.types import IMAGE as FILETYPE_IMAGE, VIDEO as FILETYPE_VIDEO

def resize_pad(img, size = 256):
            
    if len(img.shape) == 2:
        img = np.expand_dims(img, 2)
        
    if img.shape[2] == 1:
        img = np.repeat(img, 3, 2)
        
    if img.shape[2] == 4:
        img = img[:, :, :3]

    pad = None        
            
    if (img.shape[0] < img.shape[1]):
        height = img.shape[0]
        ratio = height / (size * 1.5)
        width = int(np.ceil(img.shape[1] / ratio))
        img = cv2.resize(img, (width, int(size * 1.5)), interpolation = cv2.INTER_AREA)

        
        new_width = width + (32 - width % 32)
            
        pad = (0, new_width - width)
        
        img = np.pad(img, ((0, 0), (0, pad[1]), (0, 0)), 'maximum')
    else:
        width = img.shape[1]
        ratio = width / size
        height = int(np.ceil(img.shape[0] / ratio))
        img = cv2.resize(img, (size, height), interpolation = cv2.INTER_AREA)

        new_height = height + (32 - height % 32)
            
        pad = (new_height - height, 0)
        
        img = np.pad(img, ((0, pad[0]), (0, 0), (0, 0)), 'maximum')
        
    if (img.dtype == 'float32'):
        np.clip(img, 0, 1, out = img)

    return img[:, :, :1], pad


def find_files(target_dir, img_extensions, call_back: callable = None):
    """
    递归遍历target_dir目录下的所有图片文件（包括子目录），
    并将图片文件的路径存储到一个列表中返回。

    :param img_extensions:
    :param call_back:
    :param target_dir: 要遍历的目录路径
    :return: 包含所有图片路径的列表
    """
    # 图片文件的可能扩展名列表
    # img_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']

    image_paths = []  # 用于存储图片路径的列表

    # 递归遍历目录
    for root, dirs, files in os.walk(target_dir):
        for img_file in files:
            # 当前文件后缀
            extension = img_file.split('.')[-1]
            # 转换为小写
            extension = extension.lower()
            if extension in img_extensions:
                # for extension in img_extensions:
                # 使用fnmatch过滤出图片文件,使用is_image?
                # for img_file in fnmatch.filter(files, extension):
                # 获取完整的图片文件路径并添加到列表中
                img_path = os.path.join(root, img_file)
                if call_back:
                    call_back(img_path)
                else:
                    image_paths.append(img_path)
    # 这里可以根据需要对每个图片路径进行处理
    # process_image(img_path)  # 示例处理函数调用

    return image_paths

def find_images(target_dir, call_back: callable = None):
    img_extensions = [img_ext for img_ext in [now_file_type.EXTENSION for now_file_type in FILETYPE_IMAGE]]
    img_extensions.append("jpeg")
    return find_files(target_dir, img_extensions, call_back)