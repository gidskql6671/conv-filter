#include <iostream>
#include <ctime>
#include "opencv2/opencv.hpp"
#include "src/filter.hpp"
#include "src/conv2d_layer.hpp"

using namespace std;
using namespace cv;

int w_size, bias;     // kernel window size
double** kernel; // image kernel 
vector<filter*> filters;

void push_filter(int idx) {     
	// make edge detector for color idx 
	double ***ed = get_tensor(w_size, w_size, 3); 
	for (int i = 0; i < w_size; ++i) {
		for (int j = 0; j < w_size; ++j) {
			ed[i][j][idx] = kernel[i][j];
		}
	}
	
	filter *f = new filter(ed, w_size, 3, bias);
	f->normalize();
	filters.push_back(f);
}


int main(){
	//  input the kernel matrix
	cin >> w_size >> bias;
	kernel = new double*[w_size]; 
	for (int i = 0; i < w_size; i++) {
		kernel[i] = new double[w_size];
		for (int j = 0; j < w_size; j++) {
			cin >> kernel[i][j]; 
		}
	}
	push_filter(0); // B
	push_filter(1); // G
	push_filter(2); // R
	
	clock_t t1 = clock();
	
	Mat img = imread("../images/color/largeimage.jpg");
	
	clock_t t2 = clock();
	cout << img.rows << " " << img.cols <<  " " << img.channels() << endl;
	
	
	conv_layer clayer(img.rows, img.cols, img.channels(), w_size, 1, 1, filters.size()); 
	Mat output = clayer.conv2d(img, filters);
	
	clock_t t3 = clock();
	
	imwrite("test.png", output);
	
	double time_loadImage = (double)(t2 - t1) / CLOCKS_PER_SEC;
	double time_applyFilter = (double)(t3 - t2) / CLOCKS_PER_SEC;
	double time_saveImage = (double)(clock() - t3) / CLOCKS_PER_SEC;
	
	cout << "load image time : " << time_loadImage << " sec\n";
	cout << "apply filter time : " << time_applyFilter << " sec\n";
	cout << "save image time : " << time_saveImage << " sec\n";
	
	return 0;
}