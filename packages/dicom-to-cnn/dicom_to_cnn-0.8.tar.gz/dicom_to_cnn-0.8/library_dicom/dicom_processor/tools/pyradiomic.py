from radiomics.featureextractor import RadiomicsFeatureExtractor 
import SimpleITK as sitk 
from itertools import combinations
import numpy as np
from library_dicom.dicom_processor.tools.threshold_mask import *


"""Tools to extract metrics from PET/MASK using pyradiomics
"""


def get_center_of_mass(mask_path, thresh = False, pet_path = None):
    """Get the list of every ROIs center

    Args:
        mask_path ([str]): [nifti MASK path ]
        thresh (bool, optional): [True if want to threshold MASK ]. Defaults to False.
        pet_path ([str], optional): [If thresh is True, nifti PET path]. Defaults to None.

    Returns:
        [list]: [Return a list of list of x,y,z physical coordonates of every ROIs center.]
    """
    center = []

    if pet_path != None : 
        pet_img = sitk.ReadImage(pet_path)
        pet_array = sitk.GetArrayFromImage(pet_img).transpose()


    mask_img = sitk.ReadImage(mask_path)
    mask_array = sitk.GetArrayFromImage(mask_img).transpose()


    type_ = None 
    if len(mask_array.shape) != 3 : 
        type_ = '4D'
        origin = mask_img.GetOrigin()[0:3]
        direc = mask_img.GetDirection()
        direction = direc[0:3] + direc[4:7] + direc[8:11]
        spacing = mask_img.GetSpacing()[0:3]
        size = mask_img.GetSize()[0:3]

        pet_arr = np.random.randint(10, size=(size)).transpose()
        #pet_arr = np.ones(size).transpose()
        pet_sitk = sitk.GetImageFromArray(pet_arr)
        pet_sitk.SetOrigin(origin)
        pet_sitk.SetDirection(direction)
        pet_sitk.SetSpacing(spacing)


    else : 
        type_ = '3D'
        origin = mask_img.GetOrigin()
        direction = mask_img.GetDirection()
        spacing = mask_img.GetSpacing()
        size = mask_img.GetSize() 

        #pet_arr = np.ones(size).transpose()
        pet_arr = np.random.randint(10, size=(size)).transpose()
        pet_sitk = sitk.GetImageFromArray(pet_arr)
        pet_sitk.SetOrigin(origin)
        pet_sitk.SetDirection(direction)
        pet_sitk.SetSpacing(spacing)


    if type_ == '3D' : 
        if thresh == False : 
            number_of_roi = int(np.max(mask_array))
            for i in range(1, number_of_roi + 1) : 
                extractor = RadiomicsFeatureExtractor()
                results = extractor.execute(pet_sitk, mask_img, label = i)
                x, y, z = results['diagnostics_Mask-original_CenterOfMass']
                center.append([x,y,z])

        elif thresh == True : 
            print("mask_seuillé")
            if np.max(mask_array) == 1.0 : 
                mask_threshold = threshold_matrix(mask_array, pet_array, 0.41)
                mask_threshold = mask_threshold.transpose()
                new_mask = sitk.GetImageFromArray(mask_threshold)
                new_mask.SetOrigin(origin)
                new_mask.SetDirection(direction)
                new_mask.SetSpacing(spacing)
                extractor = RadiomicsFeatureExtractor()
                results = extractor.execute(pet_img, new_mask)
                x, y, z = results['diagnostics_Mask-original_CenterOfMass']
                center.append([x,y,z])

            else : 
            
                mask_threshold = threshold_matrix(mask_array, pet_array, 0.41)
                mask_threshold = mask_threshold.transpose()
                new_mask = sitk.GetImageFromArray(mask_threshold)
                new_mask.SetOrigin(origin)
                new_mask.SetDirection(direction)
                new_mask.SetSpacing(spacing)
                for i in range(1, number_of_roi + 1) : 
                    extractor = RadiomicsFeatureExtractor()
                    results = extractor.execute(pet_sitk, new_mask, label = i)
                    x, y, z = results['diagnostics_Mask-original_CenterOfMass']
                    center.append([x,y,z])


    if type_ == '4D' : 
        if thresh == False : 
            for i in range(mask_array.shape[3]):
                mask_3d = mask_array[:,:,:,i]
                mask_3d = mask_3d.transpose()
                new_mask = sitk.GetImageFromArray(mask_3d)
                new_mask.SetOrigin(origin)
                new_mask.SetDirection(direction)
                new_mask.SetSpacing(spacing)
                extractor = RadiomicsFeatureExtractor()
                results = extractor.execute(pet_sitk, new_mask)
                x, y, z = results['diagnostics_Mask-original_CenterOfMass']
                center.append([x,y,z])

        elif thresh == True : 
            mask_4d_threshold = threshold_matrix(mask_array, pet_array, 0.41)
            print("mask seuillé")
            for i in range(mask_array.shape[3]):
                mask_3d = mask_4d_threshold[:,:,:,i]
                x,y,z = np.where(mask_3d != 0)
                if len(x) != 0 : 
                    mask_3d = mask_3d.transpose()
                    new_mask = sitk.GetImageFromArray(mask_3d)
                    new_mask.SetOrigin(origin)
                    new_mask.SetDirection(direction)
                    new_mask.SetSpacing(spacing)
                    extractor = RadiomicsFeatureExtractor()
                    results = extractor.execute(pet_img, new_mask)
                    x, y, z = results['diagnostics_Mask-original_CenterOfMass']
                    center.append([x,y,z])
                else : pass

    return center 


def distance(coord_A, coord_B):
    """calcul euclidian distance between 2 points in 3D 

    Args:
        coord_A ([liste]): [[x,y,z] coordonate point A]
        coord_B ([liste]): [[x,y,z] coordonate point A]

    Returns:
        [float]: [Return euclidian distance]
    """
    return np.sqrt((coord_A[0]-coord_B[0])**2 + (coord_A[1]-coord_B[1])**2 + (coord_A[2]-coord_B[2])**2)


def calcul_distance_max(list_center):
    """Calcul the maximum distance between two ROIs

    Args:
        list_center ([list]): [Return a list of list of x,y,z physical coordonates of every ROIs center]

    Returns:
        [float]: [Return maximum distance, in mm]
    """
    if len(list_center) == 1 : #only 1 roi
        return 0
    else : 
        comb = combinations(list_center, 2)
        comb_liste = list(comb)
        liste_distance = []
        for combinaison in comb_liste : 
            point_A = combinaison[0]
            point_B = combinaison[1]
            liste_distance.append(distance(point_A, point_B))

        maxi = np.max(liste_distance)
  
        return np.round(maxi,2)



def get_bigger_roi_number(mask_path, pet_path):
    img_mask = sitk.ReadImage(mask_path)
    img_pet = sitk.ReadImage(pet_path)
    mask_array = sitk.GetArrayFromImage(img_mask).transpose()
    pet_array = sitk.GetArrayFromImage(img_pet).transpose()

    mask_array = threshold_matrix(mask_array, pet_array, 0.41)
    pixel_spacing = img_pet.GetSpacing() #[x,y,z]

    volume_voxel = pixel_spacing[0]*pixel_spacing[1]*pixel_spacing[2] * 10**(-3)

    if len(mask_array.shape) != 3 : 
        number_of_roi = mask_array.shape[3]
    else : 
        number_of_roi = 1

    volume = []

    for i in range(number_of_roi) : 
        if number_of_roi != 1 :
            number_pixel = len(np.where(mask_array[:,:,:,i] == 1)[0])
        else : 
            number_pixel = len(np.where(mask_array == 1)[0])

        volume.append(volume_voxel * number_pixel)

    volume_max = np.max(volume)
    roi_max = volume.index(volume_max)

    if number_of_roi != 1 : 
        roi = mask_array[:,:,:,roi_max]

    else : roi = mask_array

    x,y,z = np.where(roi == 1)

    suv_values = []
    for j in range(len(x)):
        suv_values.append(pet_array[x[j],y[j],z[j]])

    return roi_max, np.round(np.max(suv_values), 2)



def get_diameter(mask_path, pet_path, number_bigger_roi) : 
    """get 2D and 3D diameter of the biggest ROI in MASK

    Args:
        mask_path ([str]): [Nifti MASK path]
        pet_path ([str]): [Nifti PET path]
        number_bigger_roi ([int]): [Number of the bigger ROI (in volume)]

    Returns:
        [tuple]: [Return 2D and 3D float diameter]
    """
    #PET
    img_pet = sitk.ReadImage(pet_path)
    origin = img_pet.GetOrigin()
    direction = img_pet.GetDirection()
    spacing = img_pet.GetSpacing()
    pet_array = sitk.GetArrayFromImage(img_pet).transpose()
    size = pet_array.shape

    #MASK
    img_mask = sitk.ReadImage(mask_path)
    array_mask = sitk.GetArrayFromImage(img_mask).transpose()

    #seuillage 41% 
    array_mask = threshold_matrix(array_mask, pet_array, 0.41)
    
    if len(array_mask.shape) != 3 :
        bigger_roi = array_mask[:,:,:,number_bigger_roi - 1]

    else : 
        if np.max(array_mask) == 1.0 : 
            bigger_roi = array_mask
        else  : 
    
            x,y,z = np.where(array_mask == number_bigger_roi - 1)
            bigger_roi = np.zeros(size)
            bigger_roi[x,y,z] = 1

 
    new_mask_img = sitk.GetImageFromArray(bigger_roi.transpose())
    new_mask_img.SetOrigin(origin)
    new_mask_img.SetDirection(direction)
    new_mask_img.SetSpacing(spacing)

    extractor = RadiomicsFeatureExtractor()
    results = extractor.execute(img_pet, new_mask_img)
    diameter_3d = results['original_shape_Maximum3DDiameter']
    diameter_2d = results['original_shape_Maximum2DDiameterSlice']
    return float(diameter_2d) , float(diameter_3d)