#include <iostream>
#include "opencv2/opencv.hpp"

using namespace std;
using namespace cv;

int main(){
    
    Mat img = imread("../images/color/test.png");
    
    cout << img.rows << " " << img.cols <<  " " << img.channels() << endl;
    
    
    for(int row = 0; row < img.rows; row++){
        uchar* prow = img.ptr<uchar>(row);
        
        for(int col = 0; col < img.cols; col++){
            // opencv는 BGR 순서
            uchar b = prow[col * 3 + 0];
            uchar g = prow[col * 3 + 1];
            uchar r = prow[col * 3 + 2];
            
            printf("(%d, %d, %d), ", r, g, b);
        }
        cout << endl;
    }
    
    
    return 0;
}