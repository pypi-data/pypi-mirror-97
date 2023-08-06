import numpy as np

from os.path import isfile
from PIL import Image

from cvdatasets.utils import retry_operation

def read_image(im_path, n_retries=5):
	assert isfile(im_path), "Image \"{}\" does not exist!".format(im_path)
	return retry_operation(n_retries, Image.open, im_path, mode="r")


def asarray(im, dtype=np.uint8):
	if isinstance(im, np.ndarray):
		return im.astype(dtype)

	elif isinstance(im, Image.Image):
		return np.asarray(im, dtype=dtype)

	else:
		raise ValueError("Unknown image instance ({})!".format(type(im)))
