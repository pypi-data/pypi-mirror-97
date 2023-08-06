from library_dicom.dicom_processor.model.Series import Series
from library_dicom.dicom_processor.model.reader.Instance import Instance
import pydicom
import os
import cv2 as cv2
import numpy as np 
import sys 



class Instance_RTSS(Instance):
    """Class to read dicom RT file and build mask 
    """

    def __init__(self, path_rtss):
        super().__init__(path_rtss, load_image=True)


    def get_image_nparray(self):
        sys.exit('Cannot get image numpy array from RTSTRUCT FILE')


    def get_list_all_SOP_Instance_UID_RTSS(self):
        number_item = len(self.dicomData[0x30060010][0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence)
        liste = []
        for i in range(number_item):
            liste.append(str(self.dicomData[0x30060010][0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence[i].ReferencedSOPInstanceUID))
        
        return liste



    def get_number_of_roi(self):
        return len(self.dicomData.StructureSetROISequence)


    #info from ReferencedFrameOfReferenceSequence
    def get_number_of_referenced_series(self):
        """return number of series in ReferencedFrameOfReferencedSequence

        """
        return len(self.dicomData.ReferencedFrameOfReferenceSequence)


    def get_frame_of_reference_uid(self):
        #Doit etre le meme que FrameOfReferenceUID de la serie CT/PT
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].FrameOfReferenceUID)

        return liste #les mêmes pour les 2 series 



    def is_frame_of_reference_same(self):
        """check if frame of reference is the same for the series in ReferencedOfReferencedSequence

        """
        frame_of_reference_UID = self.get_frame_of_reference_uid()
        for i in range(len(frame_of_reference_UID)):
            if frame_of_reference_UID[0] != frame_of_reference_UID[i] :
                return False 
        return True 


    def get_referenced_series_instance_uid(self):
        #doit être le même que SeriesInstanceUID de la CT/PT
        """get series instance UID from the CT/PT serie 


        """
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].SeriesInstanceUID)
        return liste


    def get_referenced_study_SOP_instance_uid(self):
        #Doit etre le meme que la StudyInstanceUID de la CT/PT + meme que StudyInstanceUID du RTSS
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].ReferencedSOPInstanceUID)
        return liste


    def get_referenced_SOP_class_UID(self):
        #Doit etre le meme que SOPClassUID de la serie CT/PT
        number_serie = len(self.dicomData.ReferencedFrameOfReferenceSequence)
        liste = []
        for i in range(number_serie):
            liste.append(self.dicomData[0x30060010][i].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].ContourImageSequence[0].ReferencedSOPClassUID)
        return liste 

 
    #info from StructureSetROISequence
    def get_ROI_name(self, number_roi):
        return self.dicomData[0x30060020][number_roi - 1].ROIName 

    def get_ROI_volume(self, number_roi):
        return self.dicomData[0x30060020][number_roi - 1].ROIVolume 

    def get_ROI_generation_algorithm(self, number_roi):
        return self.dicomData[0x30060020][number_roi - 1].ROIGenerationAlgorithm 

    #info from ROIContourSequence

    def get_roi_display_color(self, number_roi):
        return self.dicomData[0x30060039][number_roi - 1].ROIDisplayColor 


    def get_list_referenced_SOP_Instance_UID(self, roi_number): #la ou il y a les contours
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(str(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourImageSequence[0].ReferencedSOPInstanceUID))
        return liste 

    
    def is_referenced_SOP_Instance_UID_in_all_SOP_Instance(self):
        """check if slices in which there is a ROI is in the list of all slices of the serie

        """
        all_sop = str(self.get_list_all_SOP_Instance_UID_RTSS)
        referenced_sop = str(self.get_list_referenced_SOP_Instance_UID)
        for uid in referenced_sop : 
            if uid not in all_sop : 
                raise Exception("SOP Instance UID not in the serie")
        return True 


    def get_number_of_contour_points(self, roi_number):
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].NumberOfContourPoints)
        return liste

    def get_list_contour_geometric_type(self, roi_number):
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourGeometricType)
        return liste

    def is_closed_planar(self, roi_number):
        geometric_type = self.get_list_contour_geometric_type(roi_number)
        for type in geometric_type :
            if type != "CLOSED_PLANAR" : 
                return False
        return True 


    def get_contour_data(self, roi_number):
        number_item = len(self.dicomData[0x30060039][roi_number - 1].ContourSequence)
        liste = []
        for i in range(number_item):
            liste.append(self.dicomData[0x30060039][roi_number - 1].ContourSequence[i].ContourData)
        return liste #liste d'array 


 