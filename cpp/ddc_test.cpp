#include <hls_video.h>
#include <hls_opencv.h>
#include <ap_fixed.h>
#include <ap_int.h>
#include <cassert>
#include <iostream>

void iso_blue(volatile uint32_t* in_data, volatile uint32_t* out_data, int w, int h);

int main(){

	cv::Mat img_source = cv::imread("/home/sg7118/DDC/test.jpg", CV_LOAD_IMAGE_UNCHANGED);
	std::cout << "Image type: " << img_source.type() << ", no. of channels: " << img_source. channels() << std::endl;

	uchar* data_p = img_source.data;

	int w = 1280;
	int h = 720;

	uchar *image = (uchar *)malloc(w*h*4);

	for (int i=0; i<w*h; i++){
		image[4*i + 0] = data_p[3*i + 2]; //R - R
		image[4*i + 1] = data_p[3*i + 1]; // B - B
		image[4*i + 2] = data_p[3*i + 0]; // G - G
		image[4*i + 3] = 0;
	}
	iso_blue((volatile uint32_t *)image, (volatile uint32_t *)image, w, h);

	for (int i=0; i<w*h; i++){
		data_p[3*i + 2] = image[4*i + 0];
		data_p[3*i + 1] = image[4*i + 1];
		data_p[3*i + 0] = image[4*i + 2];
	}

	cv::imwrite("/home/sg7118/DDC/test_out.jpg", img_source);

	free(image);
	return 0;
}
