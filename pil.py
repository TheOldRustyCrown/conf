from PIL import Image, ImageFilter, ImageChops, ImageOps, ExifTags
import numpy as np
import os

res = 6000
gamma = 1.0
contrast = 0.1
quality = 99
ext = '.jpg'

def start() :
  for file in os.listdir('input') :
    name, file_ext = os.path.splitext(file)
    img = Image.open(os.path.join('./input', file)).convert('RGB')
    console(img, name)

    img = img.convert('HSV')
    H, S, V = img.split()
    V = ImageOps.autocontrast(V, cutoff=contrast)
    img = Image.merge('HSV', (H, S, V)).convert('RGB')

    img = ImageOps.autocontrast(img, cutoff=contrast)
    img = gamma_correction(img)

    img = resize(img)
    save(img, name)

  return

def gamma_correction (img) :
  img = img.convert('HSV')
  H, S, V = img.split()
  V = np.array(V).astype(float)
  V = 255.0 * (V / 255.0)**(1 / gamma)
  V = Image.fromarray(np.uint8(V))
  img = Image.merge('HSV', (H, S, V)).convert('RGB')
  return img

def console(img, name) :
  if img.height > res and img.width > res :
    print(name, str(img.size[0]) + 'x' + str(img.size[1]), 'Resided to :', str(res) + 'p', '/', 'quality :', str(quality) + '%')
  else :
    print(name, str(img.size[0]) + 'x' + str(img.size[1]), str(quality) + '%')

def resize(img) :
  if img.height > res and img.width > res :
    width = int(round(res / img.height * img.width, 0))
    img = img.resize((width, res), Image.LANCZOS, None)
  return img

def save(img, name) :
  if 'exif' in img.info :
    exif=img.info['exif']
    img.save('./output/{}_fx'.format(name) + ext, exif=exif, quality=quality, subsampling=0)
  else :
    img.save('./output/{}_fx_noexif'.format(name) + ext, quality=quality, subsampling=0)

start()

    #emboss = img.filter(ImageFilter.EMBOSS)
    #img = ImageChops.overlay(img, emboss)
    #img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=2))
    #median = img.filter(ImageFilter.MedianFilter(size=3))