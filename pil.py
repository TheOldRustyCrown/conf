from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import os

res = 2048
power = 1
quality = 100
ext = '.jpeg'

def start() :
  for file in os.listdir('src') :
    name, file_ext = os.path.splitext(file)
    img = Image.open(os.path.join('./src', file))
    exif=img.info['exif']
    img = img.convert('RGB')
    img = img.convert('HSV')
    print(name+file_ext, img.size)
    H, S, V = img.split()
    Norm = stretch_contrast(V)
    img = Image.merge('HSV', (H, S, Norm))
    img = img.convert('RGB')
    if img.height > res and img.width > res :
        img = resize(img)
    img.save('./fx/{}'.format(name) + ext, exif=exif, quality=quality)

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