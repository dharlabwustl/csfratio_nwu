# # #!/usr/bin/env python3
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Sun Apr  5 17:04:42 2020

# @author: atul
# """
# # -*- coding: utf-8 -*-
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """

import numpy as np
import sys,os
import nibabel as nib
import pandas as pd
from skimage import exposure
import cv2,re
sys.path.append("/software")
from utilities_simple import *
from sklearn.linear_model import RANSACRegressor


def contrast_stretch(img,threshold_id):
    if threshold_id==1:
        ct_image=exposure.rescale_intensity(img, in_range=(0, 200))
    if threshold_id==2:
        ct_image=exposure.rescale_intensity(img , in_range=(1000, 1200))        
    return ct_image
def test_prog():
    print("I am working")
def fit_line_to_midlinepixels_ORF_sh():
     gray_file=sys.argv[1] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/DATA/CTs_SP_Pineal/CTs/Helsinki2000_1225_1_05012015_1250_Head_2.0_ax_Tilt_1.nii"
     midline_nifti_file=sys.argv[2] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/SOFTWARE/pyscripts/IDEALML/midlinecssfResampled1InverseT.nii.gz"
     SAVE_DIRECTORY=sys.argv[3]
     methodType=sys.argv[4]
     method_name=sys.argv[5]
     # infarctfile_present=int(float(sys.argv[6]))
     latexfilename=os.path.join(SAVE_DIRECTORY,os.path.basename(gray_file.split(".nii")[0].replace('.','_')) + "_IML.tex")
     print("latexfilename")
     print(latexfilename)
     latex_start(latexfilename)
     latex_begin_document(latexfilename)
     
     midline_nifti=nib.load(midline_nifti_file)
     midline_nifti_np=midline_nifti.get_fdata()
     # if infarctfile_present==1:
     midline_nifti_np=resizeinto_512by512(midline_nifti_np)
     gray_nifti=nib.load(gray_file)
     gray_nifti_np=gray_nifti.get_fdata()  
     # if infarctfile_present==1: 
     gray_nifti_np=resizeinto_512by512(gray_nifti_np)
     gray_nifti_np_im=contrast_stretch(gray_nifti_np,1)*255
#     if "_levelset" in os.path.basename(gray_file):
#         gray_nifti_np_im=contrast_stretch(gray_nifti_np,2)*255
#     if "_header_copied" in os.path.basename(gray_file):
#         gray_nifti_np_im=contrast_stretch(gray_nifti_np,1)*255  
     numberofslices=midline_nifti_np.shape[2]
     for xx in range(numberofslices): 
         this_slice=midline_nifti_np[:,:,xx]
         this_slice_max=np.max(this_slice)
         this_slice[this_slice<(this_slice_max-5)]=0
         slice_3_layer= np.zeros([gray_nifti_np_im.shape[0],gray_nifti_np_im.shape[1],3])

         slice_3_layer[:,:,0]= gray_nifti_np_im[:,:,xx]
         slice_3_layer[:,:,1]= gray_nifti_np_im[:,:,xx]
         slice_3_layer[:,:,2]= gray_nifti_np_im[:,:,xx]
         if np.sum(this_slice)>0:
             print(xx)
             binary_image_non_zero_cord_t=np.nonzero(this_slice>0)
             binary_image_non_zero_cord=np.transpose(binary_image_non_zero_cord_t)
             ###########################################
             X=binary_image_non_zero_cord[:,1].reshape(-1,1)
             y=binary_image_non_zero_cord[:,0].reshape(-1,1)
             boston_df = pd.DataFrame(y)
             boston_df.columns = ['y']
             min_samples=X.shape[0]
             print("min_samples")
             print(min_samples)
 #            z = np.abs(stats.zscore(boston_df))
 #            threshold = 3
 #            aa=np.where(z > threshold)        
             reg = RANSACRegressor(random_state=0,min_samples=min_samples, max_trials=1000,residual_threshold =1).fit(X,y)
 #            score_diff_from_1= 1-reg.score(X, y)
             x_axis_1=np.arange(0,512).reshape(-1, 1)
             y_axis_1 = reg.predict(x_axis_1)            
             #############################################       
 #            coefficients = np.polyfit(non_zero_cord[1], non_zero_cord[0], 1)
 #            polynomial = np.poly1d(coefficients)
 #            x_axis_1 = np.linspace(0,511,512)
 #            y_axis_1 = polynomial(x_axis_1)
             font = cv2.FONT_HERSHEY_SIMPLEX
             cv2.putText(slice_3_layer, os.path.basename(gray_file).split(".nii")[0]+ "_SLICE_"+str(xx), (1,500), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
             cv2.putText(slice_3_layer,"Ideal Midline", (200,20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
             filename_tosave=re.sub('[^a-zA-Z0-9 \n\_]', '', os.path.basename(gray_file).split(".nii")[0])
             slice_number="{0:0=3d}".format(xx)
             slice_3_layer=cv2.line(slice_3_layer, ( int(x_axis_1[0]),int(y_axis_1[0])),(int(x_axis_1[511]),int(y_axis_1[511])), (0,255,255), 2)
             imagefilename=os.path.join(SAVE_DIRECTORY,filename_tosave+"IML_" + method_name+ str(slice_number)+ ".jpg")
             cv2.imwrite(imagefilename,slice_3_layer)
             file_midline=os.path.join(SAVE_DIRECTORY,filename_tosave+method_name+str(slice_number)+  ".npy")
             line_data={'x_axis':x_axis_1, 'y_axis':y_axis_1}
 #            line_data=dict([('x_axis',x_axis_1),('y_axis',y_axis_1)])
             np.save(file_midline,line_data)
             latex_start_tableNc_noboundary(latexfilename,1)
             image_list=[]
             image_list.append(imagefilename)
             latex_insertimage_tableNc(latexfilename,image_list,1, caption=os.path.basename(gray_file).split(".nii")[0],imagescale=0.5, angle=90,space=1)
             
             # latex_start_table1c(latexfilename)
             # latex_insertimage_table1c(latexfilename,image1=imagefilename,caption= os.path.basename(gray_file).split(".nii")[0],imagescale=0.5)
             latex_end_table2c(latexfilename)
             latex_insert_line_nodate(latexfilename, os.path.basename(gray_file).split(".nii")[0] + "_SLICE_"+str(xx) )
     latex_end(latexfilename)



# # # -*- coding: utf-8 -*-
# # """
# # Created on Sun Apr  5 17:04:42 2020

# # @author: atul
# # """
# # # -*- coding: utf-8 -*-
# # #!/usr/bin/env python3
# # # -*- coding: utf-8 -*-
# # """

# import numpy as np
# import sys,os
# import nibabel as nib
# import pandas as pd
# from skimage import exposure
# import cv2,re
# from utilities_simple import *
# from sklearn.linear_model import RANSACRegressor


# def contrast_stretch(img,threshold_id):
#     if threshold_id==1:
#         ct_image=exposure.rescale_intensity(img, in_range=(0, 200))
#     if threshold_id==2:
#         ct_image=exposure.rescale_intensity(img , in_range=(1000, 1200))        
#     return ct_image
# def test_prog():
#     print("I am working")
# def fit_line_to_midlinepixels_ORF_sh():
#      gray_file=sys.argv[1] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/DATA/CTs_SP_Pineal/CTs/Helsinki2000_1225_1_05012015_1250_Head_2.0_ax_Tilt_1.nii"
#      midline_nifti_file=sys.argv[2] #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/MIDLINE/SOFTWARE/pyscripts/IDEALML/midlinecssfResampled1InverseT.nii.gz"
#      SAVE_DIRECTORY=sys.argv[3]
#      methodType=sys.argv[4]
#      method_name=sys.argv[5]
#      latexfilename=os.path.join(SAVE_DIRECTORY,os.path.basename(gray_file.split(".nii")[0].replace('.','_')) + "_IML.tex")
#      print("latexfilename")
#      print(latexfilename)
#      latex_start(latexfilename)
#      latex_begin_document(latexfilename)
     
#      midline_nifti=nib.load(midline_nifti_file)
#      midline_nifti_np=midline_nifti.get_fdata()
#      # midline_nifti_np=resizeinto_512by512(midline_nifti_np)
#      gray_nifti=nib.load(gray_file)
#      gray_nifti_np=gray_nifti.get_fdata()  
#      # gray_nifti_np=resizeinto_512by512(gray_nifti_np) 
#      gray_nifti_np_im=contrast_stretch(gray_nifti_np,1)*255
# #     if "_levelset" in os.path.basename(gray_file):
# #         gray_nifti_np_im=contrast_stretch(gray_nifti_np,2)*255
# #     if "_header_copied" in os.path.basename(gray_file):
# #         gray_nifti_np_im=contrast_stretch(gray_nifti_np,1)*255  
#      numberofslices=midline_nifti_np.shape[2]
#      for xx in range(numberofslices): 
#          this_slice=midline_nifti_np[:,:,xx]
#          this_slice_max=np.max(this_slice)
#          this_slice[this_slice<(this_slice_max-5)]=0
#          slice_3_layer= np.zeros([gray_nifti_np_im.shape[0],gray_nifti_np_im.shape[1],3])

#          slice_3_layer[:,:,0]= gray_nifti_np_im[:,:,xx]
#          slice_3_layer[:,:,1]= gray_nifti_np_im[:,:,xx]
#          slice_3_layer[:,:,2]= gray_nifti_np_im[:,:,xx]
#          slice_3_layer=cv2.flip(slice_3_layer,0)        
#          if np.sum(this_slice)>0:
#              print(xx)
#              binary_image_non_zero_cord_t=np.nonzero(this_slice>0)
#              binary_image_non_zero_cord=np.transpose(binary_image_non_zero_cord_t)
#              ###########################################
#              X=binary_image_non_zero_cord[:,1].reshape(-1,1)
#              y=binary_image_non_zero_cord[:,0].reshape(-1,1)
#              boston_df = pd.DataFrame(y)
#              boston_df.columns = ['y']
#              min_samples=X.shape[0]
#              print("min_samples")
#              print(min_samples)
#  #            z = np.abs(stats.zscore(boston_df))
#  #            threshold = 3
#  #            aa=np.where(z > threshold)        
#              reg = RANSACRegressor(random_state=0,min_samples=min_samples, max_trials=1000,residual_threshold =1).fit(X,y)
#  #            score_diff_from_1= 1-reg.score(X, y)
#              x_axis_1=np.arange(0,512).reshape(-1, 1)
#              y_axis_1 = reg.predict(x_axis_1)            
#              #############################################       
#  #            coefficients = np.polyfit(non_zero_cord[1], non_zero_cord[0], 1)
#  #            polynomial = np.poly1d(coefficients)
#  #            x_axis_1 = np.linspace(0,511,512)
#  #            y_axis_1 = polynomial(x_axis_1)
#              font = cv2.FONT_HERSHEY_SIMPLEX
#              cv2.putText(slice_3_layer, os.path.basename(gray_file).split(".nii")[0]+ "_SLICE_"+str(xx), (1,500), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
#              cv2.putText(slice_3_layer,"Ideal Midline", (200,20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
#              filename_tosave=re.sub('[^a-zA-Z0-9 \n\_]', '', os.path.basename(gray_file).split(".nii")[0])
#              slice_number="{0:0=3d}".format(xx)
#              slice_3_layer=cv2.line(slice_3_layer, ( int(x_axis_1[0]),int(y_axis_1[0])),(int(x_axis_1[511]),int(y_axis_1[511])), (0,255,255), 2)
#              imagefilename=os.path.join(SAVE_DIRECTORY,filename_tosave+"IML_" + method_name+ str(slice_number)+ ".jpg")
#              cv2.imwrite(imagefilename,slice_3_layer)
#              file_midline=os.path.join(SAVE_DIRECTORY,filename_tosave+method_name+str(slice_number)+  ".npy")
#              line_data={'x_axis':x_axis_1, 'y_axis':y_axis_1}
#  #            line_data=dict([('x_axis',x_axis_1),('y_axis',y_axis_1)])
#              np.save(file_midline,line_data)
#              latex_start_tableNc_noboundary(latexfilename,1)
#              image_list=[]
#              image_list.append(imagefilename)
#              latex_insertimage_tableNc(latexfilename,image_list,1, caption=os.path.basename(gray_file).split(".nii")[0],imagescale=0.5, angle=90,space=1)
#              # latex_start_table1c(latexfilename)
#              # latex_insertimage_table1c(latexfilename,image1=imagefilename,caption= os.path.basename(gray_file).split(".nii")[0],imagescale=0.5) #
#              latex_end_table2c(latexfilename)
#              latex_insert_line_nodate(latexfilename, os.path.basename(gray_file).split(".nii")[0] + "_SLICE_"+str(xx) )
#      latex_end(latexfilename)

# # latex_start_tableNc_noboundary(latexfilename,4)
# # image_list=[]


# # image_list.append(os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename_gray +".png"))
# # image_list.append(imagefilename_infarct)
# # image_list.append(os.path.join(SLICE_OUTPUT_DIRECTORY,image_infarct_details)) 
# # image_list.append(os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +".png"))


# # latex_insertimage_tableNc(latexfilename,image_list,4, caption="",imagescale=0.2, angle=90,space=1)

# # # latex_insertimage_table1c(latexfilename,image1=os.path.join(SLICE_OUTPUT_DIRECTORY,imagefilename +".png"),caption= os.path.basename(niftifilename).split(".nii")[0],imagescale=0.3,angle=90)
# # latex_end_table2c(latexfilename)

