from PIL import Image
from time import time
import numpy as np


def timecheck(func):
	def _wrapper(*args, **kwargs):
		t1 = time()
		result = func(*args, **kwargs)
		print(f'{func.__name__} worked for {time()-t1} seconds')
		return result
	return _wrapper


@timecheck
def makeGrey(img_name):
	if img_name is None:
		return None

	img = Image.open(img_name)
	return img.convert('L')
