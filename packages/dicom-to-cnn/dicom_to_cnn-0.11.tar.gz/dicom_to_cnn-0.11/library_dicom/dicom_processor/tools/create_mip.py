import os
import imageio
from os.path import basename,splitext
import scipy 
import numpy as np
import matplotlib.pyplot as plt

from scipy import ndimage
from PIL import Image
from fpdf import FPDF


def create_gif(filenames, duration, name, directory):
    """From a list of images, create gif

    Args:
        filenames ([list]): [list of all images' path]
        duration ([float]): [time of each image]
        name ([str]): [gif name]
        directory ([str]): [gif directory]


    """
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
        
    #name = splitext(basename(filenames[0][:-2]))[0]
    output_file = directory+'/' + name +'.gif'
    imageio.mimsave(output_file, images, duration=duration)
    
    return None

def mip_imshow(numpy_array, angle, type, cmap, vmin, vmax):
    """function to visualize MIP of 3D array 

    Args:
        numpy_array ([type]): [description]
        angle ([type]): [description]
        cmap ([type]): [description]
        type ([type]): [description]
        vmin ([type]): [description]
        vmax ([type]): [description]
    """
    numpy_array = np.transpose(np.flip(numpy_array, axis = 2), (2,1,0)) #coronal

    vol_angle = scipy.ndimage.interpolation.rotate(numpy_array , angle , reshape=False, axes = (1,2))
    MIP = np.amax(vol_angle,axis=2)

    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()
    if type == 'mask' : 
        plt.imshow(MIP, cmap = cmap)
        plt.show()
    else : 
        plt.imshow(MIP, cmap = cmap, vmin = vmin, vmax = vmax) #vmax = 3.0
        plt.show()

def mip_projection(numpy_array, angle, path_image, study_uid, type, cmap, vmin, vmax):
    """function to save MIP of 3D array 

    Args:
        numpy_array ([ndarray]): [PET or MASK 3D array]
        angle ([int]): [description]
        path_image ([str]): [description]
        study_uid ([str]): [description]
        type ([str]): ['pet' or 'mask']
        cmap ([str]): [description]
        vmin ([int]): [description]
        vmax ([int]): [description]

    Returns:
        save as png the MIP
    """
    numpy_array = np.transpose(np.flip(numpy_array, axis = 2), (2,1,0)) #coronal

    vol_angle = scipy.ndimage.interpolation.rotate(numpy_array , angle , reshape=False, axes = (1,2))
    MIP = np.amax(vol_angle,axis=2)

    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()
    if type == 'pet' :
        plt.imshow(MIP, cmap = cmap, vmin = vmin, vmax = vmax)
        filename = study_uid+'_mip_'+type+"_"+str(int(angle))+".png"

    else : 
        plt.imshow(MIP, cmap = cmap)
        filename = study_uid+'_mip_'+type+"_"+str(int(angle))+".png"

    #angle_filename = path_image+'\\'+study_uid+'mip'+"."+str(int(angle))+".png" #rajouter le study iud du patient ou numero de serie 
    angle_filename = os.path.join(path_image, filename)
    f.savefig(angle_filename, bbox_inches='tight')
    plt.close()   
    return angle_filename

def mip_imshow_4D(mask, angle, cmap) :
    """function to visualize MIP of 4D image

    Args:
        mask ([type]): [description]
        angle ([type]): [description]
        cmap ([type]): [description]
    """
    liste = []
    number_roi = mask.shape[3]
    for roi in range(number_roi): 
        #print(roi)
        #pour mettre en coronal 
        liste.append(np.transpose(np.flip(mask[:,:,:,roi], axis = 2), (2,1,0)))
    
    new_mask = np.stack((liste), axis = 3)
    vol_angle = scipy.ndimage.interpolation.rotate(new_mask , angle , reshape=False, axes = (2,3))
    MIP = np.amax(vol_angle,axis=3)
    MIP2 = np.amax(MIP,axis=2)

    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()

    plt.imshow(MIP2, cmap = cmap )
    



def mip_projection_4D(mask, angle, path_image, study_uid, number_roi, cmap):
    """function to save MIP of 4D array

    Args:
        mask ([ndarray]): [4D matrix]
        angle ([type]): [description]
        path_image ([type]): [description]
        study_uid ([type]): [description]
        number_roi ([type]): [description]
        cmap ([type]): [description]

    Returns:
        save as png the MIP image
    """

    mask_3d = np.amax(mask, axis = 3)



    numpy_array = np.transpose(np.flip(mask_3d, axis = 2), (2,1,0)) #coronal

    vol_angle = scipy.ndimage.interpolation.rotate(numpy_array , angle , reshape=False, axes = (1,2))
    MIP = np.amax(vol_angle,axis=2)

    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()

    plt.imshow(MIP, cmap = cmap)
    filename = study_uid+'mip_MASK'+"_"+str(int(angle))+".png"
    #angle_filename = path_image+'\\'+study_uid+'mip_MASK'+"."+str(int(angle))+".png" #rajouter le study iud du patient ou numero de serie 
    angle_filename = os.path.join(path_image, filename)
    f.savefig(angle_filename, bbox_inches='tight')
    plt.close()        
    return angle_filename
        

def create_pdf_mip(angle_filenames, output_path_name) : 
    """angle_filenames : [[path_mip_PET 1, path_mip_MASK 1, study_uid], [path_mip_PET 2, path_mip_MASK 2, study_uid],... ]

    """

    pdf = FPDF()
    for mip in angle_filenames : 
        pdf.add_page()
        pdf.image(mip[0], x = 0, y = 10, w = 100, h = 190)
        pdf.image(mip[1], x = 100, y = 10, w = 100, h = 190)
        pdf.set_font("Arial", size=12)
    
        pdf.cell(200, 0, txt= str(mip[2]), ln=2, align="C")

    pdf.output(output_path_name)

    return None 

   

def create_mip_gif(numpy_array, path_image, study_uid, type, cmap, borne_max):
    """return a gif of a numpy_array MIP 

    """
    duration = 0.1
    number_images = 60
    
    angle_filenames = []
    
    angles = np.linspace(0, 360, number_images)
    for angle in angles:
        path = mip_projection(numpy_array, angle, path_image, study_uid, type, cmap, borne_max = borne_max)
        angle_filenames.append(path)
              

    create_gif(angle_filenames, duration, path_image, name)

    for image in angle_filenames : 
        os.remove(image)
       
    
    return None 


def mip_superposition_show(mask_array, pet_array, angle, study_uid, vmin, vmax, cmap_pet, cmap_mask, alpha, save = False, directory = None):
    """Show and save as png PET/MASK MIP for one angle

    Args:
        mask_array ([ndarray]): [Mask ndarray 3D]
        pet_array ([ndarray]): [PET ndarray]
        angle ([int]): [angle]
        vmin ([int]): [minimum value]
        vmax ([int]): [maximum value]
        cmap_pet ([str]): [Mask pet]
        cmap_mask ([str]): [Mask cmap]
        save (bool, optional): [True if save the figure]. Defaults to False.
        directory ([str], optional): [Path of the directory]. Defaults to None.

    Returns:
        Save MIP in directory
    """
    mask_array = np.transpose(np.flip(mask_array, axis = 2), (2,1,0)) #coronal
    vol_angle_mask = scipy.ndimage.interpolation.rotate(mask_array , angle , reshape=False, axes = (1,2))
    MIP_mask = np.amax(vol_angle_mask,axis=2)

    pet_array = np.transpose(np.flip(pet_array, axis = 2), (2,1,0)) #coronal
    vol_angle_pet = scipy.ndimage.interpolation.rotate(pet_array , angle , reshape=False, axes = (1,2))
    MIP_pet = np.amax(vol_angle_pet,axis=2)

    f = plt.figure(figsize=(10,10))
    axes = plt.gca()
    axes.set_axis_off()
    plt.imshow(MIP_pet, vmin=vmin, vmax=vmax, cmap=cmap_pet)
    plt.imshow(np.where(MIP_mask, 0, np.nan), cmap=cmap_mask, alpha = alpha)

    if save == True : 
        filename = study_uid + '_PET_MASK'+"_"+str(int(angle))+".png"
        angle_filename = os.path.join(directory, filename)
        f.savefig(angle_filename, bbox_inches='tight')
        plt.close()
        return angle_filename



def mip_superposition_gif(mask_array, pet_array, vmin, vmax, cmap_pet, cmap_mask, directory, name):
    """Generate PET/MASK MIP gif 

    Args:
        mask_array ([ndarray]): [description]
        pet_array ([ndarray]): [description]
        vmin ([int]): [description]
        vmax ([int]): [description]
        cmap_pet ([str]): [description]
        cmap_mask ([str]): [description]
        directory ([str]): [description]
        name ([str]): [description]
    """
    duration = 0.1
    number_images = 60

    angles = np.linspace(0, 360, number_images)
    angles_filenames = []
    for angle in angles:
        angles_filenames.append(mip_superposition_show(mask_array, pet_array, angle, vmin, vmax, cmap_pet, cmap_mask, save = True, directory = directory))
        
    create_gif(angles_filenames, duration, name, directory)

    for image in angles_filenames : 
        os.remove(image)



