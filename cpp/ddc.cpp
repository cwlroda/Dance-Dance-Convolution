#include <hls_video.h>
#include <ap_fixed.h>
#include <ap_int.h>
#include <stdint.h>
#include <assert.h>

typedef hls::Mat<720, 1280, HLS_16UC3> RGB_IMAGE;

void iso_blue(volatile uint32_t* in_data, volatile uint32_t* out_data, int w, int h){

	for (int i = 0; i < h; ++i) {

		for (int j = 0; j < w; ++j) {

			unsigned int current = *in_data++;

			int in_r = current & 0xFF;
			int in_g = (current >> 8) & 0xFF;
			int in_b = (current >> 16) & 0xFF;

			float out_r = float(in_r)/255;
			float out_g = float(in_g)/255;
			float out_b = float(in_b)/255;

			float max, min;
			if(out_g >= out_r){
			// g >= r
				if(out_b >= out_g){
					// b >= g >= r
					max = out_b;
					min = out_r;
				}
				else{
					// g >= b, g >= r
					max = out_g;
					if(out_b >= out_r){
						// g >= b >= r
						min = out_r;
					}
					else{
						// g >= r > b
						min = out_b;
					}
				}
			}
			else{
				//r > g
				if(out_b >= out_r){
					// b >= r > g
					max = out_b;
					min = out_g;
				}
				else{
					// r > b, r > g
					max = out_r;
					if(out_g >= out_b){
						// r > g >= b
						min = out_b;
					}
					else{
						// r > b > g
						min = out_g;
					}
				}
			}
			float delta = max - min;

			float h_raw = 0;
			int h;
			if(delta != 0){
				if(max == out_r){
					h_raw = ((out_g-out_b)/delta) * 60;
				}
				else if(max == out_g){
					h_raw = (((out_b-out_r)/delta)+2) * 60;
				}
				else if(max == out_b){
					h_raw = (((out_r-out_g)/delta)+4) * 60;
				}
			}
			else{
				h = 0;
			}
			h = h_raw;
			h = abs(h);

			float v_raw = max * 100;
			int v = v_raw;

			int s;
			if(v == 0){
				s = 0;
			}
			else{
				float s_raw = (delta / max) * 100;
				s = s_raw;
			}

			if( (180 <= h) && (h <= 220) && (30 <= s) && (s <= 100) && (48 <= v) && (v <= 100) ){
				//do nothing
			}
			else{
				in_r = 0;
				in_g = 0;
				in_b = 0;
			}

			unsigned int output = in_r | (in_g << 8) | (in_b << 16);
			*out_data++ = output;
		}

	}
}

void hsv_processing(RGB_IMAGE& input, RGB_IMAGE& output){
	hls::GaussianBlur<3,3>(input, input);
	hls::Sobel<1,0,3>(input, output);
}
