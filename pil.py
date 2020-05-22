from PIL import Image, ImageFilter
from PIL.ImageFilter import (UnsharpMask)
from PIL.ExifTags import TAGS
import numpy as np
import os

res = 2048
power = 0.5
quality = 100
ext = '.jpg'

def start() :
  for file in os.listdir('src') :
    name, file_ext = os.path.splitext(file)
    img = Image.open(os.path.join('./src', file))
    img=img.rotate(0)
    exif=img.info['exif']
    img = img.convert('RGB')
    #img = img.filter(ImageFilter.SHARPEN)
    #img = img.filter(UnsharpMask(radius=2, percent=150, threshold=3))
    img = img.convert('HSV')
    print(name+file_ext, img.size)
    H, S, V = img.split()
    V = stretch_contrast(V)
    img = Image.merge('HSV', (H, S, V))

    img = img.convert('RGB')
    R, G, B = img.split()
    R = stretch_contrast(R)
    G = stretch_contrast(G)
    B = stretch_contrast(B)
    img = Image.merge('RGB', (R, G, B))


    if img.height > res and img.width > res :
        img = resize(img)
        print('resized to', res, quality, '%')
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