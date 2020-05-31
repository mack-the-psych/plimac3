#Original code was retrieved from https://github.com/nico/collectiveintelligence-book

import ac_treepredict_by_variance as treepredict
#import Image, ImageDraw
#import ImageFont
import sys

from PIL import Image, ImageDraw, ImageFont

if sys.platform == "darwin":
  FONT_PATH = '/Library/Fonts/Verdana.ttf'
  FONT_PATH_JP = '/Library/Fonts/Osaka.ttf'

# added by mack.sano@gmail.com 03/14/2020
elif sys.platform == "linux":
  FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
  FONT_PATH_JP = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
  
elif sys.platform == "linux2":
  FONT_PATH = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
  FONT_PATH_JP = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'

else:
  FONT_PATH = 'C:\Windows\Fonts\\REFSAN.TTF'
  FONT_PATH_JP = 'C:\Windows\Fonts\msgothic.ttc'

FONT_SIZE = 36
FONT_SIZE_JP = 24
HSCALING = 4
VSCALING = 3
LEFT_TEXT_MARGIN = 50

def getwidth(tree):
  if tree.tb == None and tree.fb == None: return 1  # leaf
  return getwidth(tree.tb) + getwidth(tree.fb)


# XXX: why does `tree` have a value in this function?
#def getdepth(clust):
  #print tree
  #return 0

def getdepth(tree):
  if tree.tb == None and tree.fb == None: return 0  # leaf
  return max(getdepth(tree.tb), getdepth(tree.fb)) + 1


def drawtree(tree, png='tree.png', difficulty_min=0.00, difficulty_max=1.00, 
        deviance_dic=None, h_scale = HSCALING, v_scale = VSCALING, lang = 'En'):
  w = getwidth(tree)*100*h_scale
  h = getdepth(tree)*100*v_scale + 120*v_scale

  if lang == 'Jp':
    f_path = FONT_PATH_JP
    f_size = FONT_SIZE_JP
  else:
    f_path = FONT_PATH
    f_size = FONT_SIZE

  font = ImageFont.truetype(f_path, f_size)
  
  img = Image.new('RGB', (w, h), (255, 255, 255))
  draw = ImageDraw.Draw(img)

  diffculty_scale = float(w / (difficulty_max - difficulty_min))

  avrgall, numall = treepredict.getavrg_num(tree)
  xall = (avrgall - difficulty_min) * diffculty_scale

  drawnode(draw, tree, xall, 20*v_scale, difficulty_min, diffculty_scale, h_scale, v_scale, lang)

  draw.line((50*h_scale, h - 50*v_scale, w - 50*h_scale, h - 50*v_scale), fill=(0, 0, 0))
  draw.line((50*h_scale, h - 50*v_scale, 60*h_scale, h - 40*v_scale), fill=(0, 0, 0))
  draw.line((w - 50*h_scale, h - 50*v_scale, w - 60*h_scale, h - 40*v_scale), fill=(0, 0, 0))
  draw.text((w/2, h - 40*v_scale), 'Difficulty Measure', (0, 0, 0), font=font)

  if deviance_dic != None:
    for key, val in sorted(deviance_dic.items()):
      if key >= 0:
        txt = 'R^2=%1.4f' % (1- val/tree.root_deviance)
        draw.text((10*h_scale, 10*v_scale + key*100*v_scale), txt, (0, 0, 0), font=font)

  # Support TIF 300 dpi mack.sano@gmail.com
  if '.tif' in png:
    img.save(png, 'TIFF', dpi=(300, 300))
  else:
    img.save(png, 'PNG')

def drawnode(draw, tree, x, y, difficulty_min, diffculty_scale, h_scale, v_scale, lang = 'En'):
  if lang == 'Jp':
    f_path = FONT_PATH_JP
    f_size = FONT_SIZE_JP
  else:
    f_path = FONT_PATH
    f_size = FONT_SIZE
  
  font = ImageFont.truetype(f_path, f_size)

  if tree.results == None:  # internal node
    # Get width of each branch
    #w1 = getwidth(tree.fb) * 100*h_scale
    #w2 = getwidth(tree.tb) * 100*h_scale

    #left = x - (w1 + w2)/2
    #right = x + (w1 + w2)/2

    # Get width (x-axis) makoto.sano@prometric.com
    avrgf, numf = treepredict.getavrg_num(tree.fb)
    avrgt, numt = treepredict.getavrg_num(tree.tb)
    xf = (avrgf - difficulty_min) * diffculty_scale
    xt = (avrgt -difficulty_min) * diffculty_scale

    # Draw condition
    colname = ''
    if tree.value_name != None:
      colname = tree.value_name
    else:
      colname = str(tree.col)

    draw.text((x - LEFT_TEXT_MARGIN*h_scale, y - 10*v_scale), '%s:%s' % (colname, tree.value), (0, 0, 0), font=font)

    # Draw links to branches
    draw.line((x - 10*h_scale, y, xf, y+100*v_scale), fill=(255, 0, 0))
    draw.line((x + 10*h_scale, y, xt, y+100*v_scale), fill=(255, 0, 0))
    
    drawnode(draw, tree.fb, xf, y + 100*v_scale, difficulty_min, diffculty_scale, h_scale, v_scale, lang)
    drawnode(draw, tree.tb, xt, y + 100*v_scale, difficulty_min, diffculty_scale, h_scale, v_scale, lang)
  else:
    #txt = ' '.join(['%s:%d' % v for v in tree.results.items()])
    txt = '%1.2f:%d' % (treepredict.getavrg_num(tree))
    draw.text((x - 20*h_scale, y), txt, (0, 0, 0), font=font)


if __name__ == '__main__':
  import treepredict
  tree = treepredict.buildtree(treepredict.testdata())
  drawtree(tree, 'tree.png')
  print('Wrote tree.png')
