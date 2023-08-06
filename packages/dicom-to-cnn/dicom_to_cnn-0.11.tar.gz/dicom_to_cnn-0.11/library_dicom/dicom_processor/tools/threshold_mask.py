import numpy as np

#with any threshold 3d mask label

def threshold_matrix(mask_array, pet_array, threshold):
    """ Return a thresholded mask
    """
    if threshold < 1 : 
        if len(mask_array.shape) != 3 :  #mask 4D 
            number_of_roi = mask_array.shape[3]
            liste = []
            for i in range(number_of_roi):
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] ))
                suv_values = []
                x,y,z = np.where(mask_array[:,:,:,i] != 0)
                if len(x) != 0 : 
                    suv_values = pet_array[x,y,z].tolist()
                    seuil = np.max(suv_values) * threshold
                    new_mask[np.where((pet_array > seuil) & (mask_array[:,:,:,i] > 0))] = 1
                    liste.append(new_mask)
                else : liste.append(new_mask)
            return np.stack(liste, axis = 3)    

        else : 
            maxi = np.max(mask_array)
            if maxi == 1.0 : 
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] ))
                x,y,z = np.where(mask_array != 0)
                suv_values = pet_array[x,y,z].tolist()
                seuil = np.max(suv_values) * threshold
                new_mask[np.where((pet_array > seuil) & (mask_array > 0))] = 1
                return new_mask
                 

            else :  
                number_of_roi = maxi
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] ))
                for i in range(number_of_roi):
                    suv_values = []
                    x,y,z = np.where(mask_array == i)
                    suv_values = pet_array[x,y,z].tolist()
                    seuil = np.max(suv_values) * threshold
                    new_mask[np.where((pet_array > seuil) & (mask_array == i))] = i
                return new_mask



    else : 
        if len(mask_array.shape) != 3 :  #mask 4D 
            number_of_roi = mask_array.shape[3]
            liste = []
            for i in range(number_of_roi):
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] ))
                seuil = threshold
                new_mask[np.where((pet_array > seuil) & (mask_array[:,:,:,i] > 0))] = 1
                liste.append(new_mask)

            return np.stack(liste, axis = 3)    

        else : 
            maxi = np.max(mask_array)
            if maxi == 1.0 : 
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] ))
                seuil = threshold
                new_mask[np.where((pet_array > seuil) & (mask_array > 0))] = 1
                return new_mask
                 

            else :  
                number_of_roi = maxi
                new_mask = np.zeros((mask_array.shape[0],mask_array.shape[1], mask_array.shape[2] ))
                seuil = threshold
                for i in range(number_of_roi):
                    new_mask[np.where((pet_array > seuil) & (mask_array == i))] = i
                return new_mask




"""
def get_threshold_matrix(ws_array, pet_array, number_of_roi, threshold) : #0.41
    for i in range(1, number_of_roi + 1):
        #print(i)
        points = []
        suv_values = []
        x,y,z = np.where(ws_array == i)
        for j in range(len(x)): 
            points.append([x[j], y[j], z[j]])

        #SEUIL A 41%
        for point in points : 
            suv_values.append(pet_array[point[0], point[1], point[2]])

        seuil = np.max(suv_values) * threshold


        for point in points : 
            if pet_array[point[0], point[1], point[2]] <= seuil : 
                ws_array[point[0], point[1], point[2]] = 0

    return ws_array

#for 4D matrix
def get_threshold_matrix_4D(mask, pet_array, threshold) : #0.41
    if len(mask.shape) != 3 :  #plusieurs ROI 
        number_of_roi = mask.shape[3]
    else : 
        number_of_roi = 1 #1 ROI 

    for i in range(number_of_roi):

        points = []
        suv_values = []
        if len(mask.shape) != 3 : #PLUSIEURS ROI 
            x,y,z = np.where(mask[:,:,:,i] != 0)
        else : #1 ROI 
            x,y,z = np.where(mask != 0)

        for j in range(len(x)): 
            points.append([x[j], y[j], z[j]])

        for point in points :  
            suv_values.append(pet_array[point[0], point[1], point[2]])

        if len(suv_values) != 0 :
            seuil = np.max(suv_values) * threshold
        else : seuil = 0


        for point in points : 
            if pet_array[point[0], point[1], point[2]] <= seuil : 
                if len(mask.shape) != 3 : #PLUSIEURS ROI 
                    mask[point[0], point[1], point[2], i] = 0
                else :  mask[point[0], point[1], point[2]] = 0 #1 ROI 

        
    return mask


#from csv

def get_suv_max(nifti_array, list_points):
    list_suv = []
    if list_points != [] :
        for point in list_points : 
            list_suv.append(nifti_array[point[1], point[0], point[2]])

        return np.max(list_suv)
    else : return 0.0 #pas de suv max


def threshold_mask(mask_4D, details_rois, nifti_array):

    number_of_roi = mask_4D.shape[3]

    for roi in range(number_of_roi) : 
        list_points = details_rois[roi + 1]['list_points']
        suv_max = get_suv_max(nifti_array, list_points)

            #GET THRESHOLD
        threshold = details_rois['SUVlo']
        if "%" in threshold : 
            threshold = float(threshold.strip("%"))/100 * suv_max
        else : 
            threshold = float(threshold)
        

        for point in list_points :
            if nifti_array[point[1], point[0], point[2]] <= threshold :

                mask_4D[point[1], point[0], point[2], roi] = 0
 
    return mask_4D


""" 
            
       

            

            