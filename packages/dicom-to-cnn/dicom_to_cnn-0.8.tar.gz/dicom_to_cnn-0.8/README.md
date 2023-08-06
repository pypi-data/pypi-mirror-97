# library-DICOM

Features : 
- Description of Series content in a huge dataset of DICOM (output JSON descriptor for each series containings main DICOM tags).
- Conversion Dicom to Nifti
- PET : Conversion Bqml/Counts to SUV and SUL

Roadmap : 
- Read RTSS to generate Mask
- Generate RTSS from Mask
- PT / CT fusion in 4D array np array

#Maintainer  : Salim Kanoun
#Contributors : Thomas Trouillard, Wendy Revailler



To refactor : 
- conversion of a nifti mask to a ROI in a DICOM RTSTRUCT
- ROI integration to an existing RTSTRUCT
- generation empty RTSTRUCT from PET,CT or similar set of DICOM images

**TODO :** 
- conversion DICOM RTSTRUCT to mask in nifti format
