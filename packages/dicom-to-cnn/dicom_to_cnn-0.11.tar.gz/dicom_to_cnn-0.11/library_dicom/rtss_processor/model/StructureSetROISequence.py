import pydicom 
import numpy as np


class StructureSetROISequence : 

    def __init__(self, mask_4D, dict_roi_data):
        self.mask_4D = mask_4D
        self.number_of_roi = self.mask_4D.shape[3]
        self.dict_roi_data = dict_roi_data


    def create_StructureSetROISequence(self, pixel_spacing, ReferencedFrameOfReferenceUID) :
        StructureSetROISequence = pydicom.sequence.Sequence()

        for number_roi in range(1 , self.number_of_roi +1):
            dataset = pydicom.dataset.Dataset()
            dataset.ROINumber = number_roi
            dataset.ReferencedFrameOfReferenceUID = ReferencedFrameOfReferenceUID 
            if self.dict_roi_data[number_roi]['ROIName'] != '' : 
                dataset.ROIName = self.dict_roi_data[number_roi]['ROIName']

            else : dataset.ROIName = str(number_roi)

            dataset.ROIVolume = self.get_roi_volume(number_roi, pixel_spacing)
                
             
            if self.dict_roi_data[number_roi]['ROIGenerationAlgorithm'] != '' :
                dataset.ROIGenerationAlgorithm = self.dict_roi_data[number_roi]['ROIGenerationAlgorithm']

            else : dataset.ROIGenerationAlgorithm = 'UNDEFINED'
            
            StructureSetROISequence.append(dataset)
        return StructureSetROISequence 
        
     
    def get_roi_volume(self, number_roi, pixel_spacing):
        number_pixel = 0

        x = np.where(self.mask_4D != 0)[0]
        number_pixel = len(x) #same as len(y) or len(z)
        volume_pixel = pixel_spacing[0] * pixel_spacing[1] * abs(pixel_spacing[2])
        volume_pixel = volume_pixel * 10**(-3) #mm3 to ml 
        roi_volume = number_pixel * volume_pixel 

        return np.round(roi_volume , 5)

