import pydicom
import os
import numpy as np

from library_dicom.dicom_processor.enums.TagEnum import *
from library_dicom.dicom_processor.enums.SopClassUID import *

class Instance:
    """A class to represent a Dicom file 
    """

    def __init__(self, path, load_image=True):
        """Construct a Dicom file object

        Arguments:
            path {[String]} -- [Absolute path where the Dicom file is located]
        """
        self.path = path
        if (load_image) : self.__load_full_instance()
        else : self.__load_metadata()

    def __load_metadata(self):
        self.dicomData = pydicom.dcmread(self.path, stop_before_pixels=True, force=True)
    
    def __load_full_instance(self):
        self.dicomData = pydicom.dcmread(self.path, force=True)
  
    def get_series_tags(self):
        series_tags={}
        for tag_address in TagsSeries:
            if tag_address.value in self.dicomData :
                series_tags[tag_address.name] = self.dicomData[tag_address.value].value
            else : series_tags[tag_address.name] = "Undefined"
        series_tags[ImageType.ImageType.name] = self.get_image_type()
        series_tags[PixelSpacing.PixelSpacing.name] = self.get_pixel_spacing()
        return series_tags

    def get_patients_tags(self):
        patient_tags={}
        for tag_address in TagsPatient:
            if tag_address.value in self.dicomData : 
                patient_tags[tag_address.name] = self.dicomData[tag_address.value].value
                if( type(self.dicomData[tag_address.value].value) != str):
                    #patient name return PersonName3 object, convert it to string
                    patient_tags[tag_address.name] = str(patient_tags[tag_address.name])
            else : patient_tags[tag_address.name] = "Undefined"
        return patient_tags

    def get_studies_tags(self):
        studies_tags={}
        for tag_address in TagsStudy:
            if tag_address.value in self.dicomData : studies_tags[tag_address.name] = self.dicomData[tag_address.value].value
            else : studies_tags[tag_address.name] = "Undefined"
        return studies_tags

    def get_instance_tags(self):

        instance_tags={}
        instance_tags['PixelSpacing'] = self.get_pixel_spacing()
        instance_tags['ImagePosition'] = self.get_image_position()
        instance_tags['ImageOrientation'] = self.get_image_orientation()
        instance_tags['RescaleSlope'] = self.get_rescale_slope()
        instance_tags['RescaleIntercept'] = self.get_rescale_intercept()
        instance_tags['SOPInstanceUID'] = self.get_SOPInstanceUID()
        return instance_tags

    def get_sop_class_uid(self):
        if 'SOPClassUID' in self.dicomData.dir() : return self.dicomData.SOPClassUID
        else : raise Exception('Undefined SOP Class UID')

    def get_radiopharmaceuticals_tags(self):
        radiopharmaceuticals_tags={}
        radiopharmaceutical_sequence = []

        try :
            radiopharmaceutical_sequence = self.dicomData[0x00540016][0]
        except Exception: 
            print("no Radiopharmaceuticals tags")

        for tag_address in TagsRadioPharmaceuticals:
            if tag_address.value in radiopharmaceutical_sequence : radiopharmaceuticals_tags[tag_address.name] = radiopharmaceutical_sequence[tag_address.value].value
            else : radiopharmaceuticals_tags[tag_address.name] = "Undefined"
            
        return radiopharmaceuticals_tags

    def get_pet_correction_tags(self):
        if TagPTCorrection.CorrectedImage.value in self.dicomData :
            return list(self.dicomData[TagPTCorrection.CorrectedImage.value].value)
        else: return "Undefined"


    def get_philips_private_tags(self):
        philips_tags={}
        for tag_address in PhilipsPrivateTags:
            if tag_address.value in self.dicomData : 
                philips_tags[tag_address.name] = float(self.dicomData[tag_address.value].value)
            else : philips_tags[tag_address.name] = "Undefined"
        return philips_tags

    def is_secondary_capture(self):
        return True if self.get_sop_class_uid in CapturesSOPClass else False

    def get_SOPInstanceUID(self):
        return self.dicomData[TagsInstance.SOPInstanceUID.value].value

    def get_rescale_slope(self):
        return self.dicomData[TagsInstance.RescaleSlope.value].value

    def get_rescale_intercept(self):
        return self.dicomData[TagsInstance.RescaleIntercept.value].value

    def get_image_orientation(self):
        return list(self.dicomData[TagsInstance.ImageOrientation.value].value)
    
    def get_image_position(self):
        return list(self.dicomData[TagsInstance.ImagePosition.value].value)

    def get_pixel_spacing(self):
        return list(self.dicomData[PixelSpacing.PixelSpacing.value].value)    
        

    def get_image_type(self):
        return list(self.dicomData[ImageType.ImageType.value].value)

    def is_image_modality(self):
        sop_values = set(item.value for item in ImageModalitiesSOPClass)
        return True if self.get_sop_class_uid() in sop_values else False

    def get_image_nparray(self):
        if self.is_image_modality() == False : 
            raise Exception('Not Image Modality')
        else:
            pixel_array = self.dicomData.pixel_array
            rescale_slope = self.get_rescale_slope()
            rescale_intercept = self.get_rescale_intercept()

            resultArray = ( pixel_array * rescale_slope) + rescale_intercept
            return resultArray
    

    def get_series_instance_uid(self):
        return self.dicomData[TagsSeries['SeriesInstanceUID'].value].value

    def get_number_rows(self):
        return self.dicomData.Rows

    def get_number_columns(self):
        return self.dicomData.Columns


    def get_acquisition_date(self):
        if "AcquisitionDate" in self.dicomData : 
            return self.dicomData.AcquisitionDate
        else : return "Undefined"
        

    def get_acquisition_time(self):
        if 'AcquisitionTime' in self.dicomData : 
            return self.dicomData.AcquisitionTime
        else : return "Undefined"


    #for RTSS Writer 
    #check si ces informations sont bien dans le dataset sinon erreur 

    def get_accession_number(self):
        return self.dicomData[TagsStudy['AccessionNumber'].value].value 

    def get_patient_name(self):
        return self.dicomData[TagsPatient['PatientName'].value].value

    def get_patient_id(self):
        return self.dicomData[TagsPatient['PatientID'].value].value

    def get_patient_birth_date(self):
        return self.dicomData[TagsPatient['PatientBirthDate'].value].value

    def get_patient_sex(self):
        return self.dicomData[TagsPatient['PatientSex'].value].value 

    def get_study_date(self):
        return self.dicomData[TagsStudy['StudyDate'].value].value

    def get_study_description(self):
        return self.dicomData[TagsStudy['StudyDescription'].value].value 

    def get_study_id(self):
        return self.dicomData[TagsStudy['StudyID'].value].value 

    def get_study_instance_uid(self):
        return self.dicomData[TagsStudy['StudyInstanceUID'].value].value

    def get_study_time(self):
        return self.dicomData[TagsStudy['StudyTime'].value].value

    def get_referring_physician_name(self):
        if "ReferringPhysisicianName" in self.dicomData : return self.dicomData.ReferringPhysicianName
        else : return "Undefined"

    def get_specific_character_set(self):
        if "SpecificCharacterSet" in self.dicomData : return self.dicomData.SpecificCharacterSet
        else : return "Undefined"

    def get_physicians_of_record(self):
        if "PhysiciansOfRecord" in self.dicomData : return self.dicomData.PhysiciansOfRecord
        else : return "Undefined"

    
    def get_frame_of_reference_uid(self):
        return self.dicomData.FrameOfReferenceUID 




        


    




    

    