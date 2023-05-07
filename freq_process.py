import numpy as np
from PIL import Image
import cmath
from binar_process import timecheck


@timecheck
def make(image):
	image = image.convert('L')
	pixels = np.asarray(image)

	dft2d = DFT2D(pixels)
	g = IDFT2D(dft2d)

	return Image.fromarray(np.uint8(np.clip(g, 0, 255)), mode='L')


@timecheck
def DFT2D(pixels):
	M, N = np.shape(pixels)
	dft2d = np.zeros((M, N), dtype=complex)
	for k in range(M):
		for l in range(N):
			m, n = np.meshgrid(np.arange(M), np.arange(N), indexing='ij')
			e = np.exp(-2j * np.pi * (l * m / N + k * n / M))
			dft2d[k, l] = np.sum(pixels * e)
	return dft2d


@timecheck
def IDFT2D(dft2d):
	M, N = dft2d.shape
	pixels = np.zeros((M, N))
	for m in range(M):
		for n in range(N):
			k, l = np.meshgrid(np.arange(M), np.arange(N), indexing='ij')
			e = np.exp(2j * np.pi * (l * m / N + k * n / M))
			pixels[m, n] = np.sum(dft2d * e).real / (M*N)
	return pixels
