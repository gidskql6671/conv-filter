#ifndef LAYER_H
#define LAYER_H

#include <vector>
#include <tuple>
#include <algorithm>
#include "filter.hpp"
#include "opencv2/opencv.hpp"

using namespace cv;
using namespace std;

class conv_layer
{
	int in_width, in_height, in_depth,
		n_filters, window, stride,
		out_width, out_height, out_depth;

public:
	conv_layer(int _height,
			   int _width,
			   int _depth,
			   int _window,
			   int _stride = 1,
			   int n_filters = 1)
		: in_height(_height),
		  in_width(_width),
		  in_depth(_depth),
		  window(_window),
		  stride(_stride),
		  n_filters(n_filters)
	{
		// 패딩은 input 이미지에 미리 적용해두었다. 즉, 여기서 신경쓸 필요 없음
		out_width = (in_width - window) / stride + 1;
		out_height = (in_height - window) / stride + 1;
		out_depth = n_filters;
	}

	~conv_layer() {}


	tuple<int, int, Mat> conv2d(Mat image, const vector<filter *> &filters, int start_row = 0, int start_col = 0){
		Mat output(out_height, out_width, image.type());

		for (int k = 0; k < n_filters; ++k){ 
			for (int i = 0; i < out_height; ++i){
				uchar *output_row = output.ptr<uchar>(i);
				
				for (int j = 0; j < out_width; ++j){
					int i_start = i * stride,
						j_start = j * stride;
					int i_end = i_start + window,
						j_end = j_start + window;

					for (int i_pt = i_start; i_pt < i_end; i_pt++){
						uchar *img_row = image.ptr<uchar>(i_pt);
						for (int j_pt = j_start; j_pt < j_end; j_pt++){
							for (int k_pt = 0; k_pt < in_depth; k_pt++){
								output_row[j * 3 + k] += img_row[j_pt * 3 + k_pt] * filters[k]->w[i_pt - i_start][j_pt - j_start][k_pt];
							}
						}
					}
					
					output_row[j * 3 + k] += filters[k]->b;
				}
			}
		}
		return make_tuple(start_row, start_col, output);
	}
};

#endif