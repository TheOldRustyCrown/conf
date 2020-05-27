from PIL import Image, ImageFilter, ImageChops, ExifTags
import numpy as np
import os

res = 512
gamma = 1.25
power = 0.1
quality = 100
ext = '.jpg'


def start() :
  for file in os.listdir('source') :
    name, file_ext = os.path.splitext(file)
    img = Image.open(os.path.join('./source', file))
    img = img.convert('RGB')
    console(img, name)

    img = gamma_correction(img)
    img = hsv_contrast(img)
    img = white_balance(img)

    #emboss = img.filter(ImageFilter.EMBOSS)
    #img = ImageChops.overlay(img, emboss)

    img = resize(img)
    save(img, name)
  return


def gamma_correction (img) :
  img = img.convert('HSV')
  H, S, V = img.split()
  V = np.array(V).astype(float)
  V = 255.0 * (V / 255.0)**(1 / gamma)
  V = Image.fromarray(np.uint8(V))
  img = Image.merge('HSV', (H, S, V))
  img = img.convert('RGB')
  return img

def white_balance(img) :
  save_info = img.info
  R, G, B = img.split()
  R = stretch_contrast(R)
  G = stretch_contrast(G)
  B = stretch_contrast(B)
  img = Image.merge('RGB', (R, G, B))
  img.info = save_info
  return img

def hsv_contrast(img) :
  img = img.convert('HSV')
  H, S, V = img.split()
  V = stretch_contrast(V)
  img = Image.merge('HSV', (H, S, V))
  img = img.convert('RGB')
  return img

def stretch_contrast (chanel) :
  white = np.percentile(chanel, 100-power)
  black = np.percentile(chanel, power)
  print('min :', black, '/', 'max :', white)
  Lt = 255 / (white - black)
  Dk = 255 * black / (black - white)
  print('Light :', round(Lt, 1), '/', 'Dark :', round(Dk, 1))
  matrix = np.asarray(np.maximum(0, np.minimum(255 , chanel * Lt + Dk))).astype(float)
  return Image.fromarray(np.uint8(matrix))

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
    img.save('./fx/{}_fx'.format(name) + ext, exif=exif, quality=quality)
  else :
    img.save('./fx/{}_fx_noexif'.format(name) + ext, quality=quality)

start()