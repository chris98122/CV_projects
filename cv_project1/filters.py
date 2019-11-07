
import numpy as np

def Gaussian_filter_implement(kernel_len,sigma,arr): 
    gaus_filter = Gaussian_filter(kernel_len,sigma)
    
    
    pad = kernel_len 
        # pad the edges with 0, I guess
    x=arr.shape[0]
    y=arr.shape[1]
    print(pad)
    print(arr.shape)
    arr = np.pad(arr,  ((pad,pad ),(pad,pad ),(0,0)),"constant", constant_values=(180))
    print(arr.shape)
    
    
    smooth_arr =  np.zeros(arr.shape)

    for i in range( arr.shape[0] - kernel_len):
        for j in range( arr.shape[1] - kernel_len):
            smooth_arr[i, j, 0] = ( arr[i:i+kernel_len, j:j+kernel_len, 0]*gaus_filter).sum() 
            smooth_arr[i, j, 1] = ( arr[i:i+kernel_len, j:j+kernel_len, 1]*gaus_filter).sum() 
            smooth_arr[i, j, 2] = ( arr[i:i+kernel_len, j:j+kernel_len, 2]*gaus_filter).sum() 
 
    result =  smooth_arr[pad//2:x+pad//2,pad//2:y+pad//2,0:3]
    print(result.shape)
    return result
 


def Gaussian_filter(n, sigma):
    gaus_filter = np.array([range(-n//2+1, n//2+1, 1) for _ in range(n)])
    gaus_filter = np.square(gaus_filter) + np.square(gaus_filter.T)
    gaus_filter = (1/(2*np.pi*np.square(sigma)))*np.exp(-gaus_filter/(2*np.square(sigma)))
    return gaus_filter

 