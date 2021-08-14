#!/bin/bash

# 사용하는 코어의 개수
if [ $# -eq 1 ]; then
    v=$1
    r=${v//[0-9]/}
    if [ -z "$r" ]; then
        num_cores=$1
    else
        num_cores=5
    fi
else
    num_cores=5
fi

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
