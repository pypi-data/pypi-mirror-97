import numpy as np
import SimpleITK as sitk 
from skimage.measure import label
#from radiomics.featureextractor import RadiomicsFeatureExtractor
import matplotlib.pyplot as plt
import scipy as sc
from sklearn import mixture




class Mask3D : 

    def __init__(self, mask_path): 
        self.mask_path = mask_path
        self.mask = self.read_mask_array()

    
    def read_mask_array(self):
        mask_img = sitk.ReadImage(self.mask_path)
        pixel_spacing = mask_img.GetSpacing()
        self.spacing = pixel_spacing #len 3 si mask 3D 
        self.origin = mask_img.GetOrigin()
        self.direction = mask_img.GetDirection()
        self.size = mask_img.GetSize()
        return sitk.GetArrayFromImage(mask_img).transpose() #[x,y,z]


    def get_binary_threshold_mask(self, threshold): #0.5
        size = self.mask.shape
        threshold_mask = np.zeros(size)
        x,y,z = np.where(self.mask > threshold)
        for j in range(len(x)):
            threshold_mask[x[j], y[j], z[j]] = 1

        return threshold_mask.astype(np.uint8)
        

    def get_mask_spacing(self):
        return self.spacing

    def get_mask_size(self) :
        return self.size

    def get_mask_origin(self):
        return self.origin

    def get_mask_direction(self):
        return self.direction