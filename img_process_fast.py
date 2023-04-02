from PIL import Image
from time import time
import numpy as np
from binar_process import *


def apply_filters(opt, img1_name=None, img2=None, channels="RGB", transparency=0.5):
	if opt == "None":
		return channelImageF(img1_name, channels)
	elif opt == "Square mask image":
		return maskImageF(img2, "S", channels, transparency)
	elif opt == "Circle mask image":
		return maskImageF(img2, "C", channels, transparency)
	elif opt == "Add":
		return sumImageF(img1_name, img2, channels)
	elif opt == "Multiply":
		return multImage(img1_name, img2, channels)
	elif opt == "Max":
		return maxImageF(img1_name, img2, channels)
	elif opt == "Min":
		return minImageF(img1_name, img2, channels)
	elif opt == "Average":
		return avgImageF(img1_name, img2, channels)
	else:
		return None


@timecheck
def channelImageF(img_name, channels):
	if img_name is None:
		return None

	img = Image.open(img_name)
	pixels = np.array(img)

	pixels_out = np.zeros_like(pixels)
	if 'R' in channels:
		pixels_out[:,:,0] = pixels[:,:,0]
	if 'G' in channels:
		pixels_out[:,:,1] = pixels[:,:,1]
	if 'B' in channels:
		pixels_out[:,:,2] = pixels[:,:,2]

	out = Image.fromarray(pixels_out, mode="RGB")
	img.close()
	return out


@timecheck
def sumImageF(img1_name, img2, channels="RGB"):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	img1, img2 = rescale_image(img1, img2)

	if img1.size != img2.size:
		raise ValueError("The input images must have the same size")

	pixels1 = np.array(img1)
	pixels2 = np.array(img2)

	pixels_out = np.zeros_like(pixels1)

	if 'R' in channels:
		pixels_out[:,:,0] = np.clip(pixels1[:,:,0]+pixels2[:,:,0], 0, 255)
	if 'G' in channels:
		pixels_out[:,:,1] = np.clip(pixels1[:,:,1]+pixels2[:,:,1], 0, 255)
	if 'B' in channels:
		pixels_out[:,:,2] = np.clip(pixels1[:,:,2]+pixels2[:,:,2], 0, 255)

	out = Image.fromarray(pixels_out, mode="RGB")
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


# Does't work properly
@timecheck
def multImageF(img1_name, img2, channels="RGB"):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	img1, img2 = rescale_image(img1, img2)

	if img1.size != img2.size:
		raise ValueError("The input images must have the same size")

	pixels1 = np.array(img1)
	pixels2 = np.array(img2)

	pixels_out = np.zeros_like(pixels1)

	if 'R' in channels:
		pixels_out[:,:,0] = pixels1[:,:,0]*pixels2[:,:,0]//255
	if 'G' in channels:
		pixels_out[:,:,1] = pixels1[:,:,1]*pixels2[:,:,1]//255
	if 'B' in channels:
		pixels_out[:,:,2] = pixels1[:,:,2]*pixels2[:,:,2]//255

	out = Image.fromarray((pixels_out), mode="RGB")
	img1.close()
	img2.close()
	return out


@timecheck
def maxImageF(img1_name, img2, channels="RGB"):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	img1, img2 = rescale_image(img1, img2)

	if img1.size != img2.size:
		raise ValueError("The input images must have the same size")

	pixels1 = np.array(img1)
	pixels2 = np.array(img2)

	pixels_out = np.zeros_like(pixels1)

	if 'R' in channels:
		pixels_out[:,:,0] = np.maximum(pixels1[:,:,0], pixels2[:,:,0])
	if 'G' in channels:
		pixels_out[:,:,1] = np.maximum(pixels1[:,:,1], pixels2[:,:,1])
	if 'B' in channels:
		pixels_out[:,:,2] = np.maximum(pixels1[:,:,2], pixels2[:,:,2])

	out = Image.fromarray(pixels_out, mode="RGB")
	img1.close()
	img2.close()
	return out


@timecheck
def minImageF(img1_name, img2, channels="RGB"):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	img1, img2 = rescale_image(img1, img2)

	if img1.size != img2.size:
		raise ValueError("The input images must have the same size")

	pixels1 = np.array(img1)
	pixels2 = np.array(img2)

	pixels_out = np.zeros_like(pixels1)

	if 'R' in channels:
		pixels_out[:,:,0] = np.minimum(pixels1[:,:,0], pixels2[:,:,0])
	if 'G' in channels:
		pixels_out[:,:,1] = np.minimum(pixels1[:,:,1], pixels2[:,:,1])
	if 'B' in channels:
		pixels_out[:,:,2] = np.minimum(pixels1[:,:,2], pixels2[:,:,2])

	out = Image.fromarray(pixels_out, mode="RGB")
	img1.close()
	img2.close()
	return out


@timecheck
def avgImageF(img1_name, img2, channels="RGB"):
	if img1_name is None:
		return None

	img1 = Image.open(img1_name)

	img1, img2 = rescale_image(img1, img2)

	if img1.size != img2.size:
		raise ValueError("The input images must have the same size")

	pixels1 = np.array(img1)
	pixels2 = np.array(img2)

	pixels_out = np.zeros_like(pixels1)

	if 'R' in channels:
		pixels_out[:,:,0] = (pixels1[:,:,0] + pixels2[:,:,0]) // 2
	if 'G' in channels:
		pixels_out[:,:,1] = (pixels1[:,:,1] + pixels2[:,:,1]) // 2
	if 'B' in channels:
		pixels_out[:,:,2] = (pixels1[:,:,2] + pixels2[:,:,2]) // 2

	out = Image.fromarray(pixels_out, mode="RGB")
	img1.close()
	img2.close()
	return out


@timecheck
def make_circle_mask(w, transparency=0):
	x, y = np.ogrid[:w, :w]
	distance = np.sqrt((x-w/2)**2 + (y-w/2)**2)
	mask = np.where(distance > w/2, 0, 255 - np.uint8(255 * distance / (w/2)))
	alpha = np.uint8(255 * transparency)
	mask = np.dstack((mask, mask, mask, alpha * np.ones_like(mask)))
	mask = Image.fromarray(mask, mode="RGBA")
	mask.save("img/mask.png")


@timecheck
def make_square_mask(w, transparency=0):
	x, y = np.ogrid[:w, :w]
	distance = np.maximum(np.abs(x - w/2), np.abs(y - w/2))
	mask = np.where(distance > w/2, 0, 255 - np.uint8(255 * distance / (w/2)))
	alpha = np.uint8(255 * transparency)
	mask = np.dstack((mask, mask, mask, alpha * np.ones_like(mask)))
	mask = Image.fromarray(mask, mode="RGBA")
	mask.save("img/mask.png")


@timecheck
def maskImageF(img, mask_mode, channels="RGB", mask_transparency=0.5):
	if img is None:
		return None

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
	if img1.size != img2.size:
		w, h = max(img1.width, img2.width), max(img1.height, img2.height)
		img1 = img1.resize((w, h))
		img2 = img2.resize((w, h))
	return img1, img2


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

