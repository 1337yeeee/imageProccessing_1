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


class BinarIMG:
	@timecheck
	def __init__(self, img_name, window_size=21, k=-0.2, r=128):
		img = makeGrey(img_name)
		self.pixels = np.array(img)
		self.window_size = window_size if window_size%2 else window_size+1
		self.k = k
		self.r = r
		self.local_mean, self.local_std = self.calc_mean_std()
		self.gavr = self.gavrCriteria()
		self.otsu = self.otsuCriteria()
		self.wolf = self.wolfCriteria()
		self.niblack = self.niblackCriteria()
		self.sauvola = self.sauvolaCriteria()
		self.bradley = self.bradleyRothCriteria()

	@timecheck
	def gavrCriteria(self):
		pixels = self.pixels
		t = np.average(pixels)
		pixels = (pixels >= t) * 255

		out = Image.fromarray(pixels.astype(np.uint8), mode="L")
		
		return out


	@timecheck
	def otsuCriteria(self):
		pixels = self.pixels

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

		return out


	@timecheck
	def niblackCriteria(self):
		window_size = self.window_size
		k = self.k
		pixels = self.pixels

		local_mean = self.local_mean
		local_std = self.local_std

		# Calculate threshold
		t = local_mean + k * local_std

		# Create binary image
		binary = (pixels > t).astype(np.uint8) * 255
		out = Image.fromarray(binary, mode='L')

		return out


	@timecheck
	def sauvolaCriteria(self):
		window_size = self.window_size
		k = self.k
		r = self.r 
		pixels = self.pixels

		local_mean = self.local_mean
		local_std = self.local_std


		# Calculate threshold
		threshold = local_mean * (1 + k * ((local_std / r) - 1))

		# Create binary image
		binary = (pixels > threshold).astype(np.uint8) * 255
		out = Image.fromarray(binary, mode='L')

		return out


	@timecheck
	def wolfCriteria(self):
		window_size = self.window_size
		k = self.k
		r = self.r 
		pixels = self.pixels
		
		local_mean = self.local_mean
		local_std = self.local_std
		
		# Compute threshold
		m = np.amin(pixels)
		R = np.amax(local_std)
		t = 0.5*local_mean + 0.5*m + 0.5*(local_std/R)*(local_mean-m)
		
		# Create binary image
		binary = (pixels > t).astype(np.uint8) * 255
		out = Image.fromarray(binary, mode='L')
		
		return out

	@timecheck
	def bradleyRothCriteria(self):
		window_size = self.window_size
		k = self.k
		pixels = self.pixels
		
		# Calculate local mean
		pad_width = window_size // 2
		pixels_padded = np.pad(pixels, pad_width, mode='edge')
		local_sum = np.cumsum(np.cumsum(pixels_padded, axis=0), axis=1)
		local_sum = local_sum[window_size-1:-1, window_size-1:-1] + local_sum[:-(window_size), :-(window_size)] - local_sum[window_size-1:-1, :-(window_size)] - local_sum[:-(window_size), window_size-1:-1]
		local_mean = local_sum / (window_size ** 2)

		# Pad local_mean
		local_mean_padded = np.pad(local_mean, ((0, 1), (0, 1)), mode='constant')

		# Calculate threshold with an extra row and column of zeros
		threshold = local_mean_padded * (1 - k)
		threshold = np.pad(threshold, ((0, 1), (0, 1)), mode='edge')

		# Create binary image
		binary = (pixels > threshold[:-1, :-1]).astype(np.uint8) * 255
		out = Image.fromarray(binary, mode='L')

		return out

	@timecheck
	def calc_mean_std(self):
		# Calculate local mean and standard deviation of pixels
		local_mean = generic_filter(self.pixels, np.mean, size=self.window_size)
		local_std = np.sqrt(generic_filter(self.pixels**2, np.mean, size=self.window_size) - local_mean**2)
		return local_mean, local_std

	def getimages(self):
		return {
			'gavr': 	self.gavr,
			'otsu': 	self.otsu,
			'niblack': 	self.niblack,
			'sauvola': 	self.sauvola,
			'wolf': 	self.wolf,
			'bradley':	self.bradley,
		}
