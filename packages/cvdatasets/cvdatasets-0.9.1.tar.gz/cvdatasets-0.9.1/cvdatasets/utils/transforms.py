import numpy as np
import random

from PIL import Image
from functools import partial

def dimensions(im):
	if isinstance(im, np.ndarray):
		if im.ndim != 3:
			import pdb; pdb.set_trace()
		assert im.ndim == 3, "Only RGB images are currently supported!"
		return im.shape

	elif isinstance(im, Image.Image):
		w, h = im.size
		c = len(im.getbands())
		# assert c == 3, "Only RGB images are currently supported!"
		return h, w, c

	else:
		raise ValueError("Unknown image instance ({})!".format(type(im)))

def rescale(im, coords, rescale_size, center_cropped=True, no_offset=False):
	h, w, c = dimensions(im)

	offset = 0
	if center_cropped:
		_min_val = min(w, h)
		wh = np.array([_min_val, _min_val])
		if not no_offset:
			offset = (np.array([w, h]) - wh) / 2

	else:
		wh = np.array([w, h])

	scale = wh / rescale_size
	return coords * scale + offset

####################
### Source: https://github.com/chainer/chainercv/blob/b52c71d9cd11dc9efdd5aaf327fed1a99df94d10/chainercv/transforms/image/color_jitter.py
####################


def _grayscale(img, channel_order="RGB"):
	"""
		from https://scikit-image.org/docs/dev/api/skimage.color.html#skimage.color.rgb2gray:
			Y = 0.2125 R + 0.7154 G + 0.0721 B
	"""

	if channel_order == "RGB":
		return 0.2125 * img[0] + 0.7154 * img[1] + 0.0721 * img[2]

	elif channel_order == "BGR":
		return 0.0721 * img[0] + 0.7154 * img[1] + 0.2125 * img[2]

	else:
		raise ValueError(f"Unknown channel order: {channel_order}")


def _blend(img_a, img_b, alpha):
	return alpha * img_a + (1 - alpha) * img_b


def _brightness(img, var):
	alpha = 1 + np.random.uniform(-var, var)
	return _blend(img, np.zeros_like(img), alpha), alpha


def _contrast(img, var, **kwargs):
	gray = _grayscale(img, **kwargs)[0].mean()

	alpha = 1 + np.random.uniform(-var, var)
	return _blend(img, gray, alpha), alpha


def _saturation(img, var, **kwargs):
	gray = _grayscale(img, **kwargs)

	alpha = 1 + np.random.uniform(-var, var)
	return _blend(img, gray, alpha), alpha


def color_jitter(img, brightness=0.4, contrast=0.4,
				 saturation=0.4, return_param=False,
				 min_value=0,
				 max_value=255,
				 channel_order="RGB"):
	"""Data augmentation on brightness, contrast and saturation.
	Args:
		img (~numpy.ndarray): An image array to be augmented. This is in
			CHW and RGB format.
		brightness (float): Alpha for brightness is sampled from
			:obj:`unif(-brightness, brightness)`. The default
			value is 0.4.
		contrast (float): Alpha for contrast is sampled from
			:obj:`unif(-contrast, contrast)`. The default
			value is 0.4.
		saturation (float): Alpha for contrast is sampled from
			:obj:`unif(-saturation, saturation)`. The default
			value is 0.4.
		return_param (bool): Returns parameters if :obj:`True`.
	Returns:
		~numpy.ndarray or (~numpy.ndarray, dict):
		If :obj:`return_param = False`,
		returns an color jittered image.
		If :obj:`return_param = True`, returns a tuple of an array and a
		dictionary :obj:`param`.
		:obj:`param` is a dictionary of intermediate parameters whose
		contents are listed below with key, value-type and the description
		of the value.
		* **order** (*list of strings*): List containing three strings: \
			:obj:`'brightness'`, :obj:`'contrast'` and :obj:`'saturation'`. \
			They are ordered according to the order in which the data \
			augmentation functions are applied.
		* **brightness_alpha** (*float*): Alpha used for brightness \
			data augmentation.
		* **contrast_alpha** (*float*): Alpha used for contrast \
			data augmentation.
		* **saturation_alpha** (*float*): Alpha used for saturation \
			data augmentation.
	"""
	funcs = list()
	if brightness > 0:
		funcs.append(('brightness', partial(_brightness, var=brightness)))
	if contrast > 0:
		funcs.append(('contrast', partial(_contrast, var=contrast, channel_order=channel_order)))
	if saturation > 0:
		funcs.append(('saturation', partial(_saturation, var=saturation, channel_order=channel_order)))
	random.shuffle(funcs)

	params = {'order': [key for key, val in funcs],
			  'brightness_alpha': 1,
			  'contrast_alpha': 1,
			  'saturation_alpha': 1}
	for key, func in funcs:
		img, alpha = func(img)
		params[key + '_alpha'] = alpha

	if min_value is not None:
		img = np.maximum(img, min_value)

	if max_value is not None:
		img = np.minimum(img, max_value)

	if return_param:
		return img, params
	else:
		return img
