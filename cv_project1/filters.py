
import numpy as np

def Gaussian_filter_implement(kernel_len,sigma,arr): 
    gaus_filter = Gaussian_filter(kernel_len,sigma)
    
    
    pad = kernel_len 
    
    x=arr.shape[0]
    y=arr.shape[1]     
    # pad the edges with 0, I guess
    arr = add_padding(pad,arr)  
    smooth_arr =  np.zeros(arr.shape)

    for i in range( arr.shape[0] - kernel_len):
        for j in range( arr.shape[1] - kernel_len):
            smooth_arr[i, j, 0] = ( arr[i:i+kernel_len, j:j+kernel_len, 0]*gaus_filter).sum() 
            smooth_arr[i, j, 1] = ( arr[i:i+kernel_len, j:j+kernel_len, 1]*gaus_filter).sum() 
            smooth_arr[i, j, 2] = ( arr[i:i+kernel_len, j:j+kernel_len, 2]*gaus_filter).sum() 
 
    result =  minus_padding(pad,x,y,smooth_arr) 
    return result

def add_padding(pad,arr):
    return np.pad(arr,  ((pad,pad ),(pad,pad ),(0,0)),"constant", constant_values=(180))

def minus_padding(pad,x,y,arr): 
    return arr[pad//2:x+pad//2,pad//2:y+pad//2,0:3]

def Gaussian_filter(n, sigma):
    gaus_filter = np.array([range(-n//2+1, n//2+1, 1) for _ in range(n)])
    gaus_filter = np.square(gaus_filter) + np.square(gaus_filter.T)
    gaus_filter = (1/(2*np.pi*np.square(sigma)))*np.exp(-gaus_filter/(2*np.square(sigma)))
    return gaus_filter


def Roberts_op_implement(arr): 
    print("Roberts_op")
    R1 = np.array([[1, 0], [0, -1]], np.float32)

    R2 = np.array([[0, 1], [-1, 0]], np.float32)

    
    x=arr.shape[0]
    y=arr.shape[1] 

    pad = 2 
    arr = add_padding(pad,arr)  
    sharp_arr =  np.zeros(arr.shape) 

    for i in range( arr.shape[0] - 2):
        for j in range( arr.shape[1] - 2): 
            sharp_arr [i, j, 0] = abs( (arr[i:i+2, j:j+2, 0]*R1).sum() ) + abs( (arr[i:i+2, j:j+2, 0]*R2).sum() ) 
            sharp_arr [i, j, 1] = abs( (arr[i:i+2, j:j+2, 1]*R1).sum() ) + abs( (arr[i:i+2, j:j+2, 1]*R2).sum() ) 
            sharp_arr [i, j, 2] = abs( (arr[i:i+2, j:j+2, 2]*R1).sum() ) + abs( (arr[i:i+2, j:j+2, 2]*R2).sum() ) 
 

    result = minus_padding(pad,x,y,   sharp_arr ) 
    return result
