from PIL import Image
import numpy as np
import os

res = 2048
power = 0.1618
quality = 72
ext = '.jpeg'

def start() :
	for file in os.listdir('source') :
		name, file_ext = os.path.splitext(file)
		img = Image.open(os.path.join('./source', file)).convert('RGB')
		print(name+file_ext, img.size)
		R, G, B = img.split()
		NormR = stretch_contrast(R)
		NormG = stretch_contrast(G)
		NormB = stretch_contrast(B)
		img = Image.merge('RGB', (NormR, NormG, NormB))
		if img.height > res and img.width > res :
			img = resize(img)
		img.save('../../enhanced/FX_{}'.format(name) + ext, quality=quality)
		del B, G, R, NormB, NormG, NormR, img, name, file_ext, file

def stretch_contrast (chanel) :
	white = np.percentile(chanel, 100-power)
	black = np.percentile(chanel, power)
	Lt = 255 / (white - black)
	Dk = 255 * black / (black - white)
	matrix = np.asarray(np.maximum(0, np.minimum(255 , chanel * Lt + Dk)).astype(np.uint8), np.uint8)
	return Image.fromarray(matrix)

def resize(img) :
	height = res
	width = int((height / img.height * img.width) + 0.3)
	return img.resize((width, height), Image.LANCZOS, None)

start()