<<<<<<< HEAD
<<<<<<< HEAD
#!/usr/bin/python

from PIL import Image
import pylab
import sys
import numpy as np

if __name__ == "__main__":
    f = open(sys.argv[1] ,"r")
    shape = list(map(int, f.readline().split()))
    for idx in range(shape[0]):
        im = np.empty(shape=(shape[1], shape[2], shape[3]))
        for i in range(shape[1]):
            row = f.readline().split()
            assert(len(row) == shape[2])  # 512
            for j in range(shape[2]):
                im[i][j] = list(map(float, row[j].split(",")))
        result = Image.fromarray(im.astype(np.uint8))
        result.save(sys.argv[2] + "/" + str(idx) + ".bmp")
        f.readline()    # empty line
=======
#!/usr/bin/python

from PIL import Image
import pylab
import sys
import numpy as np
import os

if __name__ == "__main__":
    inputFoldername = sys.argv[1]
    outputFoldername = sys.argv[2]
    num_cores = int(sys.argv[3])
    
    
    for index in range(num_cores):
        filepath = os.path.join(inputFoldername, "out_apply_filter" + str(index) + ".dat")
        f = open(filepath, "r")
        
        # outputFoldername/batch0 과 같은 디렉토리를 만든다.
        outputBatchFolder = os.path.join(outputFoldername, "batch" + str(index))
        os.makedirs(outputBatchFolder, exist_ok=True)
        
        shape = list(map(int, f.readline().split()))
        for idx in range(shape[0]):
            im = np.empty(shape=(shape[1], shape[2], shape[3]))
            for i in range(shape[1]):
                row = f.readline().split()
                assert(len(row) == shape[2])  # 512
                for j in range(shape[2]):
                    im[i][j] = list(map(float, row[j].split(",")))
            result = Image.fromarray(im.astype(np.uint8))
            # outputFoldername/batch0/result0.bmp 와 같은 결과 파일을 만듬.
            result.save(os.path.join(outputBatchFolder, "result" + str(idx) + ".bmp"))
            f.readline()    # empty line
>>>>>>> d59733b (병렬처리에 적합하게 수정)
=======
#!/usr/bin/python

from PIL import Image
import pylab
import sys
import numpy as np
import os


# matrix 파일을 이미지 파일로 Convert
# 밑에 메인구문 보면 일단은 그냥 순차실행 시켰는데, 스레드로 병렬처리만 시켜도 엄청 빨라져용
def _matrix2Image(inputFilepath, outputDirpath):
    f = open(inputFilepath, "r")
    os.makedirs(outputDirpath, exist_ok=True)
    
    
    shape = list(map(int, f.readline().split()))
    for idx in range(shape[0]):
        # outputDirpath/result0.bmp 와 같은 결과파일명.
        outputFilename = os.path.join(outputDirpath, "result" + str(idx) + ".bmp")
        
        im = np.empty(shape=(shape[1], shape[2], shape[3]))
        for i in range(shape[1]):
            row = f.readline().split()
            assert(len(row) == shape[2]) # 512인지 확인
            for j in range(shape[2]):
                im[i][j] = list(map(float, row[j].split(",")))
        result = Image.fromarray(im.astype(np.uint8))
        
        result.save(outputFilename)
        f.readline()    # empty line
        

if __name__ == "__main__":
    inputFoldername = sys.argv[1]
    outputFoldername = sys.argv[2]
    num_cores = int(sys.argv[3])
    
    os.makedirs(outputFoldername, exist_ok=True)
    
    for index in range(num_cores):
        # input 파일들의 형태는 out_apply_filter0.dat, out_apply_filter1.dat, ... 과 같은 형태로 되어있다.
        # 사용한 코어마다 별개의 input을 받고, 별개의 output을 내도록 함. 한개로 하면 관리하기 힘듬...
        inputFilepath = os.path.join(inputFoldername, "out_apply_filter" + str(index) + ".dat")
        # {outputFoldername}/batch0 과 같은 디렉토리를 만든다.
        outputBatchFolder = os.path.join(outputFoldername, "batch" + str(index))
        
        
        # 구현을 각 코어마다 다른 폴더에 이미지 파일들을 반환하도록 해놨음.
        # 구현 조금만 수정해서 한 폴더에 쭉 내보내는 것도 가능... 하고싶으신대로...
        _matrix2Image(inputFilepath, outputBatchFolder)
>>>>>>> 80aec61 (리팩토링 : 부분 함수화)
