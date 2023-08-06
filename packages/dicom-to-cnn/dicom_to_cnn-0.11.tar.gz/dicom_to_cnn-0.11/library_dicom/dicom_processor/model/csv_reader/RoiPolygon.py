import matplotlib.patches
import numpy as np
from library_dicom.dicom_processor.model.csv_reader.Roi import Roi

"""Derivated Class for manual Polygon ROI of PetCtViewer.org

Returns:
    [RoiPolygon] -- Polygone ROI
"""
class RoiPolygon(Roi):

    def __init__(self, axis, first_slice, last_slice, roi_number, type_number, list_point, volume_dimension):
        super().__init__(axis, first_slice, last_slice, roi_number, type_number, list_point, volume_dimension)
        self.list_points = self.calculateMaskPoint()

    def calculateMaskPoint(self):
        """list of [x,y,z] coordonates of a ROI 

        Returns:
            [type] -- [description]
        """
        #np_array_3D = super().get_empty_np_array()
        #x,y,z = np_array_3D.shape

        roi_pixel_matplot = self.__create_closed_polygon()
        list_points = []
        #list_slices = []
        for number_slice in range(self.first_slice - 1  , self.last_slice ) : 
            #print(number_slice)
            point = super().mask_roi_in_slice(roi_pixel_matplot)
            #np_array_3D[:,:,number_of_slices] = mask
            for i in range(len(point)):
                point[i].append(number_slice) 


            list_points.extend(point)
        
        #if (self.axis == 2) : 
           # return super().coronal_to_axial(np_array_3D)
        #elif (self.axis == 3) :
            #return super().sagittal_to_axial(np_array_3D)

        #return np.transpose(np_array_3D.astype(np.uint8), (1,0,2)), list_points, list_slices
        return list_points

    def __create_closed_polygon(self):
        points_array = self.list_point_np
        return matplotlib.patches.Polygon(points_array  , closed = True)