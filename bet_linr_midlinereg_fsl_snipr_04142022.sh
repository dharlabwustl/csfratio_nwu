#! /bin/bash 

# project_name='SAH' #BJH' 
# current_dir=$PWD
# current_dir_parent=$(dirname ${current_dir})
# rm -r "/DATA/CSV/"
# rm -r "/DATA/ZIP/"
# rm -r "/DATA/DICOMFOLDER/"
# rm -r "/DATA/NIFTI/"

# mkdir -p "/DATA/CSV/"
# mkdir -p "/DATA/ZIP/"
# mkdir -p "/DATA/DICOMFOLDER/"
# mkdir -p "/DATA/NIFTI/"
echo "THE RUNNING PROGRAM IS:   ${0}"
id_password="atulkumar:Pushti11" #${1} #'atulkumar:Pushti11' # #'atulkumar:AtulAtul11'
# websitename=${2}
project_name=BJH #${3}
echo $id_password


counter=1
websitename='https://snipr-dev-test1.nrg.wustl.edu' #'https://snipr-dev-test1.nrg.wustl.edu' 'https://snipr.wustl.edu' ## #
echo $websitename
# id_password='atulkumar:AtulAtul11' # 'atulkumar:123abc'
curl   -u ${id_password}   -X GET   "${websitename}/data/projects/${project_name}/subjects/?format=csv"  > "/DATA/CSV/atul.csv"
# cut -d "," -f${loc_col_a},${loc_col_b} "/DATA/CSV/atul.csv" | tail -n +2
while IFS=',' read -ra array1; do
    # echo ${array[2]}
    # ar1+=("${array[0]}")
    # ar2+=("${array[1]}")
    label+=("${array1[2]}")
    # ar4+=("${array[3]}")
    subject="${array1[2]}"
    arrIN=(${subject//_/ })
    echo "subject":${arrIN[1]}
    echo $subject_URI
    if [[ 1 -gt 0 ]] ; then  #${arrIN[1]} -gt 320 
    curl   -u ${id_password}   -X GET   "${websitename}/data/projects/${project_name}/subjects/${subject}/experiments/?format=csv"    >  "/DATA/CSV/atul_sessions.csv"
while IFS=',' read -ra array2; do
    # echo ${array[2]}
    # ar1+=("${array[0]}")
    # ar2+=("${array[1]}")
    # label+=("${array[2]}")
    # ar4+=("${array[3]}")
    session="${array2[5]}"

    echo ${session}
    echo ${array2[7]}
    session_URI=${array2[7]}
    curl   -u ${id_password}   -X GET   "${websitename}${session_URI}/scans/?format=csv"    >  "/DATA/CSV/atul_sessions_scans.csv"


    # curl   -u 'atulkumar:AtulAtul11'  -X GET   "${websitename}/data/projects/${project_name}/subjects/${subject}/experiments/${session}/scans/?format=csv"    >  "/DATA/CSV/atul_sessions_scans.csv"

while IFS=',' read -ra array3; do
    # echo ${array[2]}
    # ar1+=("${array[0]}")
    # ar2+=("${array[1]}")
    # label+=("${array[2]}")
    # ar4+=("${array[3]}")
    scan_id="${array3[1]}"
    scan_URI="${array3[7]}"
    echo "type":${array3[2]}
    if [[ ${array3[2]} == 'z axial brain' ]] || [[ ${array3[2]} == 'z-axial-brain' ]] || [[ ${array3[2]} == 'Z-Axial-Brain' ]] || [[ ${array3[2]} == 'Z-Axial-Thin' ]] || [[ ${array3[2]} == 'Z-axial-thin' ]] ; then
    zipfilename_ext="${session}_${scan_id}.zip"
    curl  -u  ${id_password}  -X GET  "${websitename}${scan_URI}/resources/DICOM/files?format=zip"   --output    "/DATA/ZIP/${zipfilename_ext}"

    # curl  -u  'atulkumar:AtulAtul11' -X GET  "${websitename}/data/projects/${project_name}/subjects/${subject}/experiments/${session}/scans/${scan_id}/resources/DICOM/files?format=zip"   --output    "/DATA/ZIP/${zipfilename_ext}"
    # unar -d   "/DATA/ZIP/${zipfilename_ext}"  -o  "/DATA/DICOMFOLDER"
    unzip "/DATA/ZIP/${zipfilename_ext}" -d "/DATA/DICOMFOLDER/"
    # dcm2niix -o "/DATA/NIFTI/"  "/DATA/DICOMFOLDER/${session}_${scan_id}/${session}"
    counter=$(( counter + 1 ))
    if [[  ${counter} -gt 1 ]] ; then 
    break
    fi
    # curl   -u 'atulkumar:AtulAtul11'  -X GET   "${websitename}/data/projects/${project_name}/subjects/${subject}/experiments/${session}/scans/?format=csv"    >  "/DATA/CSV/atul_sessions_scans.csv"
fi


done < <( tail -n +2 "/DATA/CSV/atul_sessions_scans.csv" )


# break
    if [[  ${counter} -gt 1 ]] ; then 
    break
    fi

done < <( tail -n +2 "/DATA/CSV/atul_sessions.csv" )
fi 
# break
    if [[  ${counter} -gt 1 ]] ; then 
    break
    fi
done < <( tail -n +2 "/DATA/CSV/atul.csv" )

for each_folder in /DATA/DICOMFOLDER/* ;
do 
echo "Getting done"
dcm2niix -o "/DATA/NIFTI/" -m y ${each_folder}
# dcm2niix -o "/output/" ${each_folder}

done 
SAVE_DIRECTORY=/SMOOTH_IML_OUTPUT
mkdir -p $SAVE_DIRECTORY

intensity=0.01

for each_file in /DATA/NIFTI/*.nii       ;
do 

result_output_directory="/BET_OUTPUT"  #/output
output_for_BET="/BET_OUTPUT" #/output ##$result_output_directory/BET_OUTPUT
filename=${each_file}
echo ${filename}
#mkdir -p $output_for_BET
# for filename in *.nii ; do
# img=`$FSLDIR/bin/remove_ext ${filename}`
#outfile = "${img}_brain"
img=$(/usr/lib/fsl/5.0/remove_ext   ${filename})
echo $img
# Thresholding Image to 0-100
/usr/lib/fsl/5.0/fslmaths "${filename}" -thr 0.000000 -uthr 100.000000  "${img}_th"
# ls /input 
# # Running bet
/usr/lib/fsl/5.0/bet2 "${img}_th" "${img}_brain" -f ${intensity} 

# # Using fslfill to fill in any holes in mask
/usr/lib/fsl/5.0/fslmaths "${img}_brain" -bin -fillh "${img}_brain_Mask"

# # Using the filled mask to mask thresholded image to remove holes
/usr/lib/fsl/5.0/fslmaths "${img}" -mas "${img}_brain_Mask"  "${img}_brain_f" 
 
echo "${img}_brain_f" 
img_output=$(basename   "${img}_brain_f" )
mv "${img}_brain_f".nii.gz    ${output_for_BET}/${img_output}.nii.gz
bet_output_file=${output_for_BET}/${img_output}.nii.gz
echo "BET IS DONE!!"
# ##################################################################################################################
# templatefilename=scct_strippedResampled1.nii.gz 
# mask_on_template=midlinecssfResampled1.nii.gz


# echo " I AM WORKING IN DOCKER"
# input_directory=${output_for_BET}  ##/input 
# output_directory_LR=/LINEAR_REGISTRATION_OUTPUT  
# # mkdir -p $output_directory
# template_directory=/templatenifti
# template_file_name=$templatefilename
# # x=$input_directory/$1 
# # filename=$x 
# # echo $filename
# template_image=$template_directory/$template_file_name 
# template_basename="$(basename -- $template_image)"
# exten="${template_basename%%.nii*}"
# echo $template_basename 
# img=$(/usr/lib/fsl/5.0/remove_ext $filename)
# img_basename=$(basename -- $img)
# output_filename_LR=$output_directory_LR/$img_basename
# echo $output_filename_LR
# /usr/lib/fsl/5.0/flirt  -in "${img}" -ref "${template_image}"  -dof 12 -out "${output_filename_LR}${exten}lin1" -omat ${output_filename_LR}_${exten}lin1.mat  
# echo "IMAGE REGISTERED"
# echo "REGISTRATION OUTPUT:""${output_filename_LR}_${exten}lin1.nii.gz"
# #######################################################################################
# input_filename=$each_file
# echo "I am working in Docker"
# echo $input_filename
# # input_directory=/input  
# # result_output_directory=/output     
# output_for_BET=/BET_OUTPUT
# nifti_reg_output_directory=/LINEAR_REGISTRATION_OUTPUT   
# template_directory=/templatenifti
# # input_directory=$output_for_BET 
# # output_directory=$nifti_reg_output_directory 
# # template_file_name=$2
# # extension="_brain_f.nii.gz" 
# # x=$input_directory/${input_filename%.nii*}$extension
# x=$bet_output_file
# template_mask_directory=/templatemasks
# # output_directory=$nifti_reg_output_directory 
# template_mask_output_directory=/TEMPLATEMASKS_OUTPUT_LR
# mkdir -p $template_mask_output_directory 
# filename=$x 
# echo $filename
# template_image=$template_directory/$template_file_name 
# template_basename="$(basename -- $template_image)"
# exten=${template_basename%.nii*} 
# echo $template_basename 
# img=${filename%.nii*} 
# img_basename=$(basename -- $img)
# # output_filename=$output_directory/$img_basename
# # output_filename_LR=$output_directory_LR/$img_basename
# # echo $output_filename
# # mask_on_template=$3
# midline_ontemplate_nii=$template_mask_directory"/"$mask_on_template 
# file_basename=$(basename $x)
# file_basename=${file_basename%.nii*}  
# filename_without_ext=${x%.nii*} 
# transformmatrix_file=${output_filename_LR}_${exten}lin1.mat 
# inv_transformmatrix_file=${output_filename_LR}_${exten}lin1Inv.mat 
# /usr/lib/fsl/5.0/convert_xfm -omat $inv_transformmatrix_file -inverse $transformmatrix_file
# transformed_output_file=$template_mask_output_directory/${mask_on_template%.nii*}$file_basename".nii.gz"
# echo $transformmatrix_file
# echo $inv_transformmatrix_file
# /usr/lib/fsl/5.0/flirt -in ${midline_ontemplate_nii} -ref $x -out ${transformed_output_file} -init ${inv_transformmatrix_file} -applyxfm
# echo " REGISTERED OUTPUT FILE "
# echo $transformed_output_file

# ####################################################################################################################################
# method_type="REGIS"
# method_type_name="REGIS"

# this_image=$filename
# midline_nifti_file=$transformed_output_file
# python3 -c "
# import sys 
# sys.path.append('/software');
# from module_midline1 import * ;   fit_line_to_midlinepixels_ORF_sh()" $this_image $midline_nifti_file $SAVE_DIRECTORY $method_type  $method_type_name # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename



done

# for x in "/SMOOTH_IML_OUTPUT/"*.tex ;
# do 
#     pdflatex -output-directory=/MIDLINE_PDF $x 
# done
# for each_pdf in "/MIDLINE_PDF/*.pdf" ;
# do 

# # dcm2niix -o "/DATA/NIFTI/" ${each_folder}
# # dcm2niix -o "/output/" ${each_folder}
# cp $each_pdf  "/output/"

# done 

# rm /MIDLINE_PDF/*.aux 
# rm /MIDLINE_PDF/*.log
# user="fslmidline@gmail.com" 
# pswd="midlinefsl1!"
# recipient="sharmaatul11@gmail.com"
# subject='PDFS_for_MIDLINE!'
# body='The_Task_is_Complete!'
# python -c "
# import sys 
# sys.path.append('/software');
# from utilities_simple import * ;   send_email_toSNIPRUSER()" ${user} ${pswd}  ${recipient}  ${subject} ${body}
#  # ${infarctfile_present}  ##$static_template_image $new_image $backslicenumber #$single_slice_filename