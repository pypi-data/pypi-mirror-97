import pydicom 
import numpy as np

class RTROIObservationsSequence :

    def __init__(self, mask_4D, dict_roi_data):
        self.mask_4D = mask_4D
        self.number_of_roi = self.mask_4D.shape[3]
        self.dict_roi_data = dict_roi_data


    def create_RTROIObservationsSequence(self):
        RTROIObservationsSequence = pydicom.sequence.Sequence()
        for number_roi in range(1, self.number_of_roi +1) : 
            dataset = pydicom.dataset.Dataset()
            dataset.ReferencedROINumber = number_roi
            if self.dict_roi_data[number_roi]['ROIName'] != '' : 
                dataset.ROIObservationLabel = self.dict_roi_data[number_roi]['ROIName']

            else : dataset.ROIName = str(number_roi)

            if 'ROIInterpretedType' in self.dict_roi_data[number_roi] : 
                dataset.ROIInterpretedType = self.dict_roi_data[number_roi]['ROIInterpretedType']

            RTROIObservationsSequence.append(dataset)

        return RTROIObservationsSequence 