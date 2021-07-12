#!/bin/bash

# clean the current build
make clean
make

# make image matrices and store them 
# Usage: python3 make_mats.py outs_dir/ [num_cores(default : 1)]
python3 src/make_mats.py img_mats/outs_img2mat/

# run the filter program
c_executions/main img_mats/outs_img2mat/ img_mats/outs_apply_filter/ < configs/filter.txt

# run python program to generate images from matrix
# output written as 0.bmp, 1.bmp ...
python3 src/load_img.py img_mats/outs_apply_filter/ result_images/
