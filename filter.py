import sys
from PIL import Image
import numpy as np
import argparse
import datetime


def create_namespace():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--image', default=None, metavar='',
                            help='set image to transform into a mosaic in grayscale')
    arg_parser.add_argument('-r', '--result', default='res.jpg', metavar='',
                            help='set name with which the result will be saved')
    return arg_parser.parse_args(sys.argv[1:])


def open_image(image_name):
    while True:
        try:
            img = Image.open(image_name)
            return np.array(img)
        except Exception as e:
            register_an_error(e)
            print('Incorrect input.')
            print('Enter the image name in the current directory '
                  'or specify the full path to your file. Write "exit" if you want to exit.')
            image_name = input()
            if image_name == 'exit':
                exit()


def register_an_error(error):
    try:
        with open('./log.txt', 'a') as file:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write("[{}] - {}\n".format(now, error))
    except Exception as e:
        with open('./log.txt', 'w+') as file:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write("[{}] - {}\n".format(now, e))
            file.write("[{}] - {}\n".format(now, error))


def set_grayscale():
    while True:
        try:
            return int(input('Set grayscale.\n'))
        except Exception as e:
            register_an_error(e)
            print('Incorrect input. Please enter grayscale in correct format.')


def set_mosaic_dimensions():
    while True:
        try:
            height = int(input('Set the mosaic height.\n'))
            break
        except Exception as e:
            register_an_error(e)
            print('Incorrect input. Please enter mosaic height in correct format.')
    while True:
        try:
            width = int(input('Set the mosaic width.\n'))
            break
        except Exception as e:
            register_an_error(e)
            print('Incorrect input. Please enter mosaic width in correct format.')
    return height, width


def replace_with_gray(dimensions, array, step):
    height = dimensions[0]
    width = dimensions[1]
    for x in range(0, len(array), height):
        for y in range(0, len(array[1]), width):
            # find out the average brightness
            average_brightness = np.sum(array[x: x + height, y: y + width]) // (height * width * 3)
            # bring the color of average brightness to the step in increments of 50
            color = int(average_brightness // step) * step
            # paint the cell into mosaics in the resulting color
            array[x: x + height, y: y + width] = np.full(3, color)
    return Image.fromarray(array)


def save_image(result_name, array):
    while True:
        try:
            return array.save(result_name)
        except Exception as e:
            register_an_error(e)
            print('Enter a different name for the output image or specify the correct file format.')
            result_name = input()


if __name__ == '__main__':
    namespace = create_namespace()
    arr = open_image(namespace.image)
    image = replace_with_gray(set_mosaic_dimensions(), arr, set_grayscale())
    save_image(namespace.result, image)
