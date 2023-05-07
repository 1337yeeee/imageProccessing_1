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
	for l in range(N):
		for k in range(M):
			sum_matrix = 0.0
			for n in range(N):
				for m in range(M):
					e = cmath.exp(- 2j * np.pi * (float(l * m) / N + float(k * n) / M))
					sum_matrix += pixels[m, n] * e
			dft2d[k, l] = sum_matrix
	return dft2d


@timecheck
def IDFT2D(dft2d):
	M, N = dft2d.shape
	pixels = np.zeros((M, N))
	for n in range(N):
		for m in range(M):
			sum_ = 0.0
			for l in range(N):
				for k in range(M):
					e = cmath.exp(2j * np.pi * (float(l * m) / N + float(k * n) / M))
					sum_ += dft2d[k, l] * e
			pixel = sum_.real / (M*N)
			pixels[m, n] = pixel
	return pixels
