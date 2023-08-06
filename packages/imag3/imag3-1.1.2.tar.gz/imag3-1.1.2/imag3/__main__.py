#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys
from dev0s import *

# settings.
SOURCE_NAME = "imag3"
SOURCE_PATH = Defaults.source_path(__file__, back=1)
sys.path.insert(1, Defaults.source_path(SOURCE_PATH, back=1))

# imports.
from imag3.classes.config import *
from imag3.classes import utils
from imag3.classes.image import image

# the cli object class.
class CLI_(CLI.CLI):
	def __init__(self):
		
		# variables.
		CLI.CLI.__init__(self,
			modes={
				"--convert /path/to/image.icns /path/to/image.png":"Convert an image file.",
				"--replace-pixels --input-hex #000000 --output-hex #000000 --input /path/to/image.png --output /path/to/image.converted.png":"Replace a specific color for a new color.",
				"--replace-colors --hex #000000 --input /path/to/image.png --output /path/to/image.converted.png":"Replace all colors for a new color.",
				"-h / --help":"Show the documentation.",
			},
			options={},
			alias=SOURCE_NAME,
			executable=__file__,)

		#
	def start(self):

		# check args.
		#self.arguments.check()
		
		# help.
		if self.arguments.present('-h') or self.arguments.present('--help'):
			print(self.documentation)

		# convert.
		elif self.arguments.present('--convert'):
			image.convert(
				input=self.arguments.get("--convert", index=1),
				output=self.arguments.get("--convert", index=2), )

		# replace pixels.
		elif self.arguments.present('--replace-pixels'):
			image.replace_pixels(
				input_hex=self.arguments.get("--input-hex"),
				output_pixel=self.arguments.get("--output-hex"),
				input_path=self.arguments.get("--input"),
				output_path=self.arguments.get("--output"),)

		# replace colors.
		elif self.arguments.present('--replace-colors'):
			image.replace_colors(
				pixel=self.arguments.get("--hex"),
				input_path=self.arguments.get("--input"),
				output_path=self.arguments.get("--output"),)

		# invalid.
		else: 
			self.invalid()

		#
	
# main.
if __name__ == "__main__":
	cli = CLI_()
	cli.start()


