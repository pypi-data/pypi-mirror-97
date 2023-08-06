from library_dicom.dicom_processor.model.Series import Series
import numpy as np

class SeriesCT(Series):
    """Get Series CT Nifti in 16 Bits

    Arguments:
        Series {String} -- Series Location Path
    """

    def __init__(self,path):
        super().__init__(path)

    def get_numpy_array(self):
        numpy_array = super().get_numpy_array()
        return numpy_array.astype(np.int16)
