from PIL import Image
from time import time
import numpy as np
from scipy.ndimage import generic_filter


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


@timecheck
def gavrCriteria(img_name):
	if img_name is None:
		return None

	img = makeGrey(img_name)
	pixels = np.array(img)
	t = np.average(pixels)
	pixels = (pixels >= t) * 255

	img.close()
	out = Image.fromarray(pixels.astype(np.uint8), mode="L")
	out.show()
	return out


@timecheck
def otsuCriteria(img_name):
	if img_name is None:
		return None

	img = makeGrey(img_name)
	pixels = np.array(img)

	hist, _ = np.histogram(pixels, bins=range(257))
	norm_hist = hist / pixels.size

	# cумма hist[i] [1, 2, 3, 4, 5] -> [ 1  3  6 10 15]
	cumsum_hist = np.cumsum(norm_hist)
	# cумма hist[i]*i [1, 2, 3, 4, 5] -> [ 0  2  8 20 40]
	cumsum_mean = np.cumsum(np.arange(256) * norm_hist)

	mu = cumsum_mean[-1]  # overall mean

	var_b = cumsum_hist * (1 - cumsum_hist) * (cumsum_mean - mu)**2
	threshold = np.argmax(var_b)

	bin_img = np.zeros_like(pixels)
	bin_img[pixels > threshold] = 255

	out = Image.fromarray(bin_img, mode="L")
	out.show()

	return out


@timecheck
def niblackCriteria(img_name, window_size=43, k=-0.2):
	if img_name is None:
		return None

	img = makeGrey(img_name)
	pixels = np.array(img)

	# Calculate local mean and standard deviation of pixels
	local_mean = generic_filter(pixels, np.mean, size=window_size)
	local_std = np.sqrt(generic_filter(pixels**2, np.mean, size=window_size) - local_mean**2)

	# Calculate threshold
	t = local_mean + k * local_std

	# Create binary image
	binary = (pixels > t).astype(np.uint8) * 255
	out = Image.fromarray(binary, mode='L')
	out.show()

	return out
