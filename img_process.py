from PIL import Image
from time import time
from math import sqrt


def timecheck(func):
	def _wrapper(*args, **kwargs):
		t1 = time()
		result = func(*args, **kwargs)
		print(f'{func.__name__} worked for {time()-t1} seconds')
		return result
	return _wrapper


def apply_filters(opt, img1_name, img2=None, channels="RGB"):
	if opt == "None":
		return channelImage(img1_name, channels)
	elif opt == "Square mask image":
		return maskImage(img1_name, "S", channels)
	elif opt == "Circle mask image":
		return maskImage(img1_name, "C", channels)
	elif opt == "Add":
		return sumImage(img1_name, img2, channels)
	elif opt == "Multiply":
		return multImage(img1_name, img2, channels)
	elif opt == "Max":
		return maxImage(img1_name, img2, channels)
	elif opt == "Min":
		return minImage(img1_name, img2, channels)
	elif opt == "Average":
		return avgImage(img1_name, img2, channels)
	else:
		return None


@timecheck
def channelImage(img1_name, channels):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	if channels == "RGB":
		return img1

	out = Image.new("RGB", img1.size)

	pixels = img1.load()

	pixels_out = out.load()

	for x in range(img1.width):
		for y in range(img1.height):
			r, g, b = pixels[x, y]

			r_out = r if "R" in channels else 0
			g_out = g if "G" in channels else 0
			b_out = b if "B" in channels else 0

			pixels_out[x, y] = (r_out, g_out, b_out)

	img1.close()
	return out


@timecheck
def sumImage(img1_name, img2, channels="RGB"):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	img1, img2 = rescale_image(img1, img2)

	if img1.size != img2.size:
		raise ValueError("The input images must have the same size")

	out = Image.new("RGB", img1.size)

	pixels1 = img1.load()
	pixels2 = img2.load()

	pixels_out = out.load()

	for x in range(img1.width):
		for y in range(img2.height):
			r1, g1, b1 = pixels1[x, y]
			r2, g2, b2 = pixels2[x, y]

			r_out = min(r1+r2, 255) if "R" in channels else 0
			g_out = min(g1+g2, 255) if "G" in channels else 0
			b_out = min(b1+b2, 255) if "B" in channels else 0

			pixels_out[x, y] = (r_out, g_out, b_out)

	img1.close()
	img2.close()
	return out


@timecheck
def avgImage(img1_name, img2, channels="RGB"):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	img1, img2 = rescale_image(img1, img2)

	if img1.size != img2.size:
		raise ValueError("The input images must have the same size")

	out = Image.new("RGB", img1.size)

	pixels1 = img1.load()
	pixels2 = img2.load()

	pixels_out = out.load()

	for x in range(img1.width):
		for y in range(img1.height):
			r1, g1, b1 = pixels1[x, y]
			r2, g2, b2 = pixels2[x, y]

			r_out = (r1+r2)//2 if "R" in channels else 0
			g_out = (g1+g2)//2 if "G" in channels else 0
			b_out = (b1+b2)//2 if "B" in channels else 0

			pixels_out[x, y] = (r_out, g_out, b_out)

	img1.close()
	img2.close()
	return out


@timecheck
def maxImage(img1_name, img2, channels="RGB"):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	img1, img2 = rescale_image(img1, img2)

	if img1.size != img2.size:
		raise ValueError("The input images must have the same size")

	out = Image.new("RGB", img1.size)

	pixels1 = img1.load()
	pixels2 = img2.load()

	pixels_out = out.load()

	for x in range(img1.width):
		for y in range(img1.height):
			r1, g1, b1 = pixels1[x, y]
			r2, g2, b2 = pixels2[x, y]

			r_out = max(r1, r2) if "R" in channels else 0
			g_out = max(g1, g2) if "G" in channels else 0
			b_out = max(b1, b2) if "B" in channels else 0

			pixels_out[x, y] = (r_out, g_out, b_out)

	img1.close()
	img2.close()
	return out


@timecheck
def minImage(img1_name, img2, channels="RGB"):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	img1, img2 = rescale_image(img1, img2)

	if img1.size != img2.size:
		raise ValueError("The input images must have the same size")

	out = Image.new("RGB", img1.size)

	pixels1 = img1.load()
	pixels2 = img2.load()

	pixels_out = out.load()

	for x in range(img1.width):
		for y in range(img1.height):
			r1, g1, b1 = pixels1[x, y]
			r2, g2, b2 = pixels2[x, y]

			r_out = min(r1, r2) if "R" in channels else 0
			g_out = min(g1, g2) if "G" in channels else 0
			b_out = min(b1, b2) if "B" in channels else 0

			pixels_out[x, y] = (r_out, g_out, b_out)

	img1.close()
	img2.close()
	return out


@timecheck
def multImage(img1_name, img2, channels="RGB"):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	img1, img2 = rescale_image(img1, img2)

	if img1.size != img2.size:
		raise ValueError("The input images must have the same size")

	out = Image.new("RGB", img1.size)

	pixels1 = img1.load()
	pixels2 = img2.load()

	pixels_out = out.load()

	for x in range(img1.width):
		for y in range(img1.height):
			r1, g1, b1 = pixels1[x, y]
			r2, g2, b2 = pixels2[x, y]

			r_out = r1*r2//255 if "R" in channels else 0
			g_out = g1*g2//255 if "G" in channels else 0
			b_out = b1*b2//255 if "B" in channels else 0

			pixels_out[x, y] = (r_out, g_out, b_out)

	img1.close()
	img2.close()
	return out


@timecheck
def maskImage(img_name, mask_mode, channels="RGB"):
	if img_name is None:
		return None

	img = Image.open(img_name)
	w = max(img.width, img.height)

	if mask_mode == "C":
		make_circle_mask(w)
	elif mask_mode == "S":
		make_square_mask(w)

	out = Image.new("RGB", img.size)
	mask = Image.open("img/mask.jpg")

	img_pixels = img.load()
	mask_pixels = mask.load()
	pixels_out = out.load()

	for x in range(img.width):
		for y in range(img.height):
			r, g, b = img_pixels[x, y]
			rm, gm, bm = mask_pixels[x, y]

			r_out = r*rm//255 if "R" in channels else r
			g_out = g*gm//255 if "G" in channels else g
			b_out = b*bm//255 if "B" in channels else b

			pixels_out[x, y] = (r_out, g_out, b_out)

	img.close()
	mask.close()
	return out


@timecheck
def make_circle_mask(w):
	mask = Image.new("RGB", (w, w))

	pixels_out = mask.load()

	for x in range(mask.width):
		for y in range(mask.width):
			c = 255 - int(255 * sqrt((abs(x-w/2))**2 + (abs(y-w/2))**2) / (w/2))
			pixels_out[x, y] = (c, c, c)

	mask.save("img/mask.jpg")


@timecheck
def make_square_mask(w):
	mask = Image.new("RGB", (w, w))

	pixels_out = mask.load()

	for x in range(mask.width):
		for y in range(mask.width):
			c = 255 - int(255 * max(abs(x-w/2), abs(y-w/2)) / (w/2))
			pixels_out[x, y] = (c, c, c)

	mask.save("img/mask.jpg")


@timecheck
def rescale_image(img1, img2):
	if img1.size == img2.size:
		return img1, img2

	w = max(img1.width, img2.width)
	h = max(img1.height, img2.height)

	return img1.resize((w, h)), img2.resize((w, h))

