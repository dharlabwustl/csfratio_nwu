FROM sharmaatul11/fsl502py369ltx:latest
# Run configuration script for normal usage
RUN mkdir -p  /input_directory
RUN chmod -R 777 /input_directory
RUN mkdir -p /DATA/CSV/
RUN chmod -R 777 /DATA/CSV/
RUN mkdir -p /DATA/ZIP/
RUN chmod -R 777  /DATA/ZIP/
RUN mkdir -p /DATA/DICOMFOLDER/
RUN chmod -R 777  /DATA/DICOMFOLDER/
RUN mkdir -p /DATA/NIFTI/
RUN chmod -R 777 /DATA/NIFTI/
RUN mkdir -p /BET_OUTPUT/
RUN chmod -R 777 /BET_OUTPUT/
RUN mkdir -p /LINEAR_REGISTRATION_OUTPUT/
RUN chmod -R 777 /LINEAR_REGISTRATION_OUTPUT/
RUN mkdir -p /TEMPLATEMASKS_OUTPUT_LR/
RUN chmod -R 777 /TEMPLATEMASKS_OUTPUT_LR/
RUN mkdir -p /MIDLINE_PDF/
RUN chmod -R 777 /MIDLINE_PDF/
RUN mkdir -p /SMOOTH_IML_OUTPUT/
RUN chmod -R 777 /SMOOTH_IML_OUTPUT/

RUN mkdir -p /CSF_RL_VOL_OUTPUT/
RUN chmod -R 777 /CSF_RL_VOL_OUTPUT/
RUN mkdir -p /input_directory
RUN chmod -R 777 /input_directory
RUN mkdir -p /preprocessing_output/grayctimage
RUN chmod -R 777 /preprocessing_output/grayctimage
RUN mkdir -p /preprocessing_output/csfmask
RUN chmod -R 777 /preprocessing_output/csfmask
RUN mkdir -p /preprocessing_output/infarctmask
RUN chmod -R 777 /preprocessing_output/infarctmask
RUN mkdir -p /preprocessing_output/betmask
RUN chmod -R 777 /preprocessing_output/betmask
RUN mkdir -p /preprocessing_output/csvfile_directory
RUN chmod -R 777 /preprocessing_output/csvfile_directory
RUN mkdir -p /preprocessing_output/TIMING
RUN chmod -R 777  /preprocessing_output/TIMING

RUN mkdir -p /software
RUN mkdir -p /templatenifti
RUN mkdir -p /templatemasks
RUN apt install -y dcm2niix
COPY scct_strippedResampled1.nii.gz   /templatenifti/
COPY  midlinecssfResampled1.nii.gz   /templatemasks/
COPY  bet_linr_midlinereg_fsl_snipr_04142022.sh bash_functions_forhost.sh module_NWU_CSFCompartment_Calculations.py nwu_csf_volume.sh bet_linreg_midline_nwu.sh ideal_midline_pythonpart.sh linear_rigid_registration.sh  ideal_midline_fslpart.sh  utilities_simple.py module_midline1.py utilities_simple_trimmed.py bet_withlevelset.sh /software/ 

RUN  chmod +x /software/bet_linr_midlinereg_fsl_snipr_04142022.sh && chmod +x /software/bash_functions_forhost.sh && chmod +x /software/nwu_csf_volume.sh && chmod +x /software/ideal_midline_pythonpart.sh && chmod +x /software/bet_withlevelset.sh && chmod +x /software/bet_linreg_midline_nwu.sh &&  chmod +x   /software/linear_rigid_registration.sh    &&  chmod +x   /software/ideal_midline_fslpart.sh 
