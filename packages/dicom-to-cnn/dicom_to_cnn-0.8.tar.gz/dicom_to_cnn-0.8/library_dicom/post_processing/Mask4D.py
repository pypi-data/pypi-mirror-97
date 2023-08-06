import numpy as np
import SimpleITK as sitk 
from skimage.measure import label
#from radiomics.featureextractor import RadiomicsFeatureExtractor
import matplotlib.pyplot as plt
import scipy as sc
from sklearn import mixture



class Mask4D : 

    def __init__(self, mask_path): 
        self.mask_path = mask_path
        self.mask = self.read_mask_array()
        self.binary_mask = self.get_binary_mask()




    def read_mask_array(self):
        mask_img = sitk.ReadImage(self.mask_path)
        pixel_spacing = mask_img.GetSpacing()
        self.spacing = pixel_spacing #len  4 si mask  4D
        self.origin = mask_img.GetOrigin()
        self.direction = mask_img.GetDirection()
        self.size = mask_img.GetSize()
        return sitk.GetArrayFromImage(mask_img).transpose() #[x,y,z,channel]

    def get_threshold_mask(self, pet_array, threshold) : 
        mask_4D =  self.read_mask_array()
        number_of_roi = mask_4D.shape[3]
        for roi in range(number_of_roi) :
            #suv_values = []
            #suv_values.append(pet_array[np.where(mask_4D[:,:,:,roi] != 0 )])

            #maxi = np.max(suv_values)
            seuil = threshold
            #seuil = float(threshold)
            x,y,z = np.where(mask_4D[:,:,:,roi] != 0)
            for j in range(len(x)) :
                if pet_array[x[j],y[j],z[j]] <= seuil :
                    mask_4D[x[j],y[j],z[j],roi] = 0

        return mask_4D.astype(np.uint8)

    def get_binary_threshold_mask(self, pet_array, threshold) :
        threshold_mask =  self.get_threshold_mask(pet_array, threshold)
        shape_mask = threshold_mask.shape
        binary_threshold_mask = np.zeros((shape_mask[0], shape_mask[1], shape_mask[2]))
        sum_mask = np.ndarray.sum(threshold_mask, axis = -1)
        binary_threshold_mask[np.where(sum_mask != 0)] = 1
        return binary_threshold_mask.astype(np.uint8)



    def get_binary_mask(self) :
        shape_mask = self.mask.shape
        binary_mask = np.zeros((shape_mask[0], shape_mask[1], shape_mask[2]))
        sum_mask = np.ndarray.sum(self.mask, axis = -1)
        binary_mask[np.where(sum_mask != 0)] = 1
        return binary_mask.astype(np.uint8)


    def get_mask_spacing(self):
        return self.spacing[:3]

    def get_mask_size(self): 
        return self.size[:3]

    def get_mask_origin(self):
        return self.origin[:3]

    def get_mask_direction(self):
        return (self.direction[0], self.direction[1], self.direction[2], 
                            self.direction[4], self.direction[5], self.direction[6], 
                            self.direction[8],  self.direction[9], self.direction[10])
