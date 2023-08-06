import numpy as np
import SimpleITK as sitk 
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage import segmentation
import scipy
from skimage import morphology
from library_dicom.post_processing.PostProcess_Reader import PostProcess_Reader
from library_dicom.dicom_processor.tools.create_mip import *

class WatershedModel(PostProcess_Reader):

    def __init__(self, mask_path, pet_path, type):
        super().__init__(mask_path, pet_path, type)


    def get_labels_for_model(self, labelled_threshold_array, num_labels):
        label = []
        vol_roi = []
        for key in range(1, num_labels + 1) :
            volume_voxel = self.pet_spacing[0] * self.pet_spacing[1] * self.pet_spacing[2] * 10**(-3)
            number_pixel = len(np.where(labelled_threshold_array == key)[0])
            volume_roi = volume_voxel * number_pixel

            if volume_roi > float(30) :
                label.append(key)
                vol_roi.append(volume_roi)
        return label, vol_roi

    def get_pet_view(self, pet_array, labelled_mask):
        new_mask = np.zeros(self.size_matrix)
        new_mask[np.where(labelled_mask != 0)] = pet_array[np.where(labelled_mask !=0)]
        return new_mask.astype(np.uint8)


    def get_suv_values_matrix(self, label, labelled_threshold_mask):
        #x,y,z = self.size_matrix
        new_matrix = np.zeros(self.size_matrix)
        new_matrix[np.where(labelled_threshold_mask == label)] = self.pet_array[np.where(labelled_threshold_mask== label)]
        return new_matrix

    def get_mask_roi_matrix(self, label, labelled_threshold_mask):
        #x,y,z = self.size_matrix
        new_matrix = np.zeros(self.size_matrix)
        new_matrix[np.where(labelled_threshold_mask == label)] = 1
        return new_matrix.astype(np.uint8)



    def get_distance_map(self, threshold_matrix):
        return ndimage.distance_transform_edt(threshold_matrix)

    #def get_local_peak(self, distance_map, number_max_peak):
        #min_dist = int(2/np.mean(self.pet_spacing))
        #if min_dist == 0 : 
        #    return peak_local_max(distance_map, indices = False)
        #else : 

        #return peak_local_max(distance_map, indices = False, num_peaks= number_max_peak)

    def get_local_peak(self, distance_map):
        spacing = []
        spacing.append(float(self.pet_spacing[0]) * 10**(-1))
        spacing.append(float(self.pet_spacing[1]) * 10**(-1))
        spacing.append(float(self.pet_spacing[2]) * 10**(-1))
        
        min_dist = int(2/np.mean(spacing))
        #print("min dist :", min_dist)

        #localMax_1 = peak_local_max(distance_map, indices = True, min_distance= min_dist)
        #suv_max = []
        #for point in localMax_1 : 
        #    suv_max.append(self.pet_array[point[0], point[1], point[2]])

        #moy = np.mean(suv_max)
        return peak_local_max(distance_map, indices = False, min_distance=min_dist)


    def define_marker_array(self, localMax):
        #marker_array = np.zeros(self.size_matrix)
        #for marker in range(len(localMax)) : 
            #marker_array[localMax[marker][0], localMax[marker][1], localMax[marker][2]] = marker + 1

        marker_array, num_features = ndimage.label(localMax) #, structure=np.ones((3,3,3)))
        return marker_array.astype(np.uint8), num_features
 

    def watershed_segmentation(self, distance_map, marker_array, mask) : 
        labels = segmentation.watershed(distance_map, marker_array, mask = mask)
        return labels.astype(np.uint8)


    def watershed_model(self, threshold) : 
        binary_threshold_mask_img = self.get_binary_threshold_mask_img(threshold)
        binary_threshold_mask_array = self.remove_small_roi(binary_threshold_mask_img)
        labelled_threshold_array, num_labels = self.get_labelled_threshold_mask_array(binary_threshold_mask_array)
       

        label_coordonate = self.label_coordonate(labelled_threshold_array, num_labels)

        labels_for_model, vol_roi = self.get_labels_for_model(labelled_threshold_array, num_labels)
        for label in labels_for_model : 

            suv_values= self.get_suv_values_matrix(label, labelled_threshold_array)
            
            #distance_map = self.get_distance_map(suv_values)

            #localMax = self.get_local_peak(distance_map, number_max_peak)
            localMax = self.get_local_peak(suv_values)
            #local_min = morphology.local_minima(suv_values, allow_borders=False)

            marker_array, num_features = self.define_marker_array(localMax)

            if num_features != 0 : 
                #new_distance_map = -1 * distance_map
                new_label_mask = self.watershed_segmentation(-suv_values, marker_array, suv_values)
                new_coordonate = []
                for new_label in range(1, num_features + 1):
                    if len(np.where(new_label_mask == new_label)[0]) != 0 : 
                        new_coordonate.append(np.where(new_label_mask == new_label))

                label_coordonate[label] = new_coordonate


        liste_coordonate = self.extract_coordonate(label_coordonate)
        number_total_of_label = len(liste_coordonate)
        liste_label = np.arange(1, number_total_of_label + 1, 1)
        return self.watershed_matrix(liste_coordonate, liste_label), len(liste_label)


    def extract_coordonate(self, results):
        liste = []
        for key in range(1, len(results) + 1) : 
            number_coord = len(results[key])
            for i in range(number_coord) : 
                liste.append(results[key][i])
        return liste 

    def watershed_matrix(self, liste_coordonate, liste_label) :
        ws_matrix = np.zeros(self.size_matrix)
        for coordonate, label in zip(liste_coordonate, liste_label) :
            ws_matrix[coordonate] = label

        return ws_matrix.astype(np.uint8)


    def get_watershed_img(self, ws_array):
        img = sitk.GetImageFromArray(ws_array.transpose())
        img.SetSpacing(self.pet_spacing)
        img.SetDirection(self.pet_direction)
        img.SetOrigin(self.pet_origin)

        return img
