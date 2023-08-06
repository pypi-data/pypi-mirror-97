import matplotlib
import numpy as np
from library_dicom.dicom_processor.model.csv_reader.Roi import Roi

"""Derivated Class for automatic Nifti ROI of PetCtViewer.org

Returns:
    [RoiNifti] -- Nifti ROI
"""
class RoiNifti(Roi):

    def __init__(self, roi_number, list_point, volume_dimension):
        super().__init__(1, 0, 0, roi_number, 0, list_point, volume_dimension)
        self.list_points = self.calculateMaskPoint()

    def calculateMaskPoint(self):
        pixel_array = self.list_point
        list_points = []
    
        for points in pixel_array :
            if len(points) != 0 : 

                list_points.append(points)

        return list_points