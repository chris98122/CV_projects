import numpy as np
from util import *
def erosion(arr,SE,center):   
    x=arr.shape[0]
    y=arr.shape[1]    
    
    kernel_x = SE.shape[0]
    kernel_y = SE.shape[1]

    center_x = center[0]
    center_y = center[1]
    arr = add_padding(max(kernel_x,kernel_y),arr)  
    erosion_arr = np.zeros(arr.shape) 
    for i in range( center_x , arr.shape[0] - (kernel_x- center_x)):
        for j in range(center_y, arr.shape[1]-(kernel_y-center_y)):
            erosion_arr[i, j, 0] =  np.min(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 0] + SE)
            erosion_arr[i, j, 1] =  np.min(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 1] + SE)
            erosion_arr[i, j, 2] =  np.min(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 2] + SE)
            
    return  minus_padding(max(kernel_x,kernel_y),x,y,erosion_arr)    

def dilation(arr,SE,center):  
    x=arr.shape[0]
    y=arr.shape[1]    

    kernel_x = SE.shape[0]
    kernel_y = SE.shape[1]
    
    center_x = center[0]
    center_y = center[1]

    arr = add_padding(max(kernel_x,kernel_y),arr)  
    dilation_arr =  np.zeros(arr.shape) 
    for i in range( center_x , arr.shape[0] - (kernel_x- center_x)):
        for j in range(center_y, arr.shape[1] -(kernel_y-center_y)):
            dilation_arr[i, j, 0] =  np.max(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 0] + SE)
            dilation_arr[i, j, 1] =  np.max(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 1] + SE)
            dilation_arr[i, j, 2] =  np.max(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 2] + SE)
    return  minus_padding(max(kernel_x,kernel_y),x,y,dilation_arr)  


def binary_dilation(arr,SE,center):   
    x=arr.shape[0]
    y=arr.shape[1]    
    
    kernel_x = SE.shape[0]
    kernel_y = SE.shape[1]
    
    center_x = center[0]
    center_y = center[1]

    arr = add_padding(max(kernel_x,kernel_y),arr)  
    dilation_arr =  np.zeros(arr.shape) 
    for i in range( center_x , arr.shape[0] - (kernel_x- center_x)):
        for j in  range(center_y, arr.shape[1] -(kernel_y-center_y)):
            dilation_arr[i, j, 0] =  np.max(np.multiply(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 0] , SE))
            dilation_arr[i, j, 1] =  np.max(np.multiply(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 1] , SE))
            dilation_arr[i, j, 2] =  np.max(np.multiply(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 2] , SE))
    return  minus_padding(max(kernel_x,kernel_y),x,y,dilation_arr)  

def binary_erosion(arr,SE,center):   
    x=arr.shape[0]
    y=arr.shape[1]    
    
    kernel_x = SE.shape[0]
    kernel_y = SE.shape[1]
    
    center_x = center[0]
    center_y = center[1]

    arr = add_padding(max(kernel_x,kernel_y),arr)   
    erosion_arr = np.zeros(arr.shape)
    for i in range( center_x , arr.shape[0] - (kernel_x- center_x)):
        for j in  range(center_y, arr.shape[1] -(kernel_y-center_y)):
            erosion_arr[i, j, 0] =  np.min(np.multiply(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 0] , SE))
            erosion_arr[i, j, 1] =  np.min(np.multiply(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 1] , SE))
            erosion_arr[i, j, 2] =  np.min(np.multiply(arr[i-center_x:i+kernel_x- center_x, j -center_y:j+kernel_y-center_y, 2] , SE))
    return    minus_padding(max(kernel_x,kernel_y),x,y,erosion_arr)  

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

def check_small_than(a,b):
    assert(a.shape[0] == b.shape[0]) 
    assert(a.shape[1] == b.shape[1])
    
    c= np.zeros(a.shape)
    for i in range(a.shape[0] ):
        for j in range(a.shape[1]): 
                c[i,j,0] = min( a[i,j,0], b[i,j,0])  
                c[i,j,1] = min( a[i,j,1], b[i,j,1])  
                c[i,j,2] = min( a[i,j,2], b[i,j,2])  
    return c

 


def edge_detection(arr,SE,center,mode): 
    dilation_arr =  binary_dilation(arr,SE,center)
    erosion_arr = binary_erosion(arr,SE,center)  

    if mode == STANDARD: 
        return dilation_arr - erosion_arr

    if mode == EXTERNAL:
        return   dilation_arr-arr

    if mode == INTERNAL:
        return  arr-erosion_arr

    assert(0)

def gradient(arr,SE,center):
    #gray scale dilation 
    dilation_arr =  dilation(arr,SE,center)
    erosion_arr = erosion(arr,SE,center)

    return (dilation_arr - erosion_arr)/2

def conditional_dilation(arr,SE,center): 
    M_arr = binary_dilation(binary_erosion(arr,SE,center) ,SE,center) 
    
    count=1
    while(1):
        T_arr= M_arr
        M_arr = binary_dilation(M_arr ,SE,center)
        M_arr = andarr(M_arr,arr)
        if((T_arr == M_arr).all()):
            print("count:",count)
            return T_arr
        count = count+1
        if (count> 20):
            return T_arr
    return arr

def gray_recon(arr,SE,center): 
    f = dilation(arr ,SE,center) 
    M_arr = arr
    count=1
    while(1):
        M_arr = dilation(M_arr,SE,center) 
        temp = M_arr
        M_arr = check_small_than(M_arr,f)
        if((temp == M_arr).all()):
            return M_arr
        count = count+1
        if (count> 30):
            return M_arr

    return arr

def add_padding(pad,arr):
    return np.pad(arr,  ((pad,pad ),(pad,pad ),(0,0)),"constant", constant_values=(180))


def minus_padding(pad,x,y,arr): 
    return arr[pad:x+pad,pad:y+pad,0:3]
