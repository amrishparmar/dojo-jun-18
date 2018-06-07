#!/usr/bin/env python
import argparse
from collections import defaultdict
import string
import sys
from random import choice

from PIL import Image, ImageFont, ImageDraw


def load_image_as_grayscale(filename):
    return Image.open(filename).convert('LA')


def resize_image(img, scale_factor=8):
    width, height = img.size
    return img.resize(
        (width // scale_factor, height // (2 * scale_factor)),
        resample=Image.BICUBIC)


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
        normalized_luminance[255 - normalized_key] = values
    return normalized_luminance


def get_closest(mapping, value):
    return mapping.get(value, mapping[min(mapping.keys(), key=lambda k: abs(k-value))])


def convert_to_ascii(image, luminance):
    out = ""
    for n, pixel in enumerate(image.getdata(band=0)):
        closest = get_closest(luminance, pixel)
        if n != 0 and n % image.width == 0:
            out += "\n"
        out += choice(closest)

    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('--scale-factor', type=int)
    args = parser.parse_args(sys.argv[1:])

    img = load_image_as_grayscale(args.image)
    img = resize_image(img, args.scale_factor)
    # img.save('output.png')
    luminance = get_luminance(string.printable[:-5])
    luminance = normalize_luminance(luminance)

    ascii_ = convert_to_ascii(img, luminance)
    print(ascii_)


if __name__ == '__main__':
    main()
