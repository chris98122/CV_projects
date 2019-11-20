import numpy as np

def erosion(arr,pad):   
    x=arr.shape[0]
    y=arr.shape[1]    
    arr = add_padding(pad*2,arr)  
    erosion_arr = np.zeros(arr.shape)
    for i in range( pad,arr.shape[0] ):
        for j in range( pad,arr.shape[1] ):
            erosion_arr[i, j, 0] =  np.min(arr[i-pad:i+pad, j-pad:j+pad, 0])
            erosion_arr[i, j, 1] =  np.min(arr[i-pad:i+pad, j-pad:j+pad, 1])
            erosion_arr[i, j, 2] =  np.min(arr[i-pad:i+pad, j-pad:j+pad, 2])
            
    return minus_padding(pad*2,x,y,erosion_arr)   

def dilation(arr,pad):  
    x=arr.shape[0]
    y=arr.shape[1]    
    arr = add_padding(pad*2,arr)  
    dilation_arr =  np.zeros(arr.shape) 
    for i in range( pad,arr.shape[0] ):
        for j in range( pad,arr.shape[1]):
            dilation_arr[i, j, 0] =  np.max(arr[i-pad:i+pad, j-pad:j+pad, 0])
            dilation_arr[i, j, 1] =  np.max(arr[i-pad:i+pad, j-pad:j+pad, 1])
            dilation_arr[i, j, 2] =  np.max(arr[i-pad:i+pad, j-pad:j+pad, 2])
    return  minus_padding(pad*2,x,y,dilation_arr)  

def andarr(a,b):
    assert(a.shape[0] == b.shape[0]) 
    assert(a.shape[1] == b.shape[1])
    c= np.zeros(a.shape)
    for i in range(a.shape[0] ):
        for j in range(a.shape[1]):
            if a[i,j,0] == b[i,j,0]:
                c[i,j,0] = a[i,j,0]
            if a[i,j,1] == b[i,j,1]:
                c[i,j,1] = a[i,j,1]
            if a[i,j,2] == b[i,j,2]:
                c[i,j,2] = a[i,j,2]
    return c

def edge_detection(arr):
    #gray scale dilation 
    kernel_len = 3

    dilation_arr =  dilation(arr,kernel_len//2)
    erosion_arr = erosion(arr,kernel_len) 
    return dilation_arr - erosion_arr

def gradient(arr):
    #gray scale dilation 
    kernel_len = 3
    
    dilation_arr =  dilation(arr,kernel_len//2)
    erosion_arr = erosion(arr,kernel_len) 

    return (dilation_arr - erosion_arr)/2

def conditional_dilation(arr):  
    kernel_len = 2  
    M_arr = dilation(erosion(arr,kernel_len) ,kernel_len) 
    count=1
    while(1):
        T_arr= M_arr
        M_arr = dilation(M_arr ,kernel_len)
        M_arr =andarr(M_arr,arr)
        if((T_arr == M_arr).all()):
            return T_arr
        count = count+1
        if (count> 30):
            return T_arr
    return arr

def grey_recon(arr):
    return arr

def add_padding(pad,arr):
    return np.pad(arr,  ((pad,pad ),(pad,pad ),(0,0)),"constant", constant_values=(180))


def minus_padding(pad,x,y,arr): 
    return arr[pad:x+pad,pad:y+pad,0:3]
