#ifndef LAYER_H
#define LAYER_H

#include <vector>
#include <cassert>
#include <tuple>
#include <algorithm>
#include "filter.hpp"
#include "opencv2/opencv.hpp"

using namespace cv;

class conv_layer
{
	int in_width, in_height, in_depth,
		n_filters, window, stride, padding,
		out_width, out_height, out_depth;

public:
	conv_layer(int _height,
			   int _width,
			   int _depth,
			   int _window,
			   int _stride = 1,
			   int _padding = 0,
			   int n_filters = 1)
		: in_height(_height),
		  in_width(_width),
		  in_depth(_depth),
		  window(_window),
		  stride(_stride),
		  padding(_padding),
		  n_filters(n_filters)
	{
		// in_width + 2*padding - window should be divisible by stride
		out_width = (in_width + 2 * padding - window) / stride + 1;
		out_height = (in_height + 2 * padding - window) / stride + 1;
		out_depth = n_filters;
	}

	~conv_layer() {}


	Mat conv2d(Mat image, const std::vector<filter *> &filters){
		Mat output(out_height, out_width, image.type());

		for (int k = 0; k < n_filters; ++k){ // k_th activation map
			for (int i = 0; i < out_height; ++i){
				uchar *output_row = output.ptr<uchar>(i);
				
				for (int j = 0; j < out_width; ++j){
					// fill y[i][j] with kernel computation filters[k]->x + b
					// compute boundaries inside original matrix after padding

					int i_start = -padding + i * stride,
						j_start = -padding + j * stride;
					int i_end = i_start + window,
						j_end = j_start + window;

					for (int i_pt = std::max(0, i_start); i_pt < std::min(in_height, i_end); ++i_pt){
						uchar *img_row = image.ptr<uchar>(i_pt);
						for (int j_pt = std::max(0, j_start); j_pt < std::min(in_width, j_end); ++j_pt){
							for (int k_pt = 0; k_pt < in_depth; ++k_pt){
								output_row[j * 3 + k] += img_row[j_pt * 3 + k_pt] * filters[k]->w[i_pt - i_start][j_pt - j_start][k_pt];
							}
						}
					}
					
					output_row[j * 3 + k] += filters[k]->b;
				}
			}
		}
		return output;
	}
};

#endif
