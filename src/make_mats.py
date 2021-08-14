<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
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
        append_matrix(os.path.join(foldername, filename), f)

>>>>>>> fc1f714 (버그 수정)
=======
#!/usr/bin/python

from pathlib import WindowsPath
import numpy as np
from PIL import Image
from numpy.lib.shape_base import take_along_axis
import pylab
import sys
import os
from enum import Enum
import time
import multiprocessing

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
        

#im_names = ["airplane.png", "lena.png",  "fruits.png"]  # 512 * 512 * 3
#gray_imnames = ["barbara.png", "boat.png"] # 512 * 512

class Img2Matrix:
    def __init__(self, imgInfo: ImgInfo, num_cores, outFolderName):
        self.imgInfo = imgInfo
        self.num_cores = num_cores
        self.outFolderName = outFolderName
    
    # 해당 이미지를 불러와서 matrix 형태로 파일에 저장한다.
    def append_matrix(self, filepath, outf):
        img = Image.open(filepath)
        im = np.asarray(img, dtype='float64')
        #print(im.shape)
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
            outf.write('\n')
        outf.write('\n')
        
        # 테스트용 추후 삭제 요망
        outf.seek(0)

    def convertFiles2Matrix(self, filenames, outf):
        for filename in filenames:
            self.append_matrix(filename, outf)

    # 주어진 파일들을 matrix 형태로 Convert해준다.
    def convertFiles2MatrixByMultiprocess(self):
        depth = self.imgInfo.depth 
        foldername = self.imgInfo.dirname
        width = self.imgInfo.width
        height = self.imgInfo.height
        
        totalFilenames = os.listdir(foldername)
        totalFilenames = [os.path.join(foldername, filename) for filename in totalFilenames]
        totalFilenames = totalFilenames * 10
        # 테스트해볼 충분한 사진이 없기때문에 기존에 존재하는 파일로 반복을 할 것임
        
        splitedFileNames = np.array_split(totalFilenames, self.num_cores)
        splitedFileNames = [x.tolist() for x in splitedFileNames]
        
        print(f"Core 개수 : {self.num_cores}")
        start = int(time.time())
        
        procs = []
        outfs = []
        for index, filenames in enumerate(splitedFileNames):
            outFilename = os.path.join(self.outFolderName, "out" + str(index) + ".dat")
            outf = open(outFilename, "w")
            outf.write("%d %d %d %d\n" % (len(filenames), width, height, depth)) # image tensor dimensions
            
            proc = multiprocessing.Process(target=self.convertFiles2Matrix,
                                            args=(filenames, outf))
            procs.append(proc)
            outfs.append(outf)
            proc.start()
        
        for proc in procs:
            proc.join()
        for outf in outfs:
            outf.close()
        
        print("run time(sec) :", int(time.time()) - start)
        
        

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: python3 {sys.argv[0]} outFolderName [num_cores]")
        exit()
    outFolderName = sys.argv[1]
    
    num_cores = 1
    if len(sys.argv) == 3:
        if sys.argv[2].isdigit():
            num_cores = int(sys.argv[2])
        else:
            print(f"Usage: python3 {sys.argv[0]} outFolderName [num_cores]")
            exit()

    # 컬러 사진을 사용할지, 흑백 사진을 사용할지 선택
    imgInfo = ImgInfo(ImgType.COLOR)
    
    Img2Matrix(imgInfo, num_cores, outFolderName).convertFiles2MatrixByMultiprocess()

>>>>>>> 500efa4 (병렬 처리 적용)
=======
#!/usr/bin/python

from pathlib import WindowsPath
import numpy as np
from PIL import Image
from numpy.lib.shape_base import take_along_axis
import pylab
import sys
import os
from enum import Enum
import time
import multiprocessing


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
        

class Img2Matrix:
    def __init__(self, imgInfo: ImgInfo, num_cores, outFolderName):
        self.imgInfo = imgInfo
        self.num_cores = num_cores
        self.outFolderName = outFolderName
    
    # 해당 이미지를 matrix 형태로 파일에 저장한다.
    def _append_matrix(self, filepath, outf):
        img = Image.open(filepath)
        im = np.asarray(img, dtype='float64')
        #print(im.shape)
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
            outf.write('\n')
        outf.write('\n')


    # 주어진 이미지 파일들을 Matrix 형태로 Convert한다.
    def _convertImages2Matrixs(self, filepaths, outf):
        for filepath in filepaths:
            self._append_matrix(filepath, outf)


    # 주어진 파일들을 matrix 형태로 Convert해준다.
    def convertImages2MatrixsByMultiprocess(self):
        foldername = self.imgInfo.dirname
        # foldername 속 존재하는 파일들의 경로
        filepaths = [os.path.join(foldername, filename) for filename in os.listdir(foldername)]
        
        # 테스트해볼 충분한 사진이 없기때문에 기존에 존재하는 파일로 반복을 함
        filepaths = filepaths * 1
        
        # 병렬 처리를 위해 여러개의 리스트로 나눔. ex) {1, 2, 3, 4, 5, 6} -> {{1, 2}, {3, 4}, {5, 6}}
        splitedFilepaths = np.array_split(filepaths, self.num_cores)
        splitedFilepaths = [x.tolist() for x in splitedFilepaths]
        
        procs = []
        outfs = []
        for index, filepaths in enumerate(splitedFilepaths):
            # 프로세스 별로 다른 Output 파일을 가짐.
            outFilename = os.path.join(self.outFolderName, "img2mat" + str(index) + ".dat")
            outf = open(outFilename, "w")
            outf.write(f"{len(filepaths)} {self.imgInfo.width} {self.imgInfo.height} {self.imgInfo.depth}\n") # image tensor dimensions
            
            proc = multiprocessing.Process(target=self._convertImages2Matrixs,
                                            args=(filepaths, outf))
            procs.append(proc)
            outfs.append(outf)
            
            proc.start()
        
        for proc in procs:
            proc.join()
        for outf in outfs:
            outf.close()
        

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: python3 {sys.argv[0]} outFolderName [num_cores]")
        exit()
    outFolderName = sys.argv[1]
    
    num_cores = 1
    if len(sys.argv) == 3:
        if sys.argv[2].isdigit():
            num_cores = int(sys.argv[2])
        else:
            print(f"Usage: python3 {sys.argv[0]} outFolderName [num_cores]")
            exit()

    # 컬러 사진을 사용할지, 흑백 사진을 사용할지 선택
    imgInfo = ImgInfo(ImgType.COLOR)
    
    # 테스트 용. 추후 삭제하자
    print(f"Core 개수 : {num_cores}")
    start = int(time.time())
    
    Img2Matrix(imgInfo, num_cores, outFolderName).convertImages2MatrixsByMultiprocess()
    
    print("run time(sec) :", int(time.time()) - start)

>>>>>>> 161929f (코드 리팩토링)
=======
#!/usr/bin/python

from pathlib import WindowsPath
import numpy as np
from PIL import Image
from numpy.lib.shape_base import take_along_axis
import pylab
import sys
import os
from enum import Enum
import time
import multiprocessing


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
        

class Img2Matrix:
    def __init__(self, imgInfo: ImgInfo, num_cores, outFolderName):
        self.imgInfo = imgInfo
        self.num_cores = num_cores
        self.outFolderName = outFolderName
    
    # 해당 이미지를 matrix 형태로 파일에 저장한다.
    def _append_matrix(self, filepath, outf):
        img = Image.open(filepath)
        im = np.asarray(img, dtype='float64')
        #print(im.shape)
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
            outf.write('\n')
        outf.write('\n')


    # 주어진 이미지 파일들을 Matrix 형태로 Convert한다.
    def _convertImages2Matrixs(self, filepaths, outf):
        for filepath in filepaths:
            self._append_matrix(filepath, outf)


    # 주어진 파일들을 matrix 형태로 Convert해준다.
    def convertImages2MatrixsByMultiprocess(self):
        foldername = self.imgInfo.dirname
        # foldername 속 존재하는 파일들의 경로
        filepaths = [os.path.join(foldername, filename) for filename in os.listdir(foldername)]
        
        # 테스트해볼 충분한 사진이 없기때문에 기존에 존재하는 파일로 반복을 함
        filepaths = filepaths * 7
        
        # 병렬 처리를 위해 여러개의 리스트로 나눔. ex) {1, 2, 3, 4, 5, 6} -> {{1, 2}, {3, 4}, {5, 6}}
        splitedFilepaths = np.array_split(filepaths, self.num_cores)
        splitedFilepaths = [x.tolist() for x in splitedFilepaths]
        
        procs = []
        outfs = []
        for index, filepaths in enumerate(splitedFilepaths):
            # 프로세스 별로 다른 Output 파일을 가짐.
            outFilename = os.path.join(self.outFolderName, "img2mat" + str(index) + ".dat")
            outf = open(outFilename, "w")
            outf.write(f"{len(filepaths)} {self.imgInfo.width} {self.imgInfo.height} {self.imgInfo.depth}\n") # image tensor dimensions
            
            proc = multiprocessing.Process(target=self._convertImages2Matrixs,
                                            args=(filepaths, outf))
            procs.append(proc)
            outfs.append(outf)
            
            proc.start()
        
        for proc in procs:
            proc.join()
        for outf in outfs:
            outf.close()
        

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: python3 {sys.argv[0]} outFolderName [num_cores]")
        exit()
    outFolderName = sys.argv[1]
    
    num_cores = 1
    if len(sys.argv) == 3:
        if sys.argv[2].isdigit():
            num_cores = int(sys.argv[2])
        else:
            print(f"Usage: python3 {sys.argv[0]} outFolderName [num_cores]")
            exit()

    # 컬러 사진을 사용할지, 흑백 사진을 사용할지 선택
    imgInfo = ImgInfo(ImgType.COLOR)
    
    # 테스트 용. 추후 삭제하자
    print(f"Core 개수 : {num_cores}")
    start = int(time.time())
    
    Img2Matrix(imgInfo, num_cores, outFolderName).convertImages2MatrixsByMultiprocess()
    
    print("run time(sec) :", int(time.time()) - start)

>>>>>>> 03b7eda (병렬 처리 테스트를 위한 값수정)
=======
#!/usr/bin/python

from pathlib import WindowsPath
import numpy as np
from PIL import Image
from numpy.lib.shape_base import take_along_axis
import pylab
import sys
import os
from enum import Enum
import time
import multiprocessing


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
        

class Img2Matrix:
    def __init__(self, imgInfo: ImgInfo, num_cores, outFolderName):
        self.imgInfo = imgInfo
        self.num_cores = num_cores
        self.outFolderName = outFolderName
    
    # 해당 이미지를 matrix 형태로 파일에 저장한다.
    def _append_matrix(self, filepath, outf):
        img = Image.open(filepath)
        im = np.asarray(img, dtype='float64')
        #print(im.shape)
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
            outf.write('\n')
        outf.write('\n')


    # 주어진 이미지 파일들을 Matrix 형태로 Convert한다.
    def _convertImages2Matrixs(self, filepaths, outf):
        for filepath in filepaths:
            self._append_matrix(filepath, outf)


    # 주어진 파일들을 matrix 형태로 Convert해준다.
    def convertImages2MatrixsByMultiprocess(self):
        foldername = self.imgInfo.dirname
        # foldername 속 존재하는 파일들의 경로
        filepaths = [os.path.join(foldername, filename) for filename in os.listdir(foldername)]
        
        # 테스트해볼 충분한 사진이 없기때문에 기존에 존재하는 파일로 반복을 함
        filepaths = filepaths * 7
        
        # 병렬 처리를 위해 여러개의 리스트로 나눔. ex) {1, 2, 3, 4, 5, 6} -> {{1, 2}, {3, 4}, {5, 6}}
        splitedFilepaths = np.array_split(filepaths, self.num_cores)
        splitedFilepaths = [x.tolist() for x in splitedFilepaths]
        
        procs = []
        outfs = []
        for index, filepaths in enumerate(splitedFilepaths):
            # 프로세스 별로 다른 Output 파일을 가짐.
            outFilename = os.path.join(self.outFolderName, "img2mat" + str(index) + ".dat")
            outf = open(outFilename, "w")
            outf.write(f"{len(filepaths)} {self.imgInfo.width} {self.imgInfo.height} {self.imgInfo.depth}\n") # image tensor dimensions
            
            proc = multiprocessing.Process(target=self._convertImages2Matrixs,
                                            args=(filepaths, outf))
            procs.append(proc)
            outfs.append(outf)
            
            proc.start()
        
        for proc in procs:
            proc.join()
        for outf in outfs:
            outf.close()
        

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} outFolderName num_cores")
        exit()
    outFolderName = sys.argv[1]
    
    if sys.argv[2].isdigit():
        num_cores = int(sys.argv[2])
    else:
        print(f"Usage: num_cores는 정수여야 합니다.")
        exit()

    # 컬러 사진을 사용할지, 흑백 사진을 사용할지 선택
    imgInfo = ImgInfo(ImgType.COLOR)
    
    # 테스트 용. 추후 삭제하자
    print(f"Core 개수 : {num_cores}")
    start = int(time.time())
    
    Img2Matrix(imgInfo, num_cores, outFolderName).convertImages2MatrixsByMultiprocess()
    
    print("run time(sec) :", int(time.time()) - start)

>>>>>>> 4f80da8 (매개변수로 코어의 개수를 항상 받도록 함)
=======
#!/usr/bin/python

from pathlib import WindowsPath
import numpy as np
from PIL import Image
from numpy.lib.shape_base import take_along_axis
import pylab
import sys
import os
from enum import Enum
import time
import multiprocessing


# 컬러 이미지인지 흑백 이미지인지
class ImgType(Enum):
    GREY = 1
    COLOR = 3

# 이미지와 관련된 정보들을 담아둔 클래스
class ImgInfo:
    def __init__(self, imgType: ImgType, width = 512, height = 512) -> None:
        self.imgType = ImgType
        self.depth = imgType.value
        
        self.width = width
        self.height = height
  


# 이미지를 matrix 형태로 파일에 저장한다.
def _append_matrix(filepath, outf):
    img = Image.open(filepath)
    im = np.asarray(img, dtype='float64')
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
        outf.write('\n')
    outf.write('\n')
     
# 주어진 이미지 파일들을 Matrix 형태로 Convert한다.
def _convertImages2Matrixs(filepaths, outf):
    for filepath in filepaths:
        _append_matrix(filepath, outf)

# 멀티 프로세스를 사용하여 파일들을 matrix 형태로 Convert해준다.
def convertImage2MatrixByMultiprocess(inputDirname, outputDirname, num_cores = 1, imgInfo= ImgInfo(ImgType.COLOR)):
    # inputDirname 디렉토리의 파일들의 전체 경로를 얻어준다.
    filepaths = [os.path.join(inputDirname, filename) for filename in os.listdir(inputDirname)]
    
    # 단순 테스트를 위해 같은 사진을 반복적으로 처리하도록 함.
    # 같은 파일에 대해 여러 스레드가 접근하니, 완벽한 테스팅이 아님. 추후 사진 구해서 테스트 해봐야함.
    filepaths = filepaths * 7
    
    # 병렬 처리를 위해 여러개의 리스트로 나눔. ex) [1, 2, 3, 4, 5, 6] -> [[1, 2], [3, 4], [5, 6]]
    splitedFilepaths = np.array_split(filepaths, num_cores)
    splitedFilepaths = [x.tolist() for x in splitedFilepaths]
    
    procs = []
    outfs = []
    for index, filepaths in enumerate(splitedFilepaths):
        # 프로세스 별로 다른 Output 파일을 반환.
        outFilename = os.path.join(outputDirname, "img2mat" + str(index) + ".dat")
        outf = open(outFilename, "w")
        outf.write(f"{len(filepaths)} {imgInfo.width} {imgInfo.height} {imgInfo.depth}\n") # image tensor dimensions
        
        # 프로세스 별로 image convert
        proc = multiprocessing.Process(target=_convertImages2Matrixs, args=(filepaths, outf))
        
        procs.append(proc)
        outfs.append(outf)
        
        proc.start()
    
    for proc in procs:
        proc.join()
    for outf in outfs:
        outf.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} outputDirname num_cores")
        exit()
    outputDirname = sys.argv[1]
    os.makedirs(outputDirname, exist_ok=True)
    
    if sys.argv[2].isdigit():
        num_cores = int(sys.argv[2])
    else:
        print(f"Usage: num_cores는 정수여야 합니다.")
        exit()

    # 컬러사진을 사용할 것이며, 512x512사이즈(기본값)을 사용할 것임.
    imgInfo = ImgInfo(ImgType.COLOR)
    inputDirname = os.path.join('images', 'color');
            
    # 테스트 용. 시간 측정
    print(f"Core 개수 : {num_cores}")
    start = int(time.time())
    
    convertImage2MatrixByMultiprocess(inputDirname, outputDirname, num_cores, imgInfo);
    
    print("run time(sec) :", int(time.time()) - start)

>>>>>>> 7164927 (리팩토링 : 불필요한 클래스 제거)
=======
#!/usr/bin/python

from pathlib import WindowsPath
import numpy as np
from PIL import Image
from numpy.lib.shape_base import take_along_axis
import pylab
import sys
import os
from enum import Enum
import time
import multiprocessing


# 컬러 이미지인지 흑백 이미지인지
class ImgType(Enum):
    GREY = 1
    COLOR = 3

# 이미지와 관련된 정보들을 담아둔 클래스
class ImgInfo:
    def __init__(self, imgType: ImgType, width = 512, height = 512) -> None:
        self.imgType = ImgType
        self.depth = imgType.value
        
        self.width = width
        self.height = height
  


# 이미지를 matrix 형태로 파일에 저장한다.
def _append_matrix(filepath, outf):
    img = Image.open(filepath)
    im = np.asarray(img, dtype='float64')
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
        outf.write('\n')
    outf.write('\n')
     
# 주어진 이미지 파일들을 Matrix 형태로 Convert한다.
def _convertImages2Matrixs(filepaths, outf):
    for filepath in filepaths:
        _append_matrix(filepath, outf)

# 멀티 프로세스를 사용하여 파일들을 matrix 형태로 Convert해준다.
def convertImage2MatrixByMultiprocess(inputDirname, outputDirname, num_cores = 1, imgInfo= ImgInfo(ImgType.COLOR)):
    # inputDirname 디렉토리의 파일들의 전체 경로를 얻어준다.
    filepaths = [os.path.join(inputDirname, filename) for filename in os.listdir(inputDirname)]
    
    # 단순 테스트를 위해 같은 사진을 반복적으로 처리하도록 함.
    # 같은 파일에 대해 여러 스레드가 접근하니, 완벽한 테스팅이 아님. 추후 사진 구해서 테스트 해봐야함.
    filepaths = filepaths * 7
    
    # 병렬 처리를 위해 여러개의 리스트로 나눔. ex) [1, 2, 3, 4, 5, 6] -> [[1, 2], [3, 4], [5, 6]]
    splitedFilepaths = np.array_split(filepaths, num_cores)
    splitedFilepaths = [x.tolist() for x in splitedFilepaths]
    
    procs = []
    outfs = []
    for index, filepaths in enumerate(splitedFilepaths):
        # 프로세스 별로 다른 Output 파일을 반환.
        outFilename = os.path.join(outputDirname, "img2mat" + str(index) + ".dat")
        outf = open(outFilename, "w")
        outf.write(f"{len(filepaths)} {imgInfo.width} {imgInfo.height} {imgInfo.depth}\n") # image tensor dimensions
        
        # 프로세스 별로 image convert
        proc = multiprocessing.Process(target=_convertImages2Matrixs, args=(filepaths, outf))
        
        procs.append(proc)
        outfs.append(outf)
        
        proc.start()
    
    for proc in procs:
        proc.join()
    for outf in outfs:
        outf.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} outputDirname num_cores")
        exit()
    outputDirname = sys.argv[1]
    os.makedirs(outputDirname, exist_ok=True)
    
    if sys.argv[2].isdigit():
        num_cores = int(sys.argv[2])
    else:
        print(f"Usage: num_cores는 정수여야 합니다.")
        exit()

    # 컬러사진을 사용할 것이며, 512x512사이즈(기본값)을 사용할 것임.
    imgInfo = ImgInfo(ImgType.COLOR)
    inputDirname = os.path.join('images', 'color');
            
    # 테스트 용. 시간 측정
    print(f"Core 개수 : {num_cores}")
    start = time.time()
    
    convertImage2MatrixByMultiprocess(inputDirname, outputDirname, num_cores, imgInfo);
    
    print("run time(sec) :", round(time.time() - start, 3))

>>>>>>> 5504688 (시간 테스트 코드 수정)
=======
#!/usr/bin/python

from pathlib import WindowsPath
import numpy as np
from PIL import Image
from numpy.lib.shape_base import take_along_axis
import pylab
import sys
import os
from enum import Enum
import time
import multiprocessing
import threading


# 컬러 이미지인지 흑백 이미지인지
class ImgType(Enum):
    GREY = 1
    COLOR = 3

# 이미지와 관련된 정보들을 담아둔 클래스
class ImgInfo:
    def __init__(self, imgType: ImgType, width = 512, height = 512) -> None:
        self.imgType = ImgType
        self.depth = imgType.value
        
        self.width = width
        self.height = height
  


# 이미지를 matrix 형태로 파일에 저장한다.
def _append_matrix(filepath, outf):
    img = Image.open(filepath)
    im = np.asarray(img, dtype='float64')
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
        outf.write('\n')
    outf.write('\n')
     
# 주어진 이미지 파일들을 Matrix 형태로 Convert한다.
def _convertImages2Matrixs(filepaths, outf):
    for filepath in filepaths:
        _append_matrix(filepath, outf)

# 멀티 프로세스를 사용하여 파일들을 matrix 형태로 Convert해준다.
def convertImage2MatrixByMultiprocess(inputDirname, outputDirname, num_cores = 1, imgInfo= ImgInfo(ImgType.COLOR)):
    # inputDirname 디렉토리의 파일들의 전체 경로를 얻어준다.
    filepaths = [os.path.join(inputDirname, filename) for filename in os.listdir(inputDirname)]
    
    # 병렬 처리를 위해 여러개의 리스트로 나눔. ex) [1, 2, 3, 4, 5, 6] -> [[1, 2], [3, 4], [5, 6]]
    splitedFilepaths = np.array_split(filepaths, num_cores)
    splitedFilepaths = [x.tolist() for x in splitedFilepaths]
    
    procs = []
    outfs = []
    for index, filepaths in enumerate(splitedFilepaths):
        # 프로세스 별로 다른 Output 파일을 반환.
        outFilename = os.path.join(outputDirname, "img2mat" + str(index) + ".dat")
        outf = open(outFilename, "w")
        outf.write(f"{len(filepaths)} {imgInfo.width} {imgInfo.height} {imgInfo.depth}\n") # image tensor dimensions
        
        # 프로세스 별로 image convert
        proc = multiprocessing.Process(target=_convertImages2Matrixs, args=(filepaths, outf))
        
        procs.append(proc)
        outfs.append(outf)
        
        proc.start()
    
    for proc in procs:
        proc.join()
    for outf in outfs:
        outf.close()

# 스레드를 사용한 병렬처리. 파이썬 특성상 스레드 사용 부분을 나눠야 할 것 같다.
# https://yeonfamily.tistory.com/3
def convertImage2MatrixByThread(inputDirname, outputDirname, num_cores = 1, imgInfo= ImgInfo(ImgType.COLOR)):
    # inputDirname 디렉토리의 파일들의 전체 경로를 얻어준다.
    filepaths = [os.path.join(inputDirname, filename) for filename in os.listdir(inputDirname)]
    
    # 병렬 처리를 위해 여러개의 리스트로 나눔. ex) [1, 2, 3, 4, 5, 6] -> [[1, 2], [3, 4], [5, 6]]
    splitedFilepaths = np.array_split(filepaths, num_cores)
    splitedFilepaths = [x.tolist() for x in splitedFilepaths]

    threads = []
    outfs = []
    for index, filepaths in enumerate(splitedFilepaths):
        # 스레드 별로 다른 Output 파일을 반환.
        outFilename = os.path.join(outputDirname, "img2mat" + str(index) + ".dat")
        outf = open(outFilename, "w")
        outf.write(f"{len(filepaths)} {imgInfo.width} {imgInfo.height} {imgInfo.depth}\n") # image tensor dimensions
        
        # 프로세스 별로 image convert
        th = threading.Thread(target=_convertImages2Matrixs, args=(filepaths, outf))
        
        threads.append(th)
        outfs.append(outf)
        
        th.start()
    
    for th in threads:
        th.join()
    for outf in outfs:
        outf.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} outputDirname num_cores")
        exit()
    outputDirname = sys.argv[1]
    os.makedirs(outputDirname, exist_ok=True)
    
    if sys.argv[2].isdigit():
        num_cores = int(sys.argv[2])
    else:
        print(f"Usage: num_cores는 정수여야 합니다.")
        exit()

    # 컬러사진을 사용할 것이며, 512x512사이즈(기본값)을 사용할 것임.
    imgInfo = ImgInfo(ImgType.COLOR)
    inputDirname = os.path.join('images', 'color');
            
    # 테스트 용. 시간 측정
    print(f"Core 개수 : {num_cores}")
    start = time.time()
    
    convertImage2MatrixByMultiprocess(inputDirname, outputDirname, num_cores, imgInfo);
    # convertImage2MatrixByThread(inputDirname, outputDirname, num_cores, imgInfo)
    
    print("run time(sec) :", round(time.time() - start, 3))

>>>>>>> 23f9253 (스레드를 사용하는 병렬처리 추가)
=======
#!/usr/bin/python

from pathlib import WindowsPath
import numpy as np
from PIL import Image
from numpy.lib.shape_base import take_along_axis
import pylab
import sys
import os
from enum import Enum
import time
import multiprocessing
import threading


# 컬러 이미지인지 흑백 이미지인지
class ImgType(Enum):
    GREY = 1
    COLOR = 3

# 이미지와 관련된 정보들을 담아둔 클래스
class ImgInfo:
    def __init__(self, imgType: ImgType, width = 512, height = 512) -> None:
        self.imgType = ImgType
        self.depth = imgType.value
        
        self.width = width
        self.height = height
  


# 이미지를 matrix 형태로 파일에 저장한다.
def _append_matrix(filepath, outf):
    img = Image.open(filepath)
    im = np.asarray(img, dtype='float64')
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
        outf.write('\n')
    outf.write('\n')
     
# 주어진 이미지 파일들을 Matrix 형태로 Convert한다.
def _convertImages2Matrixs(filepaths, outFilename, imgInfo):
    outf = open(outFilename, "w")
    outf.write(f"{len(filepaths)} {imgInfo.width} {imgInfo.height} {imgInfo.depth}\n") # image tensor dimensions
    
    for filepath in filepaths:
        _append_matrix(filepath, outf)
    
    outf.close()

# 멀티 프로세스를 사용하여 파일들을 matrix 형태로 Convert해준다.
def convertImage2MatrixByMultiprocess(inputDirname, outputDirname, num_cores = 1, imgInfo= ImgInfo(ImgType.COLOR)):
    # inputDirname 디렉토리의 파일들의 전체 경로를 얻어준다.
    filepaths = [os.path.join(inputDirname, filename) for filename in os.listdir(inputDirname)]
    
    # 병렬 처리를 위해 여러개의 리스트로 나눔. ex) [1, 2, 3, 4, 5, 6] -> [[1, 2], [3, 4], [5, 6]]
    splitedFilepaths = np.array_split(filepaths, num_cores)
    splitedFilepaths = [x.tolist() for x in splitedFilepaths]
    
    procs = []
    for index, filepaths in enumerate(splitedFilepaths):
        # 프로세스 별로 다른 Output 파일을 반환.
        outFilename = os.path.join(outputDirname, "img2mat" + str(index) + ".dat")
        
        # 프로세스 별로 image convert
        proc = multiprocessing.Process(target=_convertImages2Matrixs, args=(filepaths, outFilename, imgInfo))
        proc.start()
        
        procs.append(proc)
    
    for proc in procs:
        proc.join()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} outputDirname num_cores")
        exit()
    outputDirname = sys.argv[1]
    os.makedirs(outputDirname, exist_ok=True)
    
    if sys.argv[2].isdigit():
        num_cores = int(sys.argv[2])
    else:
        print(f"Usage: num_cores는 정수여야 합니다.")
        exit()

    # 컬러사진을 사용할 것이며, 512x512사이즈(기본값)을 사용할 것임.
    imgInfo = ImgInfo(ImgType.COLOR)
    inputDirname = os.path.join('images', 'color');
            
    # 테스트 용. 시간 측정
    print(f"Core 개수 : {num_cores}")
    start = time.time()
    
    convertImage2MatrixByMultiprocess(inputDirname, outputDirname, num_cores, imgInfo);
    # convertImage2MatrixByThread(inputDirname, outputDirname, num_cores, imgInfo)
    
    print("run time(sec) :", round(time.time() - start, 3))

>>>>>>> 3d4ae38 (리팩토링)
=======
#!/usr/bin/python

from pathlib import WindowsPath
import numpy as np
from PIL import Image
from numpy.lib.shape_base import take_along_axis
import pylab
import sys
import os
from enum import Enum
import time
import multiprocessing
import threading


# 컬러 이미지인지 흑백 이미지인지
class ImgType(Enum):
    GREY = 1
    COLOR = 3

# 이미지와 관련된 정보들을 담아둔 클래스
class ImgInfo:
    def __init__(self, imgType: ImgType, width = 512, height = 512) -> None:
        self.imgType = ImgType
        self.depth = imgType.value
        
        self.width = width
        self.height = height
  


# 이미지를 matrix 형태로 파일에 저장한다.
def _append_matrix(filepath, outf):
    img = Image.open(filepath)
    im = np.asarray(img, dtype='float64')
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            outf.write("%f,%f,%f " %(im[i][j][0], im[i][j][1], im[i][j][2]))
        outf.write('\n')
    outf.write('\n')
     
# 주어진 이미지 파일들을 Matrix 형태로 Convert한다.
def _convertImages2Matrixs(filepaths, outFilename, imgInfo):
    outf = open(outFilename, "w")
    outf.write(f"{len(filepaths)} {imgInfo.width} {imgInfo.height} {imgInfo.depth}\n") # image tensor dimensions
    
    for filepath in filepaths:
        _append_matrix(filepath, outf)
    
    outf.close()

# 멀티 프로세스를 사용하여 파일들을 matrix 형태로 Convert해준다.
def convertImage2MatrixByMultiprocess(inputDirname, outputDirname, num_cores = 1, imgInfo= ImgInfo(ImgType.COLOR)):
    # inputDirname 디렉토리의 파일들의 전체 경로를 얻어준다.
    filepaths = [os.path.join(inputDirname, filename) for filename in os.listdir(inputDirname)]
    
    # 병렬 처리를 위해 여러개의 리스트로 나눔. ex) [1, 2, 3, 4, 5, 6] -> [[1, 2], [3, 4], [5, 6]]
    splitedFilepaths = np.array_split(filepaths, num_cores)
    splitedFilepaths = [x.tolist() for x in splitedFilepaths]
    
    procs = []
    for index, filepaths in enumerate(splitedFilepaths):
        # 프로세스 별로 다른 Output 파일을 반환.
        outFilename = os.path.join(outputDirname, "img2mat" + str(index) + ".dat")
        
        # 프로세스 별로 image convert
        proc = multiprocessing.Process(target=_convertImages2Matrixs, args=(filepaths, outFilename, imgInfo))
        proc.start()
        
        procs.append(proc)
    
    for proc in procs:
        proc.join()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} outputDirname num_cores")
        exit()
    outputDirname = sys.argv[1]
    os.makedirs(outputDirname, exist_ok=True)
    
    if sys.argv[2].isdigit():
        num_cores = int(sys.argv[2])
    else:
        print(f"Usage: num_cores는 정수여야 합니다.")
        exit()

    # 컬러사진을 사용할 것이며, 512x512사이즈(기본값)을 사용할 것임.
    imgInfo = ImgInfo(ImgType.COLOR)
    inputDirname = os.path.join('images', 'color');
            
    # 테스트 용. 시간 측정
    print(f"Core 개수 : {num_cores}")
    start = time.time()
    
    convertImage2MatrixByMultiprocess(inputDirname, outputDirname, num_cores, imgInfo);
    
    print("run time(sec) :", round(time.time() - start, 3))

>>>>>>> df4941d (리팩토링 : 불필요한 주석 제거)
