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
