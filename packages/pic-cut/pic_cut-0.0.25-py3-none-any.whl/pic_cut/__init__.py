#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'pic_cut'

from PIL import Image
import math
import os
import cached_url

MARGIN = 0.05

def getImg(path):
	try:
		return Image.open(path) 
	except:
		return

def isAnimated(fn):
	if fn.endswith('mp4'):
		return True
	gif = getImg(fn)
	if not gif:
		return False
	try:
		gif.seek(1)
	except EOFError:
		return False
	else:
		return True

def cut(path, limit=100, size_factor = 2):
	img = getImg(path)

	w, h = img.size

	for piece in range(1, limit + 1):
		nh, moves = computeSize(h, piece)
		if nh < size_factor * w:
			break

	if len(moves) <= 1 or nh > size_factor * w or h < size_factor * 1.2 * w:
		moves = []

	for p, m in enumerate(moves):
		working_slice = img.crop((0, m, w, m + nh))
		main_path, _ = os.path.splitext(path)
		fn = '%s_%d.png' % (main_path, p)
		working_slice.save(fn)
		yield fn

def cutSafe(image, size_factor = 2):
	cached_url.get(image, force_cache=True, mode='b')
	fn = cached_url.getFilePath(image)
	if isAnimated(fn):
		return [fn]
	if not getImg(fn):
		return []
	return list(cut(fn, size_factor = size_factor)) or [fn]

def getCutImages(images, limit=10, size_factor = 2):
	result = []
	for image in images:
		for c in cutSafe(image, size_factor = size_factor):
			result.append(c)
			if len(result) >= limit:
				return result
	return result

def computeSize(h, p):
	raw_h = h / (p - MARGIN * (p - 1))
	nh = math.ceil(raw_h)
	moves = [math.ceil(raw_h * ((1 - MARGIN) * step)) for step in range(p - 1)]
	moves.append(h - nh)
	return nh, moves
