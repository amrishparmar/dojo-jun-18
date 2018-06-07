#!/usr/bin/env python
import argparse
from collections import defaultdict
import string
import sys

from PIL import Image, ImageFont, ImageDraw


def load_image_as_grayscale(filename):
    return Image.open(filename).convert('LA')

def resize_image(img):
    width, height = img.size
    return img.resize((width, height//2), resample=Image.BICUBIC)

def get_luminance(characters):
    font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", 12)
    luminance = defaultdict(list)
    for character in characters:
        space = Image.new("L", (8, 16))
        draw = ImageDraw.Draw(space)
        draw.text((2,2), character, 255, font=font)

        lum = space.resize((1,1), Image.BICUBIC).getpixel((0,0))
        # print("{} = {}".format(character, lum))
        luminance[lum].append(character)
    return luminance


def normalize_luminance(luminance):
    max_key = max(luminance)
    normalized_luminance = {}
    for key, values in luminance.items():
        normalized_key = round((key * 255) / max_key)
        normalized_luminance[normalized_key] = values
    return normalized_luminance

def convert_to_ascii(image_filename):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    args = parser.parse_args(sys.argv[1:])

    img = load_image_as_grayscale(args.image)
    img = resize_image(img)
    img.save('output.png')
    luminance = get_luminance(string.printable[:-5])
    luminance = normalize_luminance(luminance)
    from pprint import pprint
    pprint(dict(luminance))
    ascii_ = convert_to_ascii(args.image)
    print(ascii_)


if __name__ == '__main__':
    main()
