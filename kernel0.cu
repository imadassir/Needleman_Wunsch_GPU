
#include "common.h"
#include "timer.h"



__global__ void nw_gpu0_kernel (unsigned char * reference_d, unsigned char* query_d, int* matrix_d, unsigned int N, unsigned int iteration) {
	int position = blockDim.x*blockIdx.x + threadIdx.x;

	if(position < iteration) {
		int r  = iteration - 1 - position;
		int q = position;
	
		int top     = (q == 0)?((r + 1)*DELETION):(matrix_d[(q - 1)*N + r]);
	        int left    = (r == 0)?((q + 1)*INSERTION):(matrix_d[q*N + (r - 1)]);
	        int topleft = (q == 0)?(r*DELETION):((r == 0)?(q*INSERTION):(matrix_d[(q - 1)*N + (r - 1)]));
	        // Find scores based on neighbors
	        int insertion = top + INSERTION;
	        int deletion  = left + DELETION;
	        int match     = topleft + ((query_d[q] == reference_d[r])?MATCH:MISMATCH);
	        // Select best score
        	int max = (insertion > deletion)?insertion:deletion;
	        max = (match > max)?match:max;
	        matrix_d[q*N + r] = max;		
	}
} 

void nw_gpu0(unsigned char* reference_d, unsigned char* query_d, int* matrix_d, unsigned int N) {
	for (int i = 1; i < N+1; i++) {
		int BLOCK_DIM = (i<512)?32:64;
		int numBlocks = (i+BLOCK_DIM-1)/(BLOCK_DIM);
		nw_gpu0_kernel <<< numBlocks, BLOCK_DIM >>> (reference_d, query_d, matrix_d, N, i);
		cudaDeviceSynchronize();
	}



}
