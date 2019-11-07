
import numpy as np

def Gaussian_filter_implement(kernel_len,sigma,arr): 
    gaus_filter = Gaussian_filter(kernel_len,sigma)
    smooth_arr = arr
    for i in range( arr.shape[0] - kernel_len):
        for j in range( arr.shape[1] - kernel_len):
            smooth_arr[i, j, 0] = ( arr[i:i+kernel_len, j:j+kernel_len, 0]*gaus_filter).sum() 
            smooth_arr[i, j, 1] = ( arr[i:i+kernel_len, j:j+kernel_len, 1]*gaus_filter).sum() 
            smooth_arr[i, j, 2] = ( arr[i:i+kernel_len, j:j+kernel_len, 2]*gaus_filter).sum() 
    return  smooth_arr
 

def Gaussian_filter(n, sigma):
    nn = int((n-1)/2)
    print(nn)
    a = np.asarray([[x**2 + y**2 for x in range(-nn,nn+1)] for y in range(-nn,nn+1)])
    # np.asarray可以将输入转化为np.array, 这里输入为一个列表推导式
    kernel = np.exp(-a/(2*sigma**2)) 
    kernel /= np.sum(kernel)
    print( kernel.shape)
    return kernel
 

 