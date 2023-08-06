from enum import Enum

class CapturesSOPClass(Enum):

    SecondaryCaptureImageStorage = '1.2.840.10008.5.1.4.1.1.7'
    MultiframeSingleBitSecondaryCaptureImageStorage = '1.2.840.10008.5.1.4.1.1.7.1'
    MultiframeGrayscaleByteSecondaryCaptureImageStorage	= '1.2.840.10008.5.1.4.1.1.7.2'
    MultiframeGrayscaleWordSecondaryCaptureImageStorage = '1.2.840.10008.5.1.4.1.1.7.3'	
    MultiframeTrueColorSecondaryCaptureImageStorage = '1.2.840.10008.5.1.4.1.1.7.4'

class ImageModalitiesSOPClass(Enum):

    CT = '1.2.840.10008.5.1.4.1.1.2'
    EnhancedCT = '1.2.840.10008.5.1.4.1.1.2.1'
    PT = '1.2.840.10008.5.1.4.1.1.128'
    EnhancedPT = '1.2.840.10008.5.1.4.1.1.130'
    NM = '1.2.840.10008.5.1.4.1.1.20'
    MR = '1.2.840.10008.5.1.4.1.1.4'
    EnhancedMR = '1.2.840.10008.5.1.4.1.1.4.1'
    MRSpectroscopy = '1.2.840.10008.5.1.4.1.1.4.2'
    RTSTRUCT = '1.2.840.10008.5.1.4.1.1.481.3'


class RTModalitiesSOPClass(Enum):

    RTSS = '1.2.840.10008.5.1.4.1.1.481.3',
    RTDose = '1.2.840.10008.5.1.4.1.1.481.2'