#!/bin/bash

# 사용하는 코어의 개수
# 여기서는 명령행인자로 개수를 넣었는데, 그냥 프로그램 내에서 사용가능한 코어개수만큼 사용하는 것도 좋을것 같아요.
# 그렇게 할려다가 왠지 다 쓰면 안좋을거같아서... 
num_cores=5

# clean the current build
make clean
make

# make image matrices and store them 
# Usage: python3 make_mats.py outs_dir/ num_cores
python3 src/make_mats.py img_mats/outs_img2mat/ $num_cores

# run the filter program
c_executions/main img_mats/outs_img2mat/ img_mats/outs_apply_filter/ $num_cores < configs/filter.txt

# run python program to generate images from matrix
# output written as batch0/0.bmp, batch0/1.bmp, ..., batch2/0.bmp, batch2/1.bmp ...
python3 src/load_img.py img_mats/outs_apply_filter/ result_images/ $num_cores
