from PIL import Image
from time import time
from math import sqrt
import numpy as np


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
def make_circle_mask(w, transparency=0):
	mask = Image.new("RGBA", (w, w), (255, 255, 255, 255))

	pixels_out = mask.load()

	for x in range(mask.width):
		for y in range(mask.width):
			distance = sqrt((abs(x-w/2))**2 + (abs(y-w/2))**2)
			if distance > w/2:
				c = 0
			else:
				c = 255 - int(255 * distance / (w/2))
			pixels_out[x, y] = (c, c, c, int(255 * transparency))

	mask.save("img/mask.png")


@timecheck
def make_square_mask(w, transparency=0):
	mask = Image.new("RGBA", (w, w), (255, 255, 255, 255))

	pixels_out = mask.load()

	for x in range(mask.width):
		for y in range(mask.width):
			distance = max(abs(x-w/2), abs(y-w/2))
			if distance > w/2:
				c = 0
			else:
				c = 255 - int(255 * distance / (w/2))
			pixels_out[x, y] = (c, c, c, int(255 * transparency))

	mask.save("img/mask.png")


@timecheck
def maskImage(img_name, mask_mode, channels="RGB", mask_transparency=0.5):
    if img_name is None:
        return None

    img = Image.open(img_name)
    w = max(img.width, img.height)

    if mask_mode == "C":
        make_circle_mask(w, transparency=mask_transparency)
    elif mask_mode == "S":
        make_square_mask(w, transparency=mask_transparency)

    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    mask = Image.open("img/mask.png")

    mask_x = int((img.width - mask.width) / 2)
    mask_y = int((img.height - mask.height) / 2)

    out.paste(img, (0, 0))
    out.paste(mask, (mask_x, mask_y), mask)

    out = out.convert("RGB")

    img.close()
    mask.close()
    return out


@timecheck
def rescale_image(img1, img2):
	if img1.size == img2.size:
		return img1, img2

	w = max(img1.width, img2.width)
	h = max(img1.height, img2.height)

	return img1.resize((w, h)), img2.resize((w, h))

# @timecheck
# def grad_transform(img_name: str, points: dict[float, float]):
# 	if img_name is None:
# 		return None

# 	img = Image.open(img_name)
# 	pixels = img.load()

# 	out = Image.new("RGB", img.size)
# 	pixels_out = out.load()

# 	new_brightness = {}
# 	for x in range(256):
# 		new_brightness[x] = bezier_curve(x, points)

# 	for x in range(img.width):
# 		for y in range(img.height):
# 			r, g, b = pixels[x, y]
# 			brightness = (r+g+b)//3

# 			nb = new_brightness[brightness]
# 			r_out = min(int(r*nb/brightness), 255) if brightness else 0
# 			g_out = min(int(g*nb/brightness), 255) if brightness else 0
# 			b_out = min(int(b*nb/brightness), 255) if brightness else 0

# 			pixels_out[x, y] = (r_out, g_out, b_out)

# 	img.close()
# 	return out

# works 10! times faster
@timecheck
def grad_transform(img_name: str, points: dict[float, float]):
	if img_name is None:
		return None
	
	img = Image.open(img_name)
	pixels = np.array(img)
	
	unique_brightness = np.unique(pixels.sum(axis=2)//3)
	new_brightness = np.vectorize(bezier_curve)(unique_brightness, points)
	
	pixels_out = np.empty_like(pixels)
	pixels_out[:,:,0] = np.interp(pixels[:,:,0], unique_brightness, new_brightness)
	pixels_out[:,:,1] = np.interp(pixels[:,:,1], unique_brightness, new_brightness)
	pixels_out[:,:,2] = np.interp(pixels[:,:,2], unique_brightness, new_brightness)
	
	out = Image.fromarray(pixels_out, mode="RGB")
	
	img.close()
	return out


def bezier_curve(x: float, points: dict[float, float]) -> float:
	keys = sorted(points.keys())
	if len(keys) == 2:
		dx = keys[1]-keys[0]
		dy = points[keys[1]] - points[keys[0]]
		# уравнение прямой между двумя точками
		return dy * (x-keys[0]) / dx + points[keys[0]]
	else:
		for i in range(len(keys) - 1):
			if keys[i] <= x <= keys[i+1]:
				t = (x - keys[i]) / (keys[i+1] - keys[i])
				P0 = points[keys[i]]
				P1 = points[keys[i]] + (points[keys[i+1]] - points[keys[i]]) // 3
				P2 = points[keys[i]] + 2 * (points[keys[i+1]] - points[keys[i]]) // 3
				P3 = points[keys[i+1]]
				return (1-t)**3 * P0 + 3*(1-t)**2 * t * P1 + 3*(1-t) * t**2 * P2 + t**3 * P3
		# если x не попадает ни в один из отрезков, возвращаем None или вызываем исключение
		return None
