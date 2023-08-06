import numpy as np

from cvdatasets.dataset.mixins.base import BaseMixin

class BBoxMixin(BaseMixin):

	def bounding_box(self, i):
		bbox = self._get("bounding_box", i)
		return [bbox[attr] for attr in "xywh"]

class MultiBoxMixin(BaseMixin):
	_all_keys=[
		"x", "x0", "x1",
		"y", "y0", "y1",
		"w", "h",
	]

	def multi_box(self, i, keys=["x0","x1","y0","y1"]):
		assert all([key in self._all_keys for key in keys]), \
			f"unknown keys found: {keys}. Possible are: {self._all_keys}"

		boxes = [
			dict(
				x=box["x0"], x0=box["x0"], x1=box["x1"],

				y=box["y0"], y0=box["y0"], y1=box["y1"],

				w=box["x1"] - box["x0"],
				h=box["y1"] - box["y0"],
			)
			for box in self._get("multi_box", i)["objects"]
		]

		return [[box[key] for key in keys] for box in boxes]

class BBCropMixin(BBoxMixin):

	def __init__(self, *, crop_to_bb=False, crop_uniform=False, **kwargs):
		super(BBCropMixin, self).__init__(**kwargs)
		self.crop_to_bb = crop_to_bb
		self.crop_uniform = crop_uniform

	def bounding_box(self, i):
		x,y,w,h = super(BBCropMixin, self).bounding_box(i)
		if self.crop_uniform:
			x0 = x + w//2
			y0 = y + h//2

			crop_size = max(w//2, h//2)

			x,y = max(x0 - crop_size, 0), max(y0 - crop_size, 0)
			w = h = crop_size * 2
		return x,y,w,h

	def get_example(self, i):
		im_obj = super(BBCropMixin, self).get_example(i)
		if self.crop_to_bb:
			bb = self.bounding_box(i)
			return im_obj.crop(*bb)
		return im_obj
