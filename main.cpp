#include <iostream>
#include <ctime>
#include <filesystem>
#include <vector>
#include <tuple>
#include "opencv2/opencv.hpp"

#include "src/filter.hpp"
#include "src/conv2d_layer.hpp"
#include "src/thread_pool.hpp"

using namespace std;
using namespace cv;
namespace fs = filesystem;

int w_size, bias;     // kernel window size
double** kernel; // image kernel 
vector<filter*> filters;

const int thread_count = thread::hardware_concurrency();
ThreadPool::ThreadPool pool(thread_count); // 스레드 풀 생성


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

// image에 필터를 적용하여 파일에 저장한다.
// 이미지의 크기가 크면, 멀티 스레드(스레드풀)를 사용하여 병렬처리한다.
void applyFilterAndSaveWithMultiThread(Mat image, string outPath){
	int sep_row = 512, sep_col = 512;
	
	int pading = 1;
	int stride = 1;
	
	Mat pad_image;
	// 이미지에 패딩 추가
	copyMakeBorder(image, pad_image, pading, pading, pading, pading, BORDER_CONSTANT, Scalar(0));
	
	int out_height = (pad_image.rows - w_size) / stride + 1;
	int out_width = (pad_image.cols - w_size) / stride + 1;
	
	// 나눌 크기는 계속 테스트해보자
	// 결과 이미지 크기가 (sep_row, sep_col) 이하라면 바로 필터 적용
	if (out_height <= sep_row && out_width <= sep_col){
		conv_layer clayer(pad_image.rows, pad_image.cols, image.channels(), w_size, stride, filters.size()); 
		Mat output = get<2>(clayer.conv2d(pad_image, filters));
	
		imwrite(outPath, output);
	}
	// 그 이상이라면 분할해서 처리
	else{
		// (start_row, start_col, split_image)
		vector<tuple<int, int, Mat>> split_images;
		
		
		// 나뉜 크기와 윈도우 사이즈를 고려해서 잘라냄
		for(int i = 0; i < pad_image.rows; i += sep_row){
			for(int j = 0; j < pad_image.cols; j += sep_col){
				split_images.emplace_back(i, j, 
					pad_image(Range(i, min(pad_image.rows, i + sep_row + w_size - 1))
							, Range(j, min(pad_image.cols, j + sep_col + w_size - 1)))
				);
			}
		}
		
		// 나눈 이미지를 병렬적으로 처리하고, 결과를 future 배열에 담음
		vector<future<tuple<int, int, Mat>>> futures;
		for(auto img_info: split_images){
			int start_row, start_col;
			Mat split_img;
			tie(start_row, start_col, split_img) = img_info;
			conv_layer clayer(split_img.rows, split_img.cols, image.channels(), w_size, stride, filters.size()); 
			
			futures.emplace_back(pool.enqueueJob(conv_layer::conv2d, clayer, split_img, filters, start_row, start_col));
		} 
		
		// 필터를 적용한 이미지들을 다시 합침
		Mat output(Size(out_width, out_height), image.type(), Scalar::all(0));
		for(auto& f: futures){
			tuple<int, int, Mat> result = f.get();
			int start_row, start_col;
			Mat split_img;
			tie(start_row, start_col, split_img) = result;
			
			split_img.copyTo(output(Rect(start_col, start_row, split_img.cols, split_img.rows)));
		}
	
		imwrite(outPath, output);
	}
}

// image에 필터를 적용하여 반환해준다.
// 싱글 스레드로 실행된다.
Mat applyFilterWithSingleThread(Mat image){
	Mat pad_image;
	
	int pading = 1;
	int stride = 1;

	// 이미지에 패딩 추가
	copyMakeBorder(image, pad_image, pading, pading, pading, pading, BORDER_CONSTANT, Scalar(0));
	
	int out_height = (pad_image.rows - w_size) / stride + 1;
	int out_width = (pad_image.cols - w_size) / stride + 1;
	
	conv_layer clayer(pad_image.rows, pad_image.cols, image.channels(), w_size, stride, filters.size()); 
	Mat output = get<2>(clayer.conv2d(pad_image, filters));
	
	return output;
}

int main(int argc, char *argv[]){
	// 명령행 인자 유효성 검사 및 사전 준비
	if (argc < 3){
		cout << "[USAGE] " << argv[0] << " <image_folder> <output_folder>\n";
		pool.end();
		return 0;
	}
	
	fs::path imageFolder(argv[1]);
	fs::path outputFolder(argv[2]);
	if (!fs::exists(imageFolder)){
		cout << "이미지 폴더가 없습니다" << endl;
		pool.end();
		return 0;
	}
	if (!fs::is_directory(imageFolder)){
		cout << "폴더가 아닙니다" << endl;
		pool.end();
		return 0;
	}
	if (!fs::exists(outputFolder)){
		fs::create_directories(outputFolder);
	}
	
	
	// 필터 입력 부분
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
	
	
	cout << "thread count : " << thread_count << endl;
	clock_t t1 = clock();
	
	// 스레드가 한개면 파일이 클 경우, 내가 구현한 방식으로는 작동 안한다.
	// 이런 경우에는 그냥 스레드 하나에서 쭉 동작시키자.
	if (thread_count == 1){
		for (const fs::directory_entry& entry : fs::directory_iterator(imageFolder)){
			// 이미지 읽기
			Mat image = imread(entry.path().u8string());
			string outPath = (outputFolder / entry.path().filename()).u8string();
			
			Mat output = applyFilterWithSingleThread(image);
			
			imwrite(outPath, output);
		}
		
		cout << "total time : " << (double)(clock() - t1) / CLOCKS_PER_SEC << " sec\n";
		
		pool.end();
		
		return 0;
	}
	
	// 이미지를 읽고, 스레드에게 job으로 던져줌
	for (const fs::directory_entry& entry : fs::directory_iterator(imageFolder)){
		Mat image = imread(entry.path().u8string());
		
		pool.enqueueJob(applyFilterAndSaveWithMultiThread, image, (outputFolder / entry.path().filename()).u8string());
	}
	
	clock_t t2 = clock();
	
	pool.end();
	
	clock_t t3 = clock();
	
	double load_image_time = (double)(t2 - t1) / CLOCKS_PER_SEC;
	double apply_filter_time = (double)(t3 - t2) / CLOCKS_PER_SEC;
	double total_time = (double)(t3 - t1) / CLOCKS_PER_SEC;
	
	cout << "load image time : " << load_image_time << " sec\n";
	cout << "apply filter time : " << apply_filter_time << " sec\n";
	cout << "total time : " << total_time << " sec\n";
	
	return 0;
}