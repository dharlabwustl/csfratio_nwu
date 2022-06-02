#!/usr/bin/env bash
input_filename=$1
echo " I AM WORKING IN DOCKER"
# input_directory=/input  
# result_output_directory=/output    
yashengfolder=$input_directory
output_for_BET=/BET_OUTPUT
nifti_reg_output_directory=/LINEAR_REGISTRATION_OUTPUT   
template_directory=/templatenifti
input_directory=$output_for_BET 
output_directory=$nifti_reg_output_directory 
template_file_name=$2
# infarctfile_present=$3
extension="_brain_f.nii.gz" 
x=$input_directory/${input_filename%.nii*}$extension
template_mask_output_directory=/TEMPLATEMASKS_OUTPUT_LR
run_fit_line_to_midlinepixels_ORF_sh() {
this_image=$1
midline_nifti_file=$2
SAVE_DIRECTORY=$3
method_type=$4
method_type_name=$5
python3 -c "
import sys 
sys.path.append('/software');
from module_midline1 import * ;   fit_line_to_midlinepixels_ORF_sh()" $this_image $midline_nifti_file $SAVE_DIRECTORY $method_type  $method_type_name # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename
}

input_for_BET=/preprocessing_output/grayctimage
GRAY_NIFTI_DIRECTORY=$yashengfolder 
TRANSFORMED_MASK_DIRECTORY=$template_mask_output_directory 
TRANSFORMED_MASKFILE_PREFIX="midlinecssfResampled1"
output_directory01=/SMOOTH_IML_OUTPUT
mkdir -p output_directory01
OUTPUT_DIRECTORY=$output_directory01 
FILE_EXTENSION=$gray_nifti_extension 
MASKFILE_EXTENSION=$extension 
echo $OUTPUT_DIRECTORY
mkdir -p  $OUTPUT_DIRECTORY
method_type="REGIS"
method_type_name="REGIS"
# time_recording_generate_smooth_midline=$timing_output/time_recording_generate_smooth_midline.csv 
GRAYSCALENIFTI_FILE=$input_for_BET/$input_filename

basename_grayfilenifti=$(basename -- $GRAYSCALENIFTI_FILE)
transformed_output_file=$TRANSFORMED_MASKFILE_PREFIX${basename_grayfilenifti%.nii*}$MASKFILE_EXTENSION

echo $transformed_output_file
echo "$GRAYSCALENIFTI_FILE" 
echo $TRANSFORMED_MASK_DIRECTORY/$transformed_output_file  
echo "$OUTPUT_DIRECTORY"  
echo "${method_type}" 
echo "${method_type_name}"
run_fit_line_to_midlinepixels_ORF_sh "$GRAYSCALENIFTI_FILE" $TRANSFORMED_MASK_DIRECTORY/$transformed_output_file  "$OUTPUT_DIRECTORY"  "${method_type}" "${method_type_name}"
