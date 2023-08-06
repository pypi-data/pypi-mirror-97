import numpy as np

def is_integer(s:str):
    if not s:
        return False
    if len(s) == 1:
        return s.isdigit()
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def array_swap(arr1:np.ndarray, arr2:np.ndarray, indices):
    arr1[indices], arr2[indices] = arr2[indices], arr1[indices]
    
def reorder_arrays(*arrays, descending:bool=True):
    if descending:
        if not (arrays[0].dtype.type in [np.string_, np.str_]):
            indices = np.argsort(-arrays[0])
        else:
            indices = np.argsort(arrays[0])[::-1]
    else:
        indices = np.argsort(arrays[0])
    for arr in arrays:
        arr[:] = arr[indices]    
        
        
def reverse_arrays(*arrays):
    for arr in arrays:
        arr[:] = arr[::-1] 