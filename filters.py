import numpy as np

def erosion(arr,kernel_len):   
    x=arr.shape[0]
    y=arr.shape[1]    
    arr = add_padding(kernel_len,arr)  
    erosion_arr = np.zeros(arr.shape)
    for i in range( arr.shape[0] ):
        for j in range( arr.shape[1] ):
            erosion_arr[i, j, 0] =  np.min(arr[i:i+kernel_len, j:j+kernel_len, 0])
            erosion_arr[i, j, 1] =  np.min(arr[i:i+kernel_len, j:j+kernel_len, 1])
            erosion_arr[i, j, 2] =  np.min(arr[i:i+kernel_len, j:j+kernel_len, 2]) 
            
    return minus_padding(kernel_len,x,y,erosion_arr)   

def dilation(arr,kernel_len):  
    x=arr.shape[0]
    y=arr.shape[1]    
    arr = add_padding(kernel_len,arr)  
    dilation_arr =  np.zeros(arr.shape) 
    for i in range( arr.shape[0] ):
        for j in range( arr.shape[1]):
            dilation_arr[i, j, 0] =  np.max(arr[i:i+kernel_len, j:j+kernel_len, 0])
            dilation_arr[i, j, 1] =  np.max(arr[i:i+kernel_len, j:j+kernel_len, 1])
            dilation_arr[i, j, 2] =  np.max(arr[i:i+kernel_len, j:j+kernel_len, 2]) 
    return  minus_padding(kernel_len,x,y,dilation_arr)   

def edge_detection(arr):
    #gray scale dilation 
    kernel_len = 3 

    dilation_arr =  dilation(arr,kernel_len)
    erosion_arr = erosion(arr,kernel_len) 
    return dilation_arr - erosion_arr

def gradient(arr):
    #gray scale dilation 
    kernel_len = 3
    
    dilation_arr =  dilation(arr,kernel_len)
    erosion_arr = erosion(arr,kernel_len) 

    return (dilation_arr - erosion_arr)/2

def conditional_dilation(arr):  
    kernel_len = 3  
    return arr


def add_padding(pad,arr):
    return np.pad(arr,  ((pad,pad ),(pad,pad ),(0,0)),"constant", constant_values=(180))


def minus_padding(pad,x,y,arr): 
    return arr[pad:x+pad,pad:y+pad,0:3]
