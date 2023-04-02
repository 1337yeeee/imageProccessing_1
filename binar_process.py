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


def niblackCriteria(img_name, window_size=21, k=-0.2):
	if img_name is None:
		return None

	img = makeGrey(img_name)
	pixels = np.array(img)
	w, h = pixels.shape

	# creating an array full of 0 shape like pixels
	binary = np.zeros_like(pixels)

	for i in range(w):
		for j in range(h):
			# setting edges
			left_i = i - window_size if i - window_size > 0 else 0
			right_i = i + window_size if i + window_size < w else w-1
			left_j = j - window_size if j - window_size > 0 else 0
			right_j = j + window_size if j + window_size < h else h-1	
			
			mean = np.mean(pixels[left_i:right_i+1, left_j:right_j+1])
			std = np.std(pixels[left_i:right_i+1, left_j:right_j+1])
			# Calculate threshold
			t = mean + k * std

			# Create binary image
			binary[i, j] = 255 if pixels[i, j] > t else 0
	
	out = Image.fromarray(binary, mode='L')
	out.show()
	
	return out
