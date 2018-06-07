import sys

from PIL import Image
from PIL.Image import BICUBIC


def load_image_as_grayscale(filename):
	return Image.open(filename).convert('LA')


def resize_image(img):
	width, height = img.size
	return img.resize((width, height//2), resample=BICUBIC)


def main():
	img = load_image_as_grayscale(sys.argv[1])
	img = resize_image(img)

	# do the processing here

	img.save('output.png')


if __name__ == '__main__':
	main()