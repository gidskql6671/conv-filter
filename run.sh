#!/bin/bash

# clean the current build
make clean
make

# make image matrices and store them 
python3 src/make_mats.py img_mats/out.dat

# run the filter program
build/main img_mats/out.dat img_mats/out_apply_filter.dat < configs/filter.txt

# run python program to generate images from matrix
# output written as 0.bmp, 1.bmp ...
python3 src/load_img.py img_mats/out_apply_filter.dat out_mats
