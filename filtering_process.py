from PIL import Image
from time import time
import numpy as np
from binar_process import timecheck
from scipy.signal import medfilt2d
from scipy.signal import convolve2d


@timecheck
def linear_filter(img, matrix):
	pixels = np.array(img)
	padding = matrix.shape
	padded_pixels = np.pad(pixels, ((padding[0]//2, padding[0]//2), (padding[1]//2, padding[1]//2), (0,0)), mode='reflect')
	pixels_out = np.zeros_like(pixels)

	for channel in range(pixels.shape[2]):
		pixels_out[:,:,channel] = convolve2d(padded_pixels[:,:,channel], matrix, mode='valid')

	pixels_out = np.clip(pixels_out, 0, 255).astype('uint8')
	out = Image.fromarray(pixels_out)
	return out


@timecheck
def median_filter(img, shape=(9,9)):
	pixels = np.array(img)
	padded_pixels = np.pad(pixels, ((shape[0]//2, shape[0]//2), (shape[1]//2, shape[1]//2), (0,0)), mode='reflect')
	pixels_out = np.zeros_like(padded_pixels)

	for channel in range(pixels.shape[2]):
		pixels_out[:,:,channel] = medfilt2d(padded_pixels[:,:,channel], kernel_size=shape)

	out = Image.fromarray(pixels_out)
	return out


@timecheck
def gaussian_filter(img, width=13, sigma=3):
	kernel = gaussian_kernel(width, sigma)
	return linear_filter(img, kernel)


@timecheck
def gaussian_kernel(width, sigma):
	x = np.arange(-width//2 + 1, width//2 + 1)
	y = np.arange(-width//2 + 1, width//2 + 1)
	xx, yy = np.meshgrid(x, y)
	kernel = np.exp(-(xx**2 + yy**2) / (2.0 * sigma**2))
	kernel = kernel / np.sum(kernel)
	return kernel


# SLOW
@timecheck
def linear_filter_slow(img, matrix):
	pixels = np.array(img)
	padding = matrix.shape
	padded_pixels = np.pad(pixels, ((padding[0]//2, padding[0]//2), (padding[1]//2, padding[1]//2), (0,0)), mode='reflect')
	pixels_out = np.zeros_like(pixels)

	for i in range(pixels.shape[0]):
		for j in range(pixels.shape[1]):
			pixels_out[i,j,0] = max(min(np.sum(padded_pixels[i:i+padding[0], j:j+padding[1], 0]*matrix), 255), 0)
			pixels_out[i,j,1] = max(min(np.sum(padded_pixels[i:i+padding[0], j:j+padding[1], 1]*matrix), 255), 0)
			pixels_out[i,j,2] = max(min(np.sum(padded_pixels[i:i+padding[0], j:j+padding[1], 2]*matrix), 255), 0)

	out = Image.fromarray(pixels_out)
	return out


@timecheck
def median_filter_slow(img, matrix):
	pixels = np.array(img)
	padding = matrix.shape
	padded_pixels = np.pad(pixels, ((padding[0]//2, padding[0]//2), (padding[1]//2, padding[1]//2), (0,0)), mode='reflect')
	pixels_out = np.zeros_like(pixels)

	for i in range(pixels.shape[0]):
		for j in range(pixels.shape[1]):
			pixels_out[i,j,0] = np.median(padded_pixels[i:i+padding[0], j:j+padding[1], 0])
			pixels_out[i,j,1] = np.median(padded_pixels[i:i+padding[0], j:j+padding[1], 1])
			pixels_out[i,j,2] = np.median(padded_pixels[i:i+padding[0], j:j+padding[1], 2])

	out = Image.fromarray(pixels_out)
	return out

