import numpy as np 
import SimpleITK as sitk 


def read_img(img_path):
    img = sitk.ReadImage(img_path)
    array = sitk.GetArrayFromImage(img).transpose()
    return array , img.GetSpacing()


def normalize_pet(array):
    x,y,z = np.where(array != 0)
    suv = []
    for j in range(len(x)):
        suv.append(array[x[j], y[j], z[j]])

    suv_max = np.max(suv)

    for i in range(len(x)):
        array[x[i], y[i], z[i]] = (array[x[i], y[i], z[i]] * 255) / suv_max

    return array 

def read_inference(inference_path):
    return sitk.GetArrayFromImage(sitk.ReadImage(inference_path)).transpose()

    
def binarize_mask(mask_array) : 
    size = mask_array.shape 
    binarize = np.zeros(size)
    x,y,z = np.where(mask_array >= 0.5)
    binarize[x,y,z] = 1
    return binarize