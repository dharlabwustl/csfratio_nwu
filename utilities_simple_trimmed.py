#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Timporthu Mar 12 15:40:53 2020

@author: atul
"""
import subprocess,os,sys,glob,datetime
import csv
import pandas as pd
import numpy as np
import cv2
import nibabel as nib
from skimage import exposure 
import smtplib,math
# import matplotlib.pyplot as plt
def demo():
    print(" i m in demo")
# def histogram_sidebyside(infarct_data,noninfarct_data,image_filename):
    
#     dflux = pd.DataFrame(dict(INFARCT=infarct_data))
#     dflux2 = pd.DataFrame(dict(NONINFARCT=noninfarct_data))

#     fig, axes = plt.subplots(1, 2)

#     dflux.hist('INFARCT', bins=255, ax=axes[0])
#     dflux2.hist('NONINFARCT', bins=255, ax=axes[1])
#     fig.savefig(image_filename)

def coninuous2binary0_255(coninuous_image_file):
    coninuous_image_file_nib=nib.load(coninuous_image_file)
    coninuous_image_file_nib_data=coninuous_image_file_nib.dataobj.get_unscaled() #""
    coninuous_image_file_nib_data[coninuous_image_file_nib_data>0]=255
    array_mask = nib.Nifti1Image(coninuous_image_file_nib_data, affine=coninuous_image_file_nib.affine, header=coninuous_image_file_nib.header)
    # niigzfilenametosave2=os.path.join(OUTPUT_DIRECTORY,os.path.basename(levelset_file)) #.split(".nii")[0]+"RESIZED.nii.gz")
    nib.save(array_mask, coninuous_image_file)





def whenOFsize512x512(levelset_file,OUTPUT_DIRECTORY):
    if "WUSTL" in levelset_file:
        image_levelset_nib=nib.load(levelset_file)
        image_levelset_data=image_levelset_nib.dataobj.get_unscaled()
        flipped_mask=np.copy(image_levelset_data)
        for idx in range(image_levelset_data.shape[2]):
            flipped_mask[:,:,idx]=cv2.flip(image_levelset_data[:,:,idx],0)
        array_mask = nib.Nifti1Image(flipped_mask, affine=image_levelset_nib.affine, header=image_levelset_nib.header)
        niigzfilenametosave2=os.path.join(OUTPUT_DIRECTORY,os.path.basename(levelset_file)) #.split(".nii")[0]+"RESIZED.nii.gz")
        nib.save(array_mask, niigzfilenametosave2)
    else:
        command= "cp  " + levelset_file + "  " + os.path.join(OUTPUT_DIRECTORY,os.path.basename(levelset_file))
        subprocess.call(command, shell=True)
    return "X"

def whenOFsize512x512_new(levelset_file,original_file,OUTPUT_DIRECTORY):
#     if "WUSTL" in levelset_file:
    original_file_nib=nib.load(original_file)
    image_levelset_nib=nib.load(levelset_file)
    image_levelset_data1=image_levelset_nib.dataobj.get_unscaled()
#         flipped_mask=np.copy(image_levelset_data)
#         for idx in range(image_levelset_data.shape[2]):
#             flipped_mask[:,:,idx]=cv2.flip(image_levelset_data[:,:,idx],0)
#         array_mask = nib.Nifti1Image(flipped_mask, affine=image_levelset_nib.affine, header=image_levelset_nib.header)
#         niigzfilenametosave2=os.path.join(OUTPUT_DIRECTORY,os.path.basename(levelset_file)) #.split(".nii")[0]+"RESIZED.nii.gz")
#         nib.save(array_mask, niigzfilenametosave2)
#     else:
    print("I am in whenOFsize512x512_new()")
    array_mask = nib.Nifti1Image(image_levelset_data1, affine=original_file_nib.affine, header=original_file_nib.header)
    niigzfilenametosave2=os.path.join(OUTPUT_DIRECTORY,os.path.basename(levelset_file)) #.split(".nii")[0]+"RESIZED.nii.gz")
    nib.save(array_mask, niigzfilenametosave2)
    
    
#     command= "cp  " + levelset_file + "  " + os.path.join(OUTPUT_DIRECTORY,os.path.basename(levelset_file))
#     subprocess.call(command, shell=True)
    return "X"

def whenOFsize512x5xx(original_file,levelset_file,OUTPUT_DIRECTORY="./"):
    image_nib_nii_file=nib.load(original_file)  #,header=False)
    image_nib_nii_file_data=image_nib_nii_file.get_fdata() #
    image_levelset_data=nib.load(levelset_file).dataobj.get_unscaled()
    array_mask1=nib.load(levelset_file)
    if image_nib_nii_file.get_fdata().shape[1]>512 : #image_levelset_data.shape[1]:
#    print("a")
        print("ORIGINAL IMAGE SIZE")
        print(image_nib_nii_file.get_fdata().shape)
        print("YES DIFFER")
        # print(imagefile_levelset)
#    npad = ((0, 0), (difference_size//2, difference_size//2), (0, 0))
        size_diff=(image_nib_nii_file.get_fdata().shape[1]-512)
        if (size_diff % 2 )== 0 : 
            size_diff=int(size_diff/2)
            npad = ((0, 0), (size_diff-1, size_diff+1), (0, 0)) 
        else :
            size_diff=int(size_diff/2)
            npad = ((0, 0), (size_diff, size_diff+1), (0, 0))  #abs(np.min(image_levelset_data)
        image_levelset_data1=np.pad(image_levelset_data, pad_width=npad, mode='constant', constant_values=np.min(image_levelset_data)) #image_nib_nii_file_data[0:image_nib_nii_file_data.shape[0],0+(difference_size//2):image_nib_nii_file_data.shape[1]-(difference_size//2),0:image_nib_nii_file_data.shape[2]]
        if "WUSTL" in levelset_file:
            flipped_mask=np.copy(image_levelset_data1)
            for idx in range(image_levelset_data1.shape[2]):
                flipped_mask[:,:,idx]=cv2.flip(image_levelset_data1[:,:,idx],0)

                image_levelset_data1=np.copy(flipped_mask)
        array_mask = nib.Nifti1Image(image_levelset_data1, affine=image_nib_nii_file.affine, header=image_nib_nii_file.header)
        niigzfilenametosave2=os.path.join(OUTPUT_DIRECTORY,os.path.basename(levelset_file)) #.split(".nii")[0]+"RESIZED.nii.gz")
        nib.save(array_mask, niigzfilenametosave2)
        # array_mask1=nib.load(niigzfilenametosave2)

    return "X"
def whenOFsize512x5xx_new(original_file,levelset_file,OUTPUT_DIRECTORY="./"):
    image_nib_nii_file=nib.load(original_file)  #,header=False)
    image_nib_nii_file_data=image_nib_nii_file.get_fdata() #
    image_levelset_data=nib.load(levelset_file).dataobj.get_unscaled()
    array_mask1=nib.load(levelset_file)
    if image_nib_nii_file.get_fdata().shape[1]>512 : #image_levelset_data.shape[1]:
#    print("a")
        print("I am in whenOFsize512x5xx_new()")
        print("ORIGINAL IMAGE SIZE")
        print(image_nib_nii_file.get_fdata().shape)
        print("YES DIFFER")
        # print(imagefile_levelset)
#    npad = ((0, 0), (difference_size//2, difference_size//2), (0, 0))
        size_diff=(image_nib_nii_file.get_fdata().shape[1]-512)
        if (size_diff % 2 )== 0 : 
            size_diff=int(size_diff/2)
            npad = ((0, 0), (size_diff-1, size_diff+1), (0, 0)) 
        else :
            size_diff=int(size_diff/2)
            npad = ((0, 0), (size_diff, size_diff+1), (0, 0))  #abs(np.min(image_levelset_data)
        image_levelset_data1=np.pad(image_levelset_data, pad_width=npad, mode='constant', constant_values=np.min(image_levelset_data)) #image_nib_nii_file_data[0:image_nib_nii_file_data.shape[0],0+(difference_size//2):image_nib_nii_file_data.shape[1]-(difference_size//2),0:image_nib_nii_file_data.shape[2]]
#         if "WUSTL" in levelset_file:
#             flipped_mask=np.copy(image_levelset_data1)
#             for idx in range(image_levelset_data1.shape[2]):
#                 flipped_mask[:,:,idx]=cv2.flip(image_levelset_data1[:,:,idx],0)

#                 image_levelset_data1=np.copy(flipped_mask)
        array_mask = nib.Nifti1Image(image_levelset_data1, affine=image_nib_nii_file.affine, header=image_nib_nii_file.header)
        niigzfilenametosave2=os.path.join(OUTPUT_DIRECTORY,os.path.basename(levelset_file)) #.split(".nii")[0]+"RESIZED.nii.gz")
        nib.save(array_mask, niigzfilenametosave2)
        # array_mask1=nib.load(niigzfilenametosave2)

    return "X"

def levelset2originalRF() : #original_file,levelset_file,OUTPUT_DIRECTORY="./"):
    original_file=sys.argv[1]
    levelset_file=sys.argv[2]
    OUTPUT_DIRECTORY=sys.argv[3]
    original_file_nib=nib.load(original_file)
    original_file_nib_data=original_file_nib.get_fdata()
    if original_file_nib_data.shape[1] == 512 :
        whenOFsize512x512(levelset_file,OUTPUT_DIRECTORY)
    else:
        whenOFsize512x5xx(original_file,levelset_file,OUTPUT_DIRECTORY)

def levelset2originalRF_new() : #original_file,levelset_file,OUTPUT_DIRECTORY="./"):
#     print(sys.argv[1])

    original_file=sys.argv[1]
    levelset_file=sys.argv[2]
    OUTPUT_DIRECTORY=sys.argv[3]
    original_file_nib=nib.load(original_file)

    original_file_nib_data=original_file_nib.get_fdata()
    print("For the file {}".format(levelset_file))
    print("I am in levelset2originalRF_new()")
    if original_file_nib_data.shape[1] == 512 :
        whenOFsize512x512_new(levelset_file,original_file,OUTPUT_DIRECTORY)
    else:
        whenOFsize512x5xx_new(original_file,levelset_file,OUTPUT_DIRECTORY)

def hdr2niigz() : #,headerfiledata): hdrfilename,niigzfilenametosave 
    filenameniigz=sys.argv[1]
    original_grayfile=sys.argv[2]
    original_grayfile_nib=nib.load(original_grayfile)
    niigzfilenametosave=sys.argv[3]
    # hdrfilename
    analyzedata=nib.AnalyzeImage.from_filename(filenameniigz)
    array_img = nib.Nifti1Image(analyzedata.dataobj.get_unscaled(), affine=original_grayfile_nib.affine, header=original_grayfile_nib.header)
    nib.save(array_img, niigzfilenametosave)

    
def hdr2niigz_py(filenameniigz,original_grayfile,niigzfilenametosave) : #,headerfiledata): hdrfilename,niigzfilenametosave 
#     filenameniigz=sys.argv[1]
#     original_grayfile=sys.argv[2]
    original_grayfile_nib=nib.load(original_grayfile)
#     niigzfilenametosave=sys.argv[3]
    # hdrfilename
    analyzedata=nib.AnalyzeImage.from_filename(filenameniigz)
    array_img = nib.Nifti1Image(analyzedata.dataobj.get_unscaled(), affine=original_grayfile_nib.affine, header=original_grayfile_nib.header)
    nib.save(array_img, niigzfilenametosave)
def resizeinto_512by512(image_nib_nii_file_data):
    if image_nib_nii_file_data.shape[1]>512 : #image_levelset_data.shape[1]:
    #    print("a")
        print("YES DIFFER")
#        print(imagefile_levelset)
    #    npad = ((0, 0), (difference_size//2, difference_size//2), (0, 0))
        size_diff=(image_nib_nii_file_data.shape[1]-512)
        if (size_diff % 2 )== 0 : 
            size_diff=int(size_diff/2)
    #            npad = ((0, 0), (size_diff-1, size_diff+1), (0, 0)) 
            image_nib_nii_file_data=image_nib_nii_file_data[0:image_nib_nii_file_data.shape[0], size_diff:(image_nib_nii_file_data.shape[1]-size_diff), 0:image_nib_nii_file_data.shape[2]]  #+ 1024 #np.pad(image_levelset_data, pad_width=npad, mode='constant', constant_values=np.min(image_levelset_data)) #image_nib_nii_file_data[0:image_nib_nii_file_data.shape[0],0+(difference_size//2):image_nib_nii_file_data.shape[1]-(difference_size//2),0:image_nib_nii_file_data.shape[2]]
            print("I am EVEN")
        else :
            size_diff=int(size_diff/2)
            image_nib_nii_file_data=image_nib_nii_file_data[0:image_nib_nii_file_data.shape[0], size_diff:(image_nib_nii_file_data.shape[1]-size_diff-1), 0:image_nib_nii_file_data.shape[2]] # +1024 #np.pad(image_levelset_data, pad_width=npad, mode='constant', constant_values=np.min(image_levelset_data)) #image_nib_nii_file_data[0:image_nib_nii_file_data.shape[0],0+(difference_size//2):image_nib_nii_file_data.shape[1]-(difference_size//2),0:image_nib_nii_file_data.shape[2]]
    return image_nib_nii_file_data


def rotate_image(img,center1=[0,0],angle=0):
    (h,w)= (img.shape[0],img.shape[1])
    scale = 1.0
    # calculate the center of the image
#    center = (w / 2, h / 2) 
    center = (center1[0], center1[1]) 
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotatedimg = cv2.warpAffine(img, M, (h, w), flags= cv2.INTER_NEAREST) 
    return rotatedimg

def rotate_around_point_highperf(xy, radians, origin=(0, 0)):
    """Rotate a point around a given point.
    
    I call this the "high performance" version since we're caching some
    values that are needed >1 time. It's less readable than the previous
    function but it's faster.
    """
    x, y = xy
    offset_x, offset_y = origin
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y

    return qx, qy
def angle_bet_two_vector(v1,v2):
#    angle = np.arctan2(np.linalg.norm(np.cross(v1,v2)), np.dot(v1,v2)) 
    angle =(np.arctan2(v2[1], v2[0]) -  np.arctan2(v1[1], v1[0]))* 180 / np.pi
    return angle
def angle_bet_two_vectorRad(v1,v2):
#    angle = np.arctan2(np.linalg.norm(np.cross(v1,v2)), np.dot(v1,v2)) 
    angle =np.arctan2(v2[1], v2[0]) -  np.arctan2(v1[1], v1[0])
    return angle

def copy_nifti_parameters_scaleintensity_1(file,output_directoryname):
#     file = sys.argv[1]
#     output_directoryname=  sys.argv[2]
#    files=glob.glob(directoryname+"/*_levelset.nii.gz")
#    for file in files:
    print(file)
#        template="/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/REGISTRATION2TEMPLATE/DATA/CLINICALMASTER/scct_strippedResampled1.nii.gz"
    target= file #sys.argv[2] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/DATA/CTswithObviousMLS/datafromyasheng/NIIGZFILES/Helsinki2000_414_02052013_1437_Head_4.0_ax_Tilt_1_levelset.nii.gz"
    #savefile_extension=sys.argv[3] #"gray" #sys.argv[3]
#        template_nii=nib.load(template)   
    target_nii= nib.load(target)
    target_save=os.path.basename(target)#.split(".nii")[0] + savefile_extension + ".nii.gz" 
    print(os.path.join(output_directoryname,target_save))
    new_header=target_nii.header
    new_data=target_nii.dataobj.get_unscaled()-1024.0
    new_header['glmax']=np.max(new_data)
    new_header['glmin']=np.min(new_data)
    print("changed header and save too")
#        new_header['dim']= target_nii.header['dim']
#        new_header['pixdim']= target_nii.header['pixdim']
    array_img = nib.Nifti1Image(new_data,affine=target_nii.affine, header=new_header)
    nib.save(array_img, os.path.join(output_directoryname,target_save)) 
    return "x"

def copy_nifti_parameters_scaleintensity_sh():
    file = sys.argv[1]
    output_directoryname=  sys.argv[2]
#    files=glob.glob(directoryname+"/*_levelset.nii.gz")
#    for file in files:
    print(file)
#        template="/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/REGISTRATION2TEMPLATE/DATA/CLINICALMASTER/scct_strippedResampled1.nii.gz"
    target= file #sys.argv[2] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/DATA/CTswithObviousMLS/datafromyasheng/NIIGZFILES/Helsinki2000_414_02052013_1437_Head_4.0_ax_Tilt_1_levelset.nii.gz"
    #savefile_extension=sys.argv[3] #"gray" #sys.argv[3]
#        template_nii=nib.load(template)   
    target_nii= nib.load(target)
    target_save=os.path.basename(target)#.split(".nii")[0] + savefile_extension + ".nii.gz" 
    print(os.path.join(output_directoryname,target_save))
    new_header=target_nii.header
#        new_header['dim']= target_nii.header['dim']
#        new_header['pixdim']= target_nii.header['pixdim']
    array_img = nib.Nifti1Image(target_nii.dataobj.get_unscaled()-1024.0,affine=target_nii.affine, header=new_header)
    nib.save(array_img, os.path.join(output_directoryname,target_save)) 
    return "x"

def dummy_copy_nifti_parameters_scaleintensity_sh():
    file = sys.argv[1]
    output_directoryname=  sys.argv[2]
#    files=glob.glob(directoryname+"/*_levelset.nii.gz")
#    for file in files:
    print(file)
#        template="/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/REGISTRATION2TEMPLATE/DATA/CLINICALMASTER/scct_strippedResampled1.nii.gz"
    target= file #sys.argv[2] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/DATA/CTswithObviousMLS/datafromyasheng/NIIGZFILES/Helsinki2000_414_02052013_1437_Head_4.0_ax_Tilt_1_levelset.nii.gz"
    #savefile_extension=sys.argv[3] #"gray" #sys.argv[3]
#        template_nii=nib.load(template)   
    target_nii= nib.load(target)
    target_save=os.path.basename(target)#.split(".nii")[0] + savefile_extension + ".nii.gz" 
    print(os.path.join(output_directoryname,target_save))
    new_header=target_nii.header
#        new_header['dim']= target_nii.header['dim']
#        new_header['pixdim']= target_nii.header['pixdim']
    array_img = nib.Nifti1Image(target_nii.get_fdata(),affine=target_nii.affine, header=new_header)
    nib.save(array_img, os.path.join(output_directoryname,target_save)) 
    return "x"


def betgrayfrombetbinary1_sh():
    inputfile=sys.argv[1]
    bet_inputfile_dir=sys.argv[2]
    betgrayfile=os.path.join(bet_inputfile_dir,os.path.basename(inputfile).split(".nii.gz")[0] + "_bet.nii.gz")   #sys.argv[2]
    ## take the grayscalefiles in the inputdirectory betgrayfile== betbinary
#    allgrayfiles=glob.glob(inputdirectory+ "/*" + betgrayfileext)
#    for eachgrayfiles in allgrayfiles:
    eachgrayfiles=inputfile
    niifilenametosave=os.path.join("/output",os.path.basename(inputfile).split(".nii")[0] + "_brain_f.nii.gz") #outputfilename #os.path.join(outputdirectory,os.path.basename(eachgrayfiles).split(".nii")[0]+"_bet.nii.gz")
    print('eachgrayfiles')
    print(eachgrayfiles)
    gray_nifti=nib.load(eachgrayfiles)
    gray_nifti_data=gray_nifti.get_fdata()
    bet_nifti=nib.load(betgrayfile)
    bet_nifti_data=bet_nifti.get_fdata()
    gray_nifti_data[bet_nifti_data<np.max(bet_nifti_data)]=np.min(gray_nifti_data)
    array_img = nib.Nifti1Image(gray_nifti_data, affine=gray_nifti.affine, header=gray_nifti.header)
    nib.save(array_img, niifilenametosave)
    return niifilenametosave

def betgrayfrombetbinary1_sh_v1():
    inputfile=sys.argv[1]
    bet_inputfile_dir=sys.argv[2]
    output_directory=sys.argv[3]
    betgrayfile=os.path.join(bet_inputfile_dir,os.path.basename(inputfile).split(".nii")[0] + "_bet.nii.gz")   #sys.argv[2]
    ## take the grayscalefiles in the inputdirectory betgrayfile== betbinary
#    allgrayfiles=glob.glob(inputdirectory+ "/*" + betgrayfileext)
#    for eachgrayfiles in allgrayfiles:
    if os.path.exists(betgrayfile):
        eachgrayfiles=inputfile
        niifilenametosave=os.path.join(output_directory,os.path.basename(inputfile).split(".nii")[0] + "_brain_f.nii.gz") #outputfilename #os.path.join(outputdirectory,os.path.basename(eachgrayfiles).split(".nii")[0]+"_bet.nii.gz")
        print('eachgrayfiles')
        print(eachgrayfiles)
        gray_nifti=nib.load(eachgrayfiles)
        gray_nifti_data=gray_nifti.dataobj.get_unscaled() #.get_fdata()
        bet_nifti=nib.load(betgrayfile)
        bet_nifti_data=bet_nifti.dataobj.get_unscaled() #.get_fdata()
        gray_nifti_data[bet_nifti_data<np.max(bet_nifti_data)]=np.min(gray_nifti_data)
        array_img = nib.Nifti1Image(gray_nifti_data, affine=gray_nifti.affine, header=gray_nifti.header)
        nib.save(array_img, niifilenametosave)
        return niifilenametosave
    else:
        print("BET FILE DOES NOT EXIST")

def betgrayfrombetbinary1_sh_v2():
    inputfile=sys.argv[1]
#    bet_inputfile_dir=os.path.dirname(sys.argv[2])
    output_directory=sys.argv[3]
    betgrayfile=sys.argv[2] #os.path.join(bet_inputfile_dir,os.path.basename(inputfile).split(".nii.gz")[0] + "_bet.nii.gz")   #sys.argv[2]
    ## take the grayscalefiles in the inputdirectory betgrayfile== betbinary
#    allgrayfiles=glob.glob(inputdirectory+ "/*" + betgrayfileext)
#    for eachgrayfiles in allgrayfiles:
    eachgrayfiles=inputfile
    niifilenametosave=os.path.join(output_directory,os.path.basename(inputfile).split(".nii")[0] + "_brain_f.nii.gz") #outputfilename #os.path.join(outputdirectory,os.path.basename(eachgrayfiles).split(".nii")[0]+"_bet.nii.gz")
    print('eachgrayfiles')
    print(eachgrayfiles)
    gray_nifti=nib.load(eachgrayfiles)
    gray_nifti_data=gray_nifti.get_fdata()
    bet_nifti=nib.load(betgrayfile)
    bet_nifti_data=bet_nifti.get_fdata()
    gray_nifti_data[bet_nifti_data<np.max(bet_nifti_data)]=np.min(gray_nifti_data)
    array_img = nib.Nifti1Image(gray_nifti_data, affine=gray_nifti.affine, header=gray_nifti.header)
    nib.save(array_img, niifilenametosave)
    return niifilenametosave
def betgrayfrombetbinary1_sh_v3():
    inputfile_gray=sys.argv[1]
    # inputfile_bet=sys.argv[2]
    # bet_inputfile_dir=sys.argv[2]
    output_directory=sys.argv[3]
    betgrayfile=sys.argv[2] #os.path.join(bet_inputfile_dir,os.path.basename(inputfile).split(".nii")[0] + "_bet.nii.gz")   #sys.argv[2]
    ## take the grayscalefiles in the inputdirectory betgrayfile== betbinary
#    allgrayfiles=glob.glob(inputdirectory+ "/*" + betgrayfileext)
#    for eachgrayfiles in allgrayfiles:
    if os.path.exists(betgrayfile):
        eachgrayfiles=inputfile_gray
        niifilenametosave=os.path.join(output_directory,os.path.basename(inputfile_gray).split(".nii")[0] + "_brain_f.nii.gz") #outputfilename #os.path.join(outputdirectory,os.path.basename(eachgrayfiles).split(".nii")[0]+"_bet.nii.gz")
        print('eachgrayfiles')
        print(eachgrayfiles)
        gray_nifti=nib.load(eachgrayfiles)
        gray_nifti_data=gray_nifti.get_fdata() #.get_unscaled() #.get_fdata() dataobj.
        bet_nifti=nib.load(betgrayfile)
        bet_nifti_data=bet_nifti.dataobj.get_unscaled() #.get_fdata()
        gray_nifti_data[bet_nifti_data<np.max(bet_nifti_data)]= 0 #np.min(gray_nifti_data)
        array_img = nib.Nifti1Image(gray_nifti_data, affine=gray_nifti.affine, header=gray_nifti.header)
        nib.save(array_img, niifilenametosave)
        return niifilenametosave
    else:
        print("BET FILE DOES NOT EXIST")

def latex_start(filename):
    file1 = open(filename,"w")
    file1.writelines("\\documentclass{article}\n")
    file1.writelines("\\usepackage[margin=0.5in]{geometry}\n")
    file1.writelines("\\usepackage{graphicx}\n")   
    file1.writelines("\\usepackage[T1]{fontenc} \n") 
    file1.writelines("\\usepackage{datetime} \n") 

#    file1.writelines("\\begin{document}\n")
    return file1
def latex_end(filename):
    file1 = open(filename,"a")
    file1.writelines("\\end{document}\n")
    file1.close()
    return "X"
def latex_begin_document(filename):
    file1 = open(filename,"a")
    file1.writelines("\\begin{document}\n")
    return file1
def latex_insert_line(filename,text="ATUL KUMAR"):
    command= "sed -i 's#\\end{document}##'   " +  filename
    subprocess.call(command,shell=True)
    file1 = open(filename,"a")
    currentDT = str(datetime.datetime.now())
    file1.writelines("\\section{" + currentDT + "}" ) #\\today : \\currenttime}")
#    file1.writelines("\\date{\\today}")
    file1.writelines("\\detokenize{")
    file1.writelines(text)
    file1.writelines("\n")
    file1.writelines("}")
    return file1
def latex_insert_line_nodek(filename,text="ATUL KUMAR"):
    command= "sed -i 's#\\end{document}##'   " +  filename
    subprocess.call(command,shell=True)
    file1 = open(filename,"a")
    file1.writelines(text)
    file1.writelines("\n")

    return file1
def latex_insert_line_nodate(filename,text="ATUL KUMAR"):
    command= "sed -i 's#\\end{document}##'   " +  filename
    subprocess.call(command,shell=True)
    file1 = open(filename,"a")
#    currentDT = str(datetime.datetime.now())
#    file1.writelines("\\section{" + currentDT + "}" ) #\\today : \\currenttime}")
#    file1.writelines("\\date{\\today}")
    file1.writelines("\\detokenize{")
    file1.writelines(text)
    file1.writelines("\n")
    file1.writelines("}")
    return file1
def writetolabnotebook(labnotebook,text):
#    latex_start(labnotebook)
#    latex_begin_document(labnotebook)
    latex_insert_line(labnotebook,text)
    latex_end(labnotebook)
def writetoanewlabnotebook(labnotebook):
    latex_start(labnotebook)
    latex_begin_document(labnotebook)
    latex_insert_line(labnotebook,"THIS IS A NEW LABNOTEBOOK")
    latex_end(labnotebook)
#def write_latex_body(labnotebook,text="HELLO WORLD"):
#    command= "sed -i 's#\\end{document}##'   " +  labnotebook
#    subprocess.call(command,shell=True)
#    command= "echo  " + "\\\section >>   " +  labnotebook
#    subprocess.call(command,shell=True)
#    command= 'echo $(date) >>   ' +  labnotebook
#    subprocess.call(command,shell=True)
#    command= 'echo  ' + text  +  '>>   ' +  labnotebook
#    subprocess.call(command,shell=True)
#    return "x"
#
#def write_latex_end(labnotebook):
#    command= "echo  " + "\\\end{document}  >>  " +  labnotebook
#    subprocess.call(command,shell=True)
#    return "x"

def combinecsvs(inputdirectory,outputdirectory,outputfilename):
    outputfilepath=os.path.join(outputdirectory,outputfilename)
    extension = 'csv'
    all_filenames = [i for i in glob.glob(os.path.join(inputdirectory,'*.{}'.format(extension)))]
#    os.chdir(inputdirectory)
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv(outputfilepath, index=False, encoding='utf-8-sig')

def combinecsvs_sh():
    inputdirectory=sys.argv[1]
    outputdirectory=sys.argv[2]
    outputfilename=sys.argv[3]
    outputfilepath=os.path.join(outputdirectory,outputfilename)
    extension = 'csv'
    all_filenames = [i for i in glob.glob(os.path.join(inputdirectory,'*.{}'.format(extension)))]
#    os.chdir(inputdirectory)
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv(outputfilepath, index=False, encoding='utf-8-sig')

def write_csv(csv_file_name,csv_columns,data_csv):
    try:
        with open(csv_file_name, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in data_csv:
                print("data")
                print(data)
                writer.writerow(data)
    except IOError:
        print("I/O error")
        
def diff_two_csv(file1,file2,outputfile="diff.csv"):
    
    
    return "XX"

def write_tex_im_in_afolder(foldername,max_num_img,img_ext="*.png"):
    # get the folder name
#    foldername="" # complete path
    # start writing tex file
    latexfilename=foldername+".tex"
    latex_start(latexfilename)
    latex_begin_document(latexfilename)
    # for each image file in the folder insert text to include the image a figure
    png_files=glob.glob(os.path.join(foldername,img_ext))
    counter=0
    for each_png_file in png_files:
        if counter < max_num_img:
            thisfilebasename=os.path.basename(each_png_file)
            latex_start_table1c(latexfilename)
            latex_insertimage_table1c(latexfilename,image1=each_png_file,caption= thisfilebasename.split('.png'),imagescale=0.3)
            latex_end_table2c(latexfilename)
            latex_insert_line_nodate(latexfilename, thisfilebasename.split('.png')[0] )
            counter=counter+1
    latex_end(latexfilename)
#    command= "mv  " + latexfilename.split('.')[0] + "*     " + os.path.dirname(foldername)
#    subprocess.call(command,shell=True)    

def filename_replace_dots(foldername,img_ext):
    files=glob.glob(os.path.join(foldername,"*"+img_ext))
    for each_file in files:
        each_f_basename=os.path.basename(each_file)
        each_f_basename_wo_ext=each_f_basename.split(img_ext)
        each_f_basename_wo_extNew= each_f_basename_wo_ext[0].replace(".","_") #re.sub('[^a-zA-Z0-9 \n\.]', '_', each_f_basename_wo_ext[0])
        each_f_basename_new=each_f_basename_wo_extNew + img_ext
        each_f_basename_new_w_path=os.path.join(foldername,each_f_basename_new)
        command = "mv   "  + each_file  + "   " + each_f_basename_new_w_path
        print(each_file)
#        print()
        subprocess.call(command,shell=True)
def filename_replace_dots1(foldername,img_ext):
    files=glob.glob(os.path.join(foldername,"*_"+img_ext))
    for each_file in files:
        each_f_basename=os.path.basename(each_file)
        each_f_basename_wo_ext=each_f_basename.split("_"+img_ext)
        each_f_basename_wo_extNew= each_f_basename_wo_ext[0] +"." + img_ext #.replace(".","_") #re.sub('[^a-zA-Z0-9 \n\.]', '_', each_f_basename_wo_ext[0])
        each_f_basename_new=each_f_basename_wo_extNew # + img_ext
        each_f_basename_new_w_path=os.path.join(foldername,each_f_basename_new)
        command = "mv   "  + each_file  + "   " + each_f_basename_new_w_path
        print(each_f_basename_new)
#        print()
        subprocess.call(command,shell=True)
    
   
    
    
    
def write_tex_im_in_3folders(foldername1,foldername2,foldername3,max_num_img,extension=".png"):
    # get the folder name
#    foldername="" # complete path
    # start writing tex file
    foldername1="/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/GaborOnly"
    foldername2="/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/RegistrationOnly"
    foldername3="/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/RegnGabor"
    foldername=os.path.join(os.path.dirname(foldername1),os.path.basename(foldername1)+os.path.basename(foldername2)+os.path.basename(foldername3))
    latexfilename=foldername+".tex"
    latex_start(latexfilename)
    latex_begin_document(latexfilename)
    # for each image file in the folder insert text to include the image a figure
    png_files=glob.glob(os.path.join(foldername1,"*" + extension )) #.png"))
    counter=0
#    max_num_img=5

    for each_png_file in png_files:
        if counter < max_num_img:
            images=[]
            thisfilebasename=os.path.basename(each_png_file)
            path2=os.path.join(foldername2,thisfilebasename)
            path3=os.path.join(foldername3,thisfilebasename)
            if os.path.exists(path2) and os.path.exists(path3):
                images.append(each_png_file)
                images.append(path2)
                images.append(path2)
                latex_start_tableNc(latexfilename,3)
                images.append(each_png_file)
                latex_insertimage_tableNc(latexfilename,images,3,caption= thisfilebasename.split(extension),imagescale=0.3)
                latex_end_table2c(latexfilename)
                latex_insert_line_nodate(latexfilename, thisfilebasename.split(extension)[0] )
                counter=counter+1
    latex_end(latexfilename)
    command= "mv  " + latexfilename.split('.')[0] + "*     " + os.path.dirname(foldername)
    subprocess.call(command,shell=True)  

def write_tex_im_in_3folders_(foldername1,foldername2,foldername3,max_num_img,extension=".png"):
    # get the folder name
#    foldername="" # complete path
    # start writing tex file
    foldername1="/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/GaborOnly"
    foldername2="/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/RegistrationOnly"
    foldername3="/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/RegnGabor"
    foldername=os.path.join(os.path.dirname(foldername1),os.path.basename(foldername1)+os.path.basename(foldername2)+os.path.basename(foldername3))
    latexfilename=foldername+".tex"
    latex_start(latexfilename)
    latex_begin_document(latexfilename)
    # for each image file in the folder insert text to include the image a figure
    png_files=sorted(glob.glob(os.path.join(foldername1,"*GTvsGABOR*" + extension ))) #.png"))
    counter=0
#    max_num_img=5

    for each_png_file in png_files:
        if counter < max_num_img:
            images=[]
            thisfilebasename=os.path.basename(each_png_file)
            numberofslice=thisfilebasename.split("GTvsGABOR")[1].split(".jpg")[0]
            secondfile=thisfilebasename.split("GTvs")[0]+"GTvsRegist" + str(numberofslice) + ".jpg"
            thirddfile=thisfilebasename.split("GTvs")[0]+"GTvsGaborNRegist" + str(numberofslice) + ".jpg"
            path2=os.path.join(foldername2,secondfile)
            path3=os.path.join(foldername3,thirddfile)
            if os.path.exists(path2) and os.path.exists(path3):
                images.append(each_png_file)
                images.append(path2)
                images.append(path3)
                latex_start_tableNc(latexfilename,3)
                images.append(each_png_file)
                latex_insertimage_tableNc(latexfilename,images,3,caption= thisfilebasename.split(extension),imagescale=0.3)
                latex_end_table2c(latexfilename)
                latex_insert_line_nodate(latexfilename, thisfilebasename.split(extension)[0] )
                counter=counter+1
    latex_end(latexfilename)
    command= "mv  " + latexfilename.split('.')[0] + "*     " + os.path.dirname(foldername)
    subprocess.call(command,shell=True)  

def write_tex_im_in_3folders_sh():
    # get the folder name
#    foldername="" # complete path
    # start writing tex file
    foldername1=sys.argv[1] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/GaborOnly"
    foldername2=sys.argv[2] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/RegistrationOnly"
    foldername3=sys.argv[3] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/RESULTS/RegnGabor"
    foldername=os.path.join(os.path.dirname(foldername1),os.path.basename(foldername1)+os.path.basename(foldername2)+os.path.basename(foldername3))
    latexfilename=foldername+".tex"
    latex_start(latexfilename)
    latex_begin_document(latexfilename)
    # for each image file in the folder insert text to include the image a figure
    png_files=glob.glob(os.path.join(foldername1,"*.png"))
    counter=0
    max_num_img=int(sys.argv[4])

    for each_png_file in png_files:
        if counter < max_num_img:
            images=[]
            thisfilebasename=os.path.basename(each_png_file)
            path2=os.path.join(foldername2,thisfilebasename)
            path3=os.path.join(foldername3,thisfilebasename)
            if os.path.exists(path2) and os.path.exists(path3):
                images.append(each_png_file)
                images.append(path2)
                images.append(path3)
                latex_start_tableNc(latexfilename,3)
                images.append(each_png_file)
                latex_insertimage_tableNc(latexfilename,images,3,caption= thisfilebasename.split('.png'),imagescale=0.3)
                latex_end_table2c(latexfilename)
                latex_insert_line_nodate(latexfilename, thisfilebasename.split('.png')[0] )
                counter=counter+1
    latex_end(latexfilename)
    command= "mv  " + latexfilename.split('.')[0] + "*     " + os.path.dirname(foldername)
    subprocess.call(command,shell=True)     
def write_tex_im_in_afolder_sh():
    foldername=sys.argv[1]
    max_num_img=int(sys.argv[2])
    # get the folder name
#    foldername="" # complete path
    # start writing tex file
    latexfilename=foldername+".tex"
    latex_start(latexfilename)
    latex_begin_document(latexfilename)
    # for each image file in the folder insert text to include the image a figure
    png_files=glob.glob(os.path.join(foldername,"*.png"))
    png_files=png_files.sort(key=os.path.getmtime)
    counter=0
    for each_png_file in png_files:
        if counter < max_num_img:
            thisfilebasename=os.path.basename(each_png_file)
            latex_start_table1c(latexfilename)
            latex_insertimage_table1c(latexfilename,image1=each_png_file,caption= thisfilebasename.split('.png'),imagescale=0.3)
            latex_end_table2c(latexfilename)
            latex_insert_line_nodate(latexfilename, thisfilebasename.split('.png')[0] )
            counter=counter+1
    latex_end(latexfilename)
    command= "mv  " + latexfilename.split('.')[0] + "*     " + os.path.dirname(foldername)
    subprocess.call(command,shell=True)   
    
def write_tex_im_in_afolder_py(foldername,max_num_img=200,fileext="png"):

    # get the folder name
#    foldername="" # complete path
    # start writing tex file

    # for each image file in the folder insert text to include the image a figure
    png_files=glob.glob(os.path.join(foldername,"*."+ fileext))
    png_files.sort(key=os.path.getmtime)
    counter=0
    filecount=0
    latexfilename=foldername+ str(filecount) + ".tex"
    latex_start(latexfilename)
    latex_begin_document(latexfilename)
    for each_png_file in png_files:
        if counter%1000 == 0:
            latex_end(latexfilename)
            filecount=filecount+1
            latexfilename=foldername+ str(filecount) + ".tex"
            latex_start(latexfilename)
            latex_begin_document(latexfilename)
        if counter < max_num_img:
            thisfilebasename=os.path.basename(each_png_file)
            thisfilebasename_S=thisfilebasename.split("."+ fileext)
            thisfilebasename_S=thisfilebasename_S[0].replace(".","_")
            thisfilebasenameNPath=os.path.join(foldername,thisfilebasename_S+"."+ fileext)
            command= "mv   " + each_png_file +  "   " + thisfilebasenameNPath
            subprocess.call(command,shell=True)
            thisfilebasename=os.path.basename(thisfilebasenameNPath)
            latex_start_table1c(latexfilename)
            latex_insertimage_table1c(latexfilename,image1=thisfilebasenameNPath,caption= thisfilebasename.split('.' + fileext),imagescale=0.3)
            latex_end_table2c(latexfilename)
            latex_insert_line_nodate(latexfilename, thisfilebasename.split('.' + fileext)[0] )
            counter=counter+1
    latex_end(latexfilename)
    command= "mv  " + latexfilename.split('.')[0] + "*     " + os.path.dirname(foldername)
    subprocess.call(command,shell=True)

def write_tex_im_in_afolder_v1(foldername,max_num_img=200,filenamepattern=".png"):

    # get the folder name
#    foldername="" # complete path
    # start writing tex file

    # for each image file in the folder insert text to include the image a figure
    fileext=filenamepattern.split(".")[1]
    png_files=glob.glob(os.path.join(foldername,"*"+ filenamepattern))
    png_files.sort(key=os.path.getmtime)
    counter=0
    filecount=0
    latexfilename=foldername+ str(filecount) + ".tex"
    latex_start(latexfilename)
    latex_begin_document(latexfilename)
    for each_png_file in png_files:
        if counter%1000 == 0:
            latex_end(latexfilename)
            filecount=filecount+1
            latexfilename=foldername+ str(filecount) + ".tex"
            latex_start(latexfilename)
            latex_begin_document(latexfilename)
        if counter < max_num_img:
            thisfilebasename=os.path.basename(each_png_file)
            thisfilebasename_S=thisfilebasename.split("."+ fileext)
            thisfilebasename_S=thisfilebasename_S[0].replace(".","_")
            thisfilebasenameNPath=os.path.join(foldername,thisfilebasename_S+"."+ fileext)
            command= "mv   " + each_png_file +  "   " + thisfilebasenameNPath
            subprocess.call(command,shell=True)
            thisfilebasename=os.path.basename(thisfilebasenameNPath)
            latex_start_table1c(latexfilename)
            latex_insertimage_table1c(latexfilename,image1=thisfilebasenameNPath,caption= thisfilebasename.split('.' + fileext),imagescale=0.3)
            latex_end_table2c(latexfilename)
            latex_insert_line_nodate(latexfilename, thisfilebasename.split('.' + fileext)[0] )
            counter=counter+1
    latex_end(latexfilename)
    command= "mv  " + latexfilename.split('.')[0] + "*     " + os.path.dirname(foldername)
    subprocess.call(command,shell=True)
   
def latex_start_table2c(filename):
    print("latex_start_table2c")
    print(filename)
    file1 = open(filename,"a")
    file1.writelines("\\begin{center}\n")
    file1.writelines("\\begin{tabular}{ c c  }\n")
    return file1
def latex_start_tableNc(filename,N):
    print("latex_start_table2c")
    print(filename)
    file1 = open(filename,"a")
    file1.writelines("\\begin{center}\n")
    texttowrite=""
    for x in range(N):
        texttowrite = texttowrite + " | " + "c" + " | " 
    file1.writelines("\\begin{tabular}{ " + texttowrite + "  }\n")
    return file1

def latex_start_tableNc_noboundary(filename,N):
    print("latex_start_table2c")
    print(filename)
    file1 = open(filename,"a")
    file1.writelines("\\begin{center}\n")
    texttowrite=""
    for x in range(N):
        texttowrite = texttowrite +  "c" # + " " 
    file1.writelines("\\begin{tabular}{ " + texttowrite + "  }\n")
    return file1
def latex_start_table1c(filename):
    print("latex_start_table2c")
    print(filename)
    file1 = open(filename,"a")
    file1.writelines("\\begin{center}\n")
    file1.writelines("\\begin{tabular}{ c  }\n")
    return file1

def latex_end_table2c(filename):
    file1 = open(filename,"a")
    file1.writelines("\n")
    file1.writelines("\\end{tabular}\n")
    file1.writelines("\\end{center}\n")
    return file1

def latex_insertimage_table2c(filename,image1="lion.jpg", image2="lion.jpg",caption="ATUL",imagescale=0.5):
    file1 = open(filename,"a")
    file1.writelines("\\includegraphics[width=" + str(imagescale) + "\\textwidth]{" + image1 + "}\n")
    file1.writelines("&")
    file1.writelines("\\includegraphics[width=" + str(imagescale) + "\\textwidth]{"+  image2 + "}\n")

    return file1
def latex_insertimage_tableNc(filename,images,N, caption="ATUL",imagescale=0.5, angle=0,space=1):
    file1 = open(filename,"a")
    # file1.writelines("\\vspace{-2em}\n")

    for x in range(N):
        if x < N-1:
            file1.writelines("\\includegraphics[angle="+ str(angle) + ",width=" + str(imagescale) + "\\textwidth]{" + images[x] + "}\n")
            file1.writelines("&")
        else:
            file1.writelines("\\includegraphics[angle="+ str(angle) + ",width=" + str(imagescale) + "\\textwidth]{" + images[x] + "}\n")
            
#    file1.writelines("\\includegraphics[width=" + str(imagescale) + "\\textwidth]{"+  image2 + "}\n")
    file1.writelines("\\vspace{" + str(space)+"em}\n")
    return file1

def latex_insertimage_tableNc_v1(filename,images,N, caption="ATUL",imagescale=0.5, angle=0,space=1):
    file1 = open(filename,"a")
    # file1.writelines("\\vspace{-2em}\n")

    for x in range(N):
        if x < N-1:
            file1.writelines("\\includegraphics[angle="+ str(angle) + ",width=" + str(imagescale) + "\\textwidth]{" + images[x] + "}\n")
            file1.writelines("&")
        else:
            file1.writelines("\\includegraphics[angle="+ str(angle) + ",width=" + str(imagescale) + "\\textwidth]{" + images[x] + "}\n")
            file1.writelines("\\" + "\\")
            
#    file1.writelines("\\includegraphics[width=" + str(imagescale) + "\\textwidth]{"+  image2 + "}\n")
    # file1.writelines("\\vspace{" + str(space)+"em}\n")
    return file1


def latex_inserttext_tableNc(filename,text1,N,space=1):
    file1 = open(filename,"a")
    # file1.writelines("\\vspace{-2em}\n")

    for x in range(N):
        if x < N-1:
            file1.writelines(text1[x])
            file1.writelines("&")
        else:
            file1.writelines(text1[x] + "\\" +"\\")
            
#    file1.writelines("\\includegraphics[width=" + str(imagescale) + "\\textwidth]{"+  image2 + "}\n")
    # file1.writelines("\\vspace{" + str(space)+"em}\n")
    return file1

def latex_insertimage_table1c(filename,image1="lion.jpg",caption="ATUL",imagescale=0.5,angle=0):
    file1 = open(filename,"a")
    file1.writelines("\\includegraphics[angle="+ str(angle) + ",width=" + str(imagescale) + "\\textwidth]{" + image1 + "}\n")
    return file1
def latex_inserttext_table2c(filename,text1="lion.jpg", text2="lion.jpg"):
    file1 = open(filename,"a")
    file1.writelines(text1)
    file1.writelines("&")
    file1.writelines(text2)
    
def latex_inserttext_table1c(filename,text1="lion.jpg"):
    file1 = open(filename,"a")
    file1.writelines(text1)

    return file1    
def saveslicesofnifti(filename,savetodir=""):
    filename_nib=nib.load(filename)
    filename_gray_data_np=filename_nib.get_fdata()
    min_img_gray=np.min(filename_gray_data_np)
    img_gray_data=0
    if not os.path.exists(savetodir):
        savetodir=os.path.dirname(filename)
    if min_img_gray>=0:
        img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(1000, 1200)) 
    else:
        img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(0, 200))
    for x in range(img_gray_data.shape[2]):
        cv2.imwrite(os.path.join(savetodir,os.path.basename(filename).split(".nii")[0]+str(x)+".jpg" ),img_gray_data[:,:,x]*255 )
    
def savesingleslicesofnifti(filename,slicenumber=0,savetodir=""):
    filename_nib=nib.load(filename)
    filename_gray_data_np=filename_nib.get_fdata()
    min_img_gray=np.min(filename_gray_data_np)
    img_gray_data=0
    if not os.path.exists(savetodir):
        savetodir=os.path.dirname(filename)
    if min_img_gray>=0:
        img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(1000, 1200)) 
    else:
        img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(0, 200))
#    for x in range(img_gray_data.shape[2]):
    x=slicenumber
    filenamejpg=os.path.join(savetodir,os.path.basename(filename).split(".nii")[0]+str(x)+".jpg" )
    cv2.imwrite(filenamejpg,img_gray_data[:,:,x]*255 )
    return filenamejpg

def sas7bdatTOcsv(inputfilename,outputfilename=""):
    if len(outputfilename)==0:
        outputfilename=inputfilename.split(".sas7bdat")[0] + ".csv"
#    inputfilename="/home/atul/Downloads/dra.sas7bdat"
#    outputfilename="/home/atul/Downloads/dra.csv"
    inputdataframe=pd.read_sas(inputfilename, format = 'sas7bdat', encoding="latin-1")
    inputdataframe.to_csv(outputfilename, index=False)
    
def print_number_slices(inputdirectory):
    return "X"
    
def contrast_stretch(img,threshold_id):
    if threshold_id==1:
        ct_image=exposure.rescale_intensity(img.get_fdata() , in_range=(0, 200))
    if threshold_id==2:
        ct_image=exposure.rescale_intensity(img.get_fdata() , in_range=(1000, 1200))        
    return ct_image
def contrast_stretch_np(img,threshold_id):
    if threshold_id==1:
        ct_image=exposure.rescale_intensity(img , in_range=(0, 200))
    if threshold_id==2:
        ct_image=exposure.rescale_intensity(img, in_range=(1000, 1200))        
    return ct_image
def saveslicesofnumpy3D(img_gray_data,savefilename="",savetodir=""):
##    filename_nib=nib.load(filename)
##    filename_gray_data_np=filename_nib.get_fdata()
#    min_img_gray=np.min(filename_gray_data_np)
#    img_gray_data=0
#    if not os.path.exists(savetodir):
#        savetodir=os.path.dirname(filename)
#    if min_img_gray>=0:
#        img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(1000, 1200)) 
#    else:
#        img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(0, 200))
    for x in range(img_gray_data.shape[2]):
        slice_num="{0:0=3d}".format(x)
        cv2.imwrite(os.path.join(savetodir,os.path.basename(savefilename).split(".nii")[0]+str(slice_num)+".jpg" ),img_gray_data[:,:,x] )
  
    
#def tex_for_each_subject():
    # find unique CT names:
    
    #create a tex file:
    # for each file of a CT:
    # find the files with that name arranged in ascending order of time:
    
    # write those images into the tex file
    
    # come out of for loop and close the latex file
    
    
    
def send_email():
    
    gmail_user = 'booktonotesbtn@gmail.com'
    gmail_password = 'AtulAtul1!@#$'
    
    sent_from = gmail_user
    to = ['sharmaatul11@gmail.com']
    subject = 'Program execution'
    body = "Your program has completed its task"
    
    email_text = """\
    From: %s
    To: %s
    Subject: %s
    
    %s
    """ % (sent_from, ", ".join(to), subject, body)
    
    try:
        server = smtplib.SMTP_SSL('mail.smtp2go.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
    
        print('Email sent!')
    except:
        print('Something went wrong...')
    
    
    
def normalizeimage0to1(data): 
    epi_img_data_max=np.max(data)
    epi_img_data_min=np.min(data)
    thisimage=data
    thisimage=(thisimage-epi_img_data_min)/(epi_img_data_max-epi_img_data_min) 
    return thisimage   
    
    
def multidim_intersect(arr1, arr2):
    arr1_view = arr1.view([('',arr1.dtype)]*arr1.shape[1])
    arr2_view = arr2.view([('',arr2.dtype)]*arr2.shape[1])
    intersected = np.intersect1d(arr1_view, arr2_view)
    return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])

def combine_csv_files():
    print("WE ARE COMBINING CSV TOTAL FILES")
    os.chdir(sys.argv[1]) ###"/fileinput_directory") #/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/CTPDATA/Atul_20210408/output_directory/OUTPUT_20_80/CSF_RL_VOL_OUTPUT_infarct_manual/thres2080") #/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/Missing_CTs_2021/OUTPUT/CSF_RL_VOL_OUTPUT/CSVS")
    extension="csv"
    all_filenames=[i for i in glob.glob('*.{}'.format(extension)) ]
    combined_csv=pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv("combined_csv_TOTAL.csv" , index=False, encoding='utf-8-sig')
    print("{0}  files combined".format(len(all_filenames)))


############################################################################################################################




