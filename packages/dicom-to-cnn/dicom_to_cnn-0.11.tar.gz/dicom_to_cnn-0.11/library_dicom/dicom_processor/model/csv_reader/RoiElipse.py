import matplotlib
import numpy as np
from library_dicom.dicom_processor.model.csv_reader.Roi import Roi
import math

"""Derivated Class for manual Elipse ROI of PetCtViewer.org

Returns:
    [RoiElipse] -- Roi Elipse Object
"""
class RoiElipse(Roi):

    def __init__(self, axis, first_slice, last_slice, roi_number, type_number, list_point, volume_dimension):
        super().__init__(axis, first_slice, last_slice, roi_number, type_number, list_point, volume_dimension)
        self.list_points = self.calculateMaskPoint()


    def calculateMaskPoint(self):
        #np_array_3D = super().get_empty_np_array()
        #x,y,z = np_array_3D.shape
        points_array = self.list_point_np 
        x0 = points_array[0][0]
        y0 = points_array[0][1]
        delta_x = points_array[1][0] - x0
        #print("delta_x =", delta_x)
        delta_y = abs(points_array[2][1] - y0)
        #print("delta_y =", delta_y)
        middle = ((self.first_slice + self.last_slice) / 2) - 1
        rad1 = ((self.last_slice - self.first_slice) / 2) 

        list_points = []
        if(rad1 == 0) :
            return list_points

        for number_slice in range(self.first_slice  , self.last_slice - 1 ) : 
            diff0 = abs(middle - number_slice)
            factor = pow(rad1,2) - pow(diff0,2)
            factor = math.sqrt(factor) / rad1
            #print((factor))

            width = factor * delta_x
            height = factor * delta_y
        
            roi_pixel_matplot = self.__create_elipse(2 * width, 2 * height)
            point = super().mask_roi_in_slice(roi_pixel_matplot)

            for i in range(len(point)):
                point[i].append(number_slice)

            #np_array_3D[:,:,number_of_slices] = mask
            
            list_points.extend(point)
        #list_points.append([x0, y0, self.first_slice - 1])
        #list_points.append([x0, y0, self.last_slice - 1])
        #print(list_points)

        #return np.transpose(np_array_3D.astype(np.uint8), (1,0,2)) , list_points, list_slices

        return list_points

    def __create_elipse(self, width, height): 
        points_array = self.list_point_np  
        #width = 2 * abs(points_array[0][0] - points_array[1][0]) #centre_x - est_x 
        #height = 2 * abs(points_array[0][1] - points_array[2][1]) #centre_y - nord_y
        return matplotlib.patches.Ellipse(points_array[0], width, height, angle = 0)



    