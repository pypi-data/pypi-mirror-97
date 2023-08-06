import os
from library_dicom.dicom_processor.model.reader.Instance import Instance
from library_dicom.dicom_processor.model.Series import Series
from library_dicom.dicom_processor.model.SeriesPT import SeriesPT
from library_dicom.dicom_processor.enums.SopClassUID import *

def get_series_object(path):
    try:
        first_file_name = os.listdir(path)[0]
    except Exception as err:
        print(err)
        print(path)
    first_instance = Instance( os.path.join(path,first_file_name) )
    sop_class_uid = first_instance.get_sop_class_uid()
    if(sop_class_uid == ImageModalitiesSOPClass.PT.value or sop_class_uid == ImageModalitiesSOPClass.EnhancedPT.value):
        return SeriesPT(path)
    else : return Series(path)