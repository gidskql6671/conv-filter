cmake . -G "MinGW Makefiles"

make

./main.exe ./images/color ./result_images < ./configs/filter.txt