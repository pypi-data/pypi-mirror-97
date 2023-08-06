from library_dicom.dicom_processor.model.Series import Series
from library_dicom.dicom_processor.model.reader.Instance import Instance
from library_dicom.dicom_processor.model.reader.Instance_RTSS import Instance_RTSS
import pydicom
import os
import cv2 as cv2
import numpy as np 
import sys 


class MaskBuilder_RTSS : 

    def __init__(self, rtss_path, serie_path):

        self.serie = Series(serie_path)
        self.serie_data = self.serie.get_series_details()
        self.instance_uid_serie = self.serie.get_all_SOPInstanceIUD()
        self.matrix_size = self.serie.get_size_matrix()
        instances = self.serie.get_instances_ordered()
        
        self.image_position = instances[-1].get_image_position()
        self.pixel_spacing = instances[-1].get_pixel_spacing()
        self.pixel_spacing.append(self.serie.get_z_spacing())

        #print(self.image_position)
        #print(self.pixel_spacing)

        self.rtss = Instance_RTSS(rtss_path)
        self.number_of_roi = self.rtss.get_number_of_roi()



    def get_list_all_SOP_Instance_UID_serie(self):
        return self.instance_uid_serie

    

    def is_sop_instance_uid_same(self):
        uid_serie = self.get_list_all_SOP_Instance_UID_serie()
        uid_rtss = self.rtss.get_list_all_SOP_Instance_UID_RTSS()
        for uid in uid_rtss : 
            if uid not in uid_serie : 
                return False

        return True

    """
    def get_image_position(self):
        #print("origin : ", self.serie_data['instance']['ImagePosition'] )
        return self.serie_data['instance']['ImagePosition']

    def get_pixel_spacing(self):
        pixel_spacing =  self.serie_data['instance']['PixelSpacing']
        instances = self.serie.get_instances_ordered()
        pixel_spacing.append(self.serie.get_z_spacing())
        for i in range(len(instances)):
            print(instances[i].get_image_position())
        return pixel_spacing
    """ 


    def __spatial_to_pixels(self, matrix_size, number_roi, list_all_SOPInstanceUID):
        """Transform contour data in spatial to contour data in pixels, return a dict 


        Returns:
            [dict] -- [{1 : { x : []
                               y : []
                               z : []} , 
                       {2 : { x : []
                               y : []
                               z : []} , ...]
        """
        #frame_of_reference_UID = self.get_frame_of_reference_UID()

        #pixel_spacing = self.get_pixel_spacing()
        #image_position = self.get_image_position()

        #list_referenced_SOP_instance_uid = self.rtss.get_list_referenced_SOP_Instance_UID(number_roi)
        
        list_contour_data = self.rtss.get_contour_data(number_roi) #x y z en mm 
        list_pixels = {}
        for i in range(3):
            self.image_position[i] = float(self.image_position[i])

        for contour_data in (list_contour_data):
            number_item = list_contour_data.index(contour_data) #0 1 2 3 ...
            contour_item = {}
            x = contour_data[::3]  #list
            x = [int((i - self.image_position[0]) / self.pixel_spacing[0] ) for i in x ] 

            contour_item['x'] = x
            y = contour_data[1::3] #list
            y = [int((i - self.image_position[1]) / self.pixel_spacing[1] )  for i in y ] 
            contour_item['y'] = y

            z = contour_data[2::3]
            z = [int((i - self.image_position[2]) / self.pixel_spacing[2] ) for i in z ][0]
            #z = list_referenced_SOP_instance_uid[number_item]
            #z = list_all_SOPInstanceUID.index(z) #numero de coupe correspondant
            contour_item['z'] = z
            list_pixels[number_item + 1] = contour_item

        return list_pixels

    #eventuellement en privé
    def get_list_points(self, matrix_size, number_roi, list_all_SOPInstanceUID):
        """transform a list of pixels of a ROI to a list nx2 (n points, coordonate (x,y)) for each contour

        Arguments:
          

        Returns:
            [list] -- list of (x,y) points and list of z slices in which there is a contour
        """
        pixels = self.__spatial_to_pixels(matrix_size, number_roi, list_all_SOPInstanceUID) #dict 
        number_item = len(pixels)
        list_points = []
        slice = []
        for item in range(number_item):
            subliste = []
            list_x = (pixels[item + 1]['x'])
            list_y = (pixels[item + 1]['y'])
            for x,y in zip(list_x, list_y):
                subliste.append([x,y])

            list_points.append(subliste)

            slice.append(pixels[item + 1]['z'])

        return list_points, slice 

  
    def rtss_to_3D_mask(self, number_roi, matrix_size, list_all_SOPInstanceUID):
        number_of_slices = matrix_size[2]
        np_array_3D = np.zeros(( matrix_size[0],  matrix_size[1], number_of_slices)).astype(np.uint8)
        if self.rtss.is_closed_planar(number_roi) == False : raise Exception ("Not CLOSED_PLANAR contour")
        liste_points, slice = self.get_list_points(matrix_size, number_roi, list_all_SOPInstanceUID )
        #print(slice)
        for item in range(len(slice)):
            np_array_3D[:,:,slice[item]] = cv2.drawContours(np.float32(np_array_3D[:,:,slice[item]]), [np.asarray(liste_points[item])], -1, number_roi , -1)

        return np_array_3D.astype(np.uint8)


    def rtss_to_4D_mask(self):
        matrix_size = self.matrix_size
        list_all_SOPInstanceUID = self.rtss.get_list_all_SOP_Instance_UID_RTSS()
        np_array_3D = []
        for number_roi in range(1, self.number_of_roi +1):
            np_array_3D.append(self.rtss_to_3D_mask(number_roi, matrix_size, list_all_SOPInstanceUID))
        np_array_4D = np.stack((np_array_3D), axis = 3)

        return np_array_4D.astype(np.uint8)