from enum import Enum

class TagsPatient(Enum):
    """Patient related dicom tags

    Arguments:
        Enum {hex} -- [Tag address]
    """

    PatientName = 0x00100010
    PatientID = 0x00100020
    PatientBirthDate = 0x00100030
    PatientSex = 0x00100040

class TagsStudy(Enum):
    """Study related tags

    Arguments:
        Enum {hex} -- [Tag address]
    """

    AccessionNumber = 0x00080050
    InstitutionName = 0x0080080
    StudyDate = 0x00080020
    StudyTime = 0x00080030
    StudyDescription = 0x00081030
    StudyID = 0x00200010
    StudyInstanceUID = 0x0020000D
    PatientWeight = 0x00101030
    PatientHeight = 0x00101020

class TagsSeries(Enum):
    """Series related dicom tags

    Arguments:
        Enum {hex} -- [Tag address]
    """
    Manufacturer = 0x00080070
    Modality = 0x00080060
    SeriesDate = 0x00080021
    SeriesTime = 0x00080031
    SeriesDescription = 0x0008103E
    SeriesInstanceUID = 0x0020000E
    SeriesNumber = 0x00200011
    AcquisitionDate = 0x00080022
    AcquisitionTime = 0x00080032
    NumberOfSlices = 0x00540081
    ImageInAcquisition = 0x00201002
    Units = 0x00541001
    DecayCorrection = 0x00541102

class PhilipsPrivateTags(Enum):
    PhilipsSUVFactor = 0x70531000
    PhilipsBqMlFactor = 0x70531009

class TagPTCorrection(Enum):
    CorrectedImage = 0x00280051

class ImageType(Enum):
    ImageType = 0x00080008

class PixelSpacing(Enum):
    PixelSpacing = 0x00280030


class TagsInstance(Enum):
    """Instance related tags

    Arguments:
        Enum {hex} -- [tag address]
    """

    ImagePosition = 0x00200032
    ImageOrientation = 0x00200037
    RescaleSlope = 0x00281053
    RescaleIntercept = 0x00281052
    SOPInstanceUID = 0x00080018

class TagsRadioPharmaceuticals(Enum):
    """Tags related to Radiopharmaceuticals injection

    Arguments:
        Enum {hex} -- [tag address]
    """

    RadionuclideHalfLife = 0x00181075
    TotalDose = 0x00181074
    RadiopharmaceuticalStartDateTime = 0x00181078
    RadiopharmaceuticalStartTime = 0x00181072