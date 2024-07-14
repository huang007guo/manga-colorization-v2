import os
import argparse
import shutil
import sys

import numpy as np
import matplotlib.pyplot as plt

from colorizator import MangaColorizator
from utils.utils import find_images, is_color_image, auto_shutdown_pc
from PIL import Image


def process_image(image, colorizator, args):
    colorizator.set_image(image, args.size, args.denoiser, args.denoiser_sigma)

    return colorizator.colorize()


def colorize_single_image(image_path, save_path, colorizator, args):
    # image = Image.open(image_path)
    if not is_color_image(image_path):
        image = plt.imread(image_path)
        # colorization = process_image(np.array(image.convert('RGB')), colorizator, args)
        colorization = process_image(image, colorizator, args)

        # plt.imsave(save_path, colorization)
        img = Image.fromarray((colorization * 255).astype('uint8'))
        img.save(save_path, quality=args.quality)
    else:
        # 直接复制图片文件
        shutil.copy(image_path, save_path)


    return True


def colorize_images(target_path, colorizator, args):
    # images = os.listdir(args.path)
    images = find_images(args.path)

    for file_path in images:
        # file_path = os.path.join(args.path, image_name)
        if os.path.isdir(file_path):
            continue
        image_name = os.path.basename(file_path)
        name, ext = os.path.splitext(image_name)
        if args.format is not None:
            image_name = name + '.' + args.format
            # if (ext != '.png'):
            #     image_name = name + '.png'

        print(file_path)
        # 输出目录,如果没有默认为当前目录/colorization,如果配置了,里面还会新建子目录(path\图片所在子目录)
        if args.output is not None:
            # 如果是多个目录的场景 args.isMultiple,替换的时候需要把path的最后一个目录去除掉再替换,这样就会保留最后一个目录了
            path = args.path
            if args.isMultiple:
                path = os.path.dirname(path)
            target_path = file_path.replace(path, args.output)
            target_path = os.path.dirname(target_path)
            # 新建目录
            os.makedirs(target_path, exist_ok=True)
        save_path = os.path.join(target_path, image_name)
        colorize_single_image(file_path, save_path, colorizator, args)


def parse_args():
    parser = argparse.ArgumentParser()
    # 多个图片,路径英文逗号分割
    parser.add_argument("-p", "--path", required=True, help='path to image or directory, multiple images separated by comma')
    # 输出目录,如果没有默认为当前目录/colorization,如果配置了,里面还会新建子目录(path\图片所在子目录)
    parser.add_argument("-o", "--output", default=None, help='output path')
    # 图片的目标格式,不指定为图片原始格式
    parser.add_argument("-f", "--format", default=None, help='output image format')
    # 图片质量,默认为90
    parser.add_argument("-q", "--quality", type=int, default=90, help='output image quality')
    # 运行完成后关机
    parser.add_argument('-sd', "--shutdown", dest='shutdown', action='store_true')
    parser.add_argument("-gen", "--generator", default='networks/generator.zip')
    parser.add_argument("-ext", "--extractor", default='networks/extractor.pth')
    parser.add_argument('-g', '--gpu', dest='gpu', action='store_true')
    parser.add_argument('-nd', '--no_denoise', dest='denoiser', action='store_false')
    parser.add_argument("-ds", "--denoiser_sigma", type=int, default=25)
    # parser.add_argument("-s", "--size", type = int, default = 576)
    parser.add_argument("-s", "--size", type=int, default=None)
    parser.set_defaults(gpu=False)
    parser.set_defaults(denoiser=True)
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse_args()

    if args.gpu:
        device = 'cuda'
    else:
        device = 'cpu'

    colorizer = MangaColorizator(device, args.generator, args.extractor)
    args.paths = args.path.split(',')
    if len(args.paths) > 1:
        args.isMultiple = True
    else:
        args.isMultiple = False
    for path in args.paths:
        args.path = path
        if os.path.isdir(args.path):
            colorization_path = os.path.join(args.path, 'colorization')
            if not os.path.exists(colorization_path):
                os.makedirs(colorization_path)

            colorize_images(colorization_path, colorizer, args)

        elif os.path.isfile(args.path):

            split = os.path.splitext(args.path)

            if split[1].lower() in ('.jpg', '.png', '.jpeg'):
                new_image_path = split[0] + '_colorized' + '.png'

                colorize_single_image(args.path, new_image_path, colorizer, args)
            else:
                print('Wrong format')
        else:
            print('Wrong path')
    auto_shutdown_pc(args)
