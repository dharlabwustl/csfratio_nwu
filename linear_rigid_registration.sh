#!/usr/bin/env bash

intensity=0.01
echo " I AM WORKING IN DOCKER"
input_directory=/BET_OUTPUT 
output_directory=/LINEAR_REGISTRATION_OUTPUT  
echo " I am in LINEAR_REGISTRATION"
# mkdir -p $output_directory
template_directory=/templatenifti
template_file_name=$2
x=$input_directory/$1 
filename=$x 
echo $filename
template_image=$template_directory/$template_file_name 
template_basename="$(basename -- $template_image)"
exten="${template_basename%%.nii*}"
echo $template_basename 
img=$(/usr/lib/fsl/5.0/remove_ext $filename)
img_basename=$(basename -- $img)
output_filename=$output_directory/$img_basename
echo $output_filename
/usr/lib/fsl/5.0/flirt  -in "${img}" -ref "${template_image}"  -dof 12 -out "${output_filename}${exten}lin1" -omat ${output_filename}_${exten}lin1.mat  


/usr/lib/fsl/5.0/flirt -ref  "${img}"  -in "${template_image}"  -dof 12 -out "${output_filename}${exten}lin1_1" -omat ${output_filename}_${exten}lin1_1.mat  

echo "IMAGE REGISTERED"
echo "REGISTRATION OUTPUT:""${output_filename}_${exten}lin1.nii.gz"
echo "REGISTRATION OUTPUT:""${output_filename}_${exten}lin1_1.nii.gz"
