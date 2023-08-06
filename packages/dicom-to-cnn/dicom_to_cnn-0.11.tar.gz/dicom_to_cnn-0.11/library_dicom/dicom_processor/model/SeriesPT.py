from library_dicom.dicom_processor.model.Series import Series
from library_dicom.dicom_processor.model.reader.Instance import Instance 
import os 
from math import exp, log, pow
from datetime import datetime, timedelta

class SeriesPT(Series):
    """Specific methods to read PET series
    Store radiopharmaceutical data
    Check Attenuation conrrection
    SUV / SUL calculation
    Get Series as 32bits Nifti SUV/SUL
    

    Arguments:
        Series {[class]} -- [description]
    """

    def __init__(self, path, sul_value=False):
        """Constructor

        Arguments:
            path {String} -- Path folder of series

        Keyword Arguments:
            sul_value {bool} -- [If true return NIFTI SUL] (default: {False})
        """
        super().__init__(path)
        self.sul_value=sul_value




    def get_minimum_acquisition_datetime(self):
        """Get earlier acquisition datetime of the PET serie

        Returns : 
            [datetime] -- [Return the earlier acquisition datetime, or "Undefined" if no acquisition_time or no acquisition date]
        """
        liste = []
        try : 
            for filename in self.file_names : 
                instanceData = Instance(os.path.join(self.path,filename), load_image=True)
                datetime = instanceData.get_acquisition_date() + instanceData.get_acquisition_time()
                parsed_datetime = self.__parse_datetime(datetime)
                liste.append(parsed_datetime)

            return min(liste)

        except Exception : 
            return "Undefined"
        


    def get_series_details(self):
        """Add Pharmaceuticals data to common series details

        Returns:
            [dict] -- [Return the details of a SeriePT from the first Dicom]
        """
        details = super().get_series_details()
        dicomInstance = self.get_first_instance_metadata()
        self.radiopharmaceutical_details = {}
        self.radiopharmaceutical_details = dicomInstance.get_radiopharmaceuticals_tags()
        details['radiopharmaceutical'] = self.radiopharmaceutical_details
        self.pet_correction_details = {}
        self.pet_correction_details = dicomInstance.get_pet_correction_tags()
        details['pet_correction'] = self.pet_correction_details
        self.philips_tag = {}
        self.philips_tag = dicomInstance.get_philips_private_tags()
        details['philips_tags'] = self.philips_tag

        return details
        

    @classmethod
    def __parse_datetime(cls, date_time):
        """ class method to parse datetime

        Returns : 
        [datetime] -- [Return parse datetime]
        """
        #remove microsecond at it is inconstant over dicom
        if '.' in date_time : 
            date_time = date_time[0 : date_time.index('.')]
        #parse datetime to date objet
        return datetime.strptime(date_time, "%Y%m%d%H%M%S")



    def __calculateSUVFactor(self):
        """
        Calcul of  SUV factor

        Returns:
            [float] -- [return SUV factor or "Calcul SUV impossible" if there is "Undefined" value in tags]
        """
        series_details = self.get_series_details()
        units = series_details['series']['Units']
    
        known_units = ['GML', 'BQML', 'CNTS']
        if units not in known_units : 
            raise Exception ('Unknown PET Units')

        if units == 'GML' : return 1
        elif units == 'CNTS' :
            philips_suv_bqml = series_details['philips_tags']['PhilipsBqMlFactor']
            philips_suv_factor = series_details['philips_tags']['PhilipsSUVFactor']
            if (philips_suv_factor != 'Undefined') : return philips_suv_factor
            if (philips_suv_factor == 'Undefined' and philips_suv_bqml == 'Undefined') : raise Exception('Missing Philips private Factors')
        
        patient_weight = series_details['study']['PatientWeight'] * 1000 #kg to g conversion
        
        series_time = series_details['series']['SeriesTime']
        series_date = series_details['series']['SeriesDate']
        series_datetime = series_date + series_time 

        series_datetime = self.__parse_datetime(series_datetime)
        acquisition_datetime = self.get_minimum_acquisition_datetime()
        acquisition_date = series_details['series']['AcquisitionDate']
        
        decay_correction = series_details['series']['DecayCorrection']
        radionuclide_half_life = series_details['radiopharmaceutical']['RadionuclideHalfLife']
        total_dose = series_details['radiopharmaceutical']['TotalDose']

        radiopharmaceutical_start_date_time = series_details['radiopharmaceutical']['RadiopharmaceuticalStartDateTime']

        
        if radiopharmaceutical_start_date_time == 'Undefined' or radiopharmaceutical_start_date_time == '' : 
            #If startDateTime not available use the deprecated statTime assuming the injection is same day than acquisition date
            radiopharmaceutical_start_time = series_details['radiopharmaceutical']['RadiopharmaceuticalStartTime']
            radiopharmaceutical_start_date_time = acquisition_date + radiopharmaceutical_start_time 
            
        
        radiopharmaceutical_start_date_time = self.__parse_datetime(radiopharmaceutical_start_date_time)
        
        if (total_dose == 'Undefined' or total_dose == None or  acquisition_datetime== 'Undefined' 
            or patient_weight == 'Undefined' or patient_weight == 'None' or radionuclide_half_life == 'Undefined' ) :
            raise Exception('Missing Radiopharmaceutical data or patient weight')
        
        #Determine Time reference of image acqusition 
        acquisition_hour = series_datetime
        if (acquisition_datetime != 'Undefined'
             and (acquisition_datetime - series_datetime).total_seconds() < 0 and units == 'BQML') : 
            acquisition_hour = acquisition_datetime

        
        #Calculate decay correction
        if decay_correction == 'START' : 
            delta = (acquisition_hour - radiopharmaceutical_start_date_time)
            delta = delta.total_seconds()
            if (delta < 0) : raise("Acqusition time before injection time")
            decay_factor = exp(-delta * log(2) / radionuclide_half_life)

        #If decay corrected from administration time no decay correction to apply
        elif decay_correction == 'ADMIN' : 
            decay_factor = 1


        else : raise Exception('Unknown Decay Correction methode')
        
        suv_conversion_factor = 1/((total_dose * decay_factor) / patient_weight)
        
        if units == 'CNTS' : return philips_suv_bqml * suv_conversion_factor
        else : return suv_conversion_factor


    def calculateSULFactor(self):
        """Calcul SUL Factor

        Returns:
            [float] -- [Return SUL Factor or "Calcul SUL impossible" if there is "Undefined" value in tags]
        """
        series_details = self.get_series_details()
        patient_sex = series_details['patient']['PatientSex']
        patient_weight = series_details['study']['PatientWeight']
        patient_height = series_details['study']['PatientHeight']
        if (patient_sex == 'Undefined' or patient_height == 'Undefined' or patient_weight == 'Undefined' or patient_height == 0.0) : 
            raise Exception('Missing Height or Weight to calculate SUL')
        bmi =  patient_weight / pow(patient_height, 2)
        if patient_sex == 'F' :
            return 9270 / (8780 + 244 * bmi)
        elif patient_sex == 'M':
            return 9270 / (6680 + 216 * bmi)
        else :
            raise Exception('Unknown Sex String')
    

    def is_corrected_attenuation(self):
        """If PET Series is attenuation corrected

        Returns:
            [bool] -- [True if attenuation corrected]
        """
        series_details = self.get_series_details()
        corrected_image = series_details['pet_correction']
        if 'ATTN' in corrected_image : return True
        else : return False


    
    def get_numpy_array(self):
        """[summary]

        Returns:
            [array] -- [return array of the SeriesPT with SUV and SUL factor in 32bis npArray ]
        """
        numpy_array = super().get_numpy_array()
        try:
            if (self.sul_value == False) :
                return numpy_array * self.__calculateSUVFactor()
            else :
                return numpy_array * self.__calculateSUVFactor() * self.calculateSULFactor()
        except Exception as err:
            print("Error generating result array", err)