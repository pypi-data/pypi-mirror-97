from library_dicom.dicom_processor.model.Fusion import Fusion 
import SimpleITK as sitk 

class FusionMask(Fusion):
    """ReshapeResampleAlign CT/PET with MASK 
    If 'dict' or 'img'. Missing 'serie' option ! 

    Args:
        Fusion ([type]): [description]
    """
    def __init__(self, pet, mask, target_size=None, target_spacing=None, target_direction=None, mode = 'dict'):
        #super().__init__()
        self.pet_objet = pet
        self.mask_object = mask
        self.target_size = target_size
        self.target_spacing = target_spacing
        self.target_direction = target_direction
        self.mode = mode


    def resample(self, array = False): 
        _, mask_img = self.generate_pet_ct_img()
        target_spacing, target_direction, target_origin, target_size = self.get_feature_pet_img()
        _, _, _, mask_size = self.get_feature_ct_img()
        
        if len(mask_size) == 3 : 
            transformation = sitk.ResampleImageFilter()
            transformation.SetOutputDirection(target_direction)
            transformation.SetOutputOrigin(target_origin)
            transformation.SetOutputSpacing(target_spacing)
            transformation.SetSize(target_size)
            transformation.SetDefaultPixelValue(0.0)
            transformation.SetInterpolator(sitk.sitkNearestNeighbor)
            img = transformation.Execute(mask_img)

        
        else : #mask 4D => mask 4D
            liste = []
            for roi in range(mask_size[3]):
                extract = sitk.ExtractImageFilter()
                extract.setSize([mask_size[0], mask_size[1], mask_size[2], 0])
                extract.setIndex([0,0,0,roi])
                extracted_img = extract.Execute(mask_img)
                transformation = sitk.ResampleImageFilter()
                transformation.SetOutputDirection(target_direction)
                transformation.SetOutputOrigin(target_origin)
                transformation.SetOutputSpacing(target_spacing)
                transformation.SetSize(target_size)
                transformation.SetDefaultPixelValue(0.0)
                transformation.SetInterpolator(sitk.sitkNearestNeighbor)
                new_mask_img = transformation.Execute(extracted_img)
                liste.append(new_mask_img)

            img = sitk.JoinSeries(liste)


        if array==True : 
            mask_array = sitk.GetArrayFromImage(img)
            return mask_array 

        return img

