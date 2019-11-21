import numpy as np

def erosion(arr,SE):   
    x=arr.shape[0]
    y=arr.shape[1]    
    
    pad_x = SE.shape[0]
    pad_y = SE.shape[1]
    arr = add_padding(max(pad_x,pad_y)*2,arr) 
    erosion_arr = np.zeros(arr.shape)
    for i in range( arr.shape[0] - pad_x):
        for j in range( arr.shape[1] -pad_y):
            erosion_arr[i, j, 0] =  np.min(arr[i:i+pad_x, j:j+pad_y, 0] + SE)
            erosion_arr[i, j, 1] =  np.min(arr[i:i+pad_x , j:j+pad_y, 1] + SE)
            erosion_arr[i, j, 2] =  np.min(arr[i:i+pad_x , j:j+pad_y, 2] + SE)
            
    return  minus_padding(max(pad_x,pad_y)*2,x,y,erosion_arr)  

def dilation(arr,SE):  
    x=arr.shape[0]
    y=arr.shape[1]    
    pad_x = SE.shape[0]
    pad_y = SE.shape[1]
    arr = add_padding(max(pad_x,pad_y)*2,arr)  
    dilation_arr =  np.zeros(arr.shape) 
    for i in range( arr.shape[0]- pad_x):
        for j in range(arr.shape[1]-pad_y):
            dilation_arr[i, j, 0] =  np.max(arr[i:i+pad_x , j:j+pad_y, 0] + SE)
            dilation_arr[i, j, 1] =  np.max(arr[i:i+pad_x , j:j+pad_y, 1] + SE)
            dilation_arr[i, j, 2] =  np.max(arr[i:i+pad_x , j:j+pad_y, 2] + SE)
    return  minus_padding(max(pad_x,pad_y)*2,x,y,dilation_arr)  


def binary_dilation(arr,SE):   
    x=arr.shape[0]
    y=arr.shape[1]    
    pad_x = SE.shape[0]
    pad_y = SE.shape[1]
    arr = add_padding(max(pad_x,pad_y)*2,arr)  
    dilation_arr =  np.zeros(arr.shape) 
    for i in range( arr.shape[0]- pad_x):
        for j in range(arr.shape[1]-pad_y):
            dilation_arr[i, j, 0] =  np.max(np.multiply(arr[i:i+pad_x , j:j+pad_y, 0],SE))
            dilation_arr[i, j, 1] =  np.max(np.multiply(arr[i:i+pad_x , j:j+pad_y, 1] ,SE))
            dilation_arr[i, j, 2] =  np.max(np.multiply(arr[i:i+pad_x , j:j+pad_y, 2] ,SE))
    return  minus_padding(max(pad_x,pad_y)*2,x,y,dilation_arr)  

def binary_erosion(arr,SE):   
    x=arr.shape[0]
    y=arr.shape[1]    
    
    pad_x = SE.shape[0]
    pad_y = SE.shape[1]
    arr = add_padding(max(pad_x,pad_y)*2,arr) 
    erosion_arr = np.zeros(arr.shape)
    for i in range( arr.shape[0] - pad_x):
        for j in range( arr.shape[1] -pad_y):
            erosion_arr[i, j, 0] =  np.min(np.multiply(arr[i:i+pad_x, j:j+pad_y, 0],SE))
            erosion_arr[i, j, 1] =  np.min(np.multiply(arr[i:i+pad_x , j:j+pad_y, 1] ,SE))
            erosion_arr[i, j, 2] =  np.min(np.multiply(arr[i:i+pad_x , j:j+pad_y, 2],SE))
            
    return  minus_padding(max(pad_x,pad_y)*2,x,y,erosion_arr)  

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


def edge_detection(arr,SE):
    #gray scale dilation  
    dilation_arr =  dilation(arr,SE)
    erosion_arr = erosion(arr,SE) 
    return dilation_arr - erosion_arr

def gradient(arr,SE):
    #gray scale dilation 
    dilation_arr =  dilation(arr,SE)
    erosion_arr = erosion(arr,SE)

    return (dilation_arr - erosion_arr)/2

def conditional_dilation(arr,SE): 
    M_arr = binary_dilation(binary_erosion(arr,SE) ,SE) 
    
    count=1
    while(1):
        T_arr= M_arr
        M_arr = binary_dilation(M_arr ,SE)
        M_arr = andarr(M_arr,arr)
        if((T_arr == M_arr).all()):
            return T_arr
        count = count+1
        if (count> 20):
            return T_arr
    return arr

def gray_recon(arr,SE): 
    f = dilation(arr ,SE) 
    M_arr = arr
    count=1
    while(1):
        M_arr = dilation(M_arr,SE) 
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
