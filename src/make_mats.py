<<<<<<< HEAD
#!/usr/bin/python

import numpy as np
from PIL import Image
import pylab
import sys
import os

dirname = 'images/'
#im_names = ["airplane.png", "lena.png",  "fruits.png"]  # 512 * 512 * 3
#gray_imnames = ["barbara.png", "boat.png"] # 512 * 512

def append_matrix(filepath, outf):
    img = Image.open(filepath)
    im = np.asarray(img, dtype='float64')
    #print(im.shape)
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
        outf.write('\n')
    outf.write('\n')

if __name__ == "__main__":
    f = open(sys.argv[1], "w")
    depth = 3   # 3 for color, 1 for grey
    foldername = dirname + 'color/' # grey for grey 
    filenames = os.listdir(foldername)
    f.write("%d 512 512 %d\n" % (len(filenames), depth)) # image tensor dimensions
    for filename in filenames:
        append_matrix(foldername + filename, f)

=======
#!/usr/bin/python

from pathlib import WindowsPath
import numpy as np
from PIL import Image
import pylab
import sys
import os
from enum import Enum


# 컬러 이미지인지 흑백 이미지인지
class ImgType(Enum):
    GREY = 1
    COLOR = 3

# 이미지와 관련된 정보들을 담아둔 클래스
class ImgInfo:
    def __init__(self, imgType: ImgType, width = 512, height = 512) -> None:
        self.imgType = ImgType
        if imgType == ImgType.GREY:
            self.dirname = os.path.join('images', 'grey')
        elif imgType == ImgType.COLOR:
            self.dirname = os.path.join('images', 'color')
        self.depth = imgType.value
        
        self.width = width
        self.height = height
        

# 컬러 사진을 사용할지, 흑백 사진을 사용할지 선택
imgInfo = ImgInfo(ImgType.COLOR)
#im_names = ["airplane.png", "lena.png",  "fruits.png"]  # 512 * 512 * 3
#gray_imnames = ["barbara.png", "boat.png"] # 512 * 512


# 이미지를 불러와서 matrix 형태로 파일에 저장한다.
def append_matrix(filepath, outf):
    img = Image.open(filepath)
    im = np.asarray(img, dtype='float64')
    #print(im.shape)
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
        outf.write('\n')
    outf.write('\n')

if __name__ == "__main__":
    f = open(sys.argv[1], "w")
    
    depth = imgInfo.depth 
    foldername = imgInfo.dirname
    width = imgInfo.width
    height = imgInfo.height
      
    filenames = os.listdir(foldername)
    f.write("%d %d %d %d\n" % (len(filenames), width, height, depth)) # image tensor dimensions
    for filename in filenames:
        append_matrix(foldername + filename, f)

>>>>>>> 497f3dc (유지보수하기 쉽도록 정보들을 모아 클래스로 만듬.)
