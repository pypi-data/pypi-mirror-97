#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from imag3.classes.config import *
from PIL import Image as _Image_

# the image object class.
class Image(object):
	def __init__(self):	
		a=1
		#
	def convert(self, input='logo.png', output='logo.ico'):
		filename = input
		img = _Image_.open(filename)
		img.save(output)
		print(f"Successfully converted image {input} to {output}.")
	def replace_pixels(self, input_path=None, output_path=None, input_hex=None, output_hex=None):
		img = _Image_.open(input_path)
		pixels = img.load()
		input_rgb, output_rgb = input_hex, output_hex # self.hex_to_rgb(input_hex), self.hex_to_rgb(output_hex)
		for i in range(img.size[0]): 
			for j in range(img.size[1]):
				print(pixels[i,j], "VS", input_rgb)
				if pixels[i,j] == input_rgb:
					pixels[i,j] = output_rgb
		img.save(output_path)
	def replace_colors(self, input_path=None, output_path=None, hex=None):
		img = _Image_.open(input_path)
		pixels = img.load()
		rgb = hex #self.hex_to_rgb(hex)
		for i in range(img.size[0]):
			for j in range(img.size[1]):
				if pixels[i,j] != rgb and pixels[i,j] != (0, 0, 0, 0):
					pixels[i,j] = rgb
		img.save(output_path)
	def rgb_to_hex(self, tuple):
		return '#%02x%02x%02x' % tuple
	def hex_to_rgb(self, _hex_):
		return tuple(int(_hex_[i:i+2], 16) for i in (0, 2, 4))

# initialized objects.
image = Image()