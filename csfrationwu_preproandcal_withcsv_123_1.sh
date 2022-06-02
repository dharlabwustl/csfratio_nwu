#!/usr/bin/env bash
# export LSF_DOCKER_PRESERVE_ENVIRONMENT=TRUE
# mode="${9}"
# run_preprocessing="${10}"
# echo "istesting : ${mode}"
# echo "run_preprocessing : ${run_preprocessing}"
# #  template_directory="/storage1/fs1/dharr/Active/ATUL/TEMPLATE/" #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LEARNING/dockermount/TEMPLATENIFTI"
# #  template_mask_directory="/storage1/fs1/dharr/Active/ATUL/TEMPLATEMASKS" #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LEARNING/dockermount/TEMPLATEMASKS"
templatefilename=scct_strippedResampled1.nii.gz
mask_on_template=midlinecssfResampled1.nii.gz
# ## mount directories for docker:
# master_directory=$1 #/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/Atul_20210408
# original_CT_directory_names=$2 #/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/Atul_20210408/original_CT_directory_names
# YashengDataCopy=$3 #/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/Atul_20210408
# infarct_mask_directory=$4 #/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/Atul_20210408/levelset_infarctmask
# output_directory=$master_directory"/output_directoryFU"  ### /output_directoryFU" 
# # gray_output_subdir=${output_directory}/grayctimage

# # csf_output_subdir=${output_directory}/csfmask

# # infarct_output_subdir=${output_directory}/infarctmask

# # bet_output_subdir=${output_directory}/betmask

# # levelset_directory="${YashengDataCopy}/levelset_gray"
# # levelset_csf_directory="${YashengDataCopy}/levelset_csf"
# # levelset_bet_directory="${YashengDataCopy}/levelset_bet"
# # csvfile_directory="${YashengDataCopy}/csvfile_directory"

# ######################################
# mkdir -p ${output_directory}
# gray_output_subdir=${output_directory}/grayctimage
# mkdir -p $gray_output_subdir
# csf_output_subdir=${output_directory}/csfmask
# mkdir -p $csf_output_subdir
# infarct_output_subdir=${output_directory}/infarctmask
# mkdir -p $infarct_output_subdir
# bet_output_subdir=${output_directory}/betmask
# mkdir -p $bet_output_subdir
# levelset_directory="${YashengDataCopy}/levelset_gray"
# levelset_csf_directory="${YashengDataCopy}/levelset_csf"
# levelset_bet_directory="${YashengDataCopy}/levelset_bet"
# csvfile_directory="${YashengDataCopy}/csvfile_directory"
# mkdir -p ${csvfile_directory}
# export LSF_DOCKER_VOLUMES="${original_CT_directory_names}:/original_CT_directory_names ${csvfile_directory}:/csv_file_directory  ${infarct_mask_directory}:/infarct_mask_directory   ${YashengDataCopy}:/YashengDataCopy   ${levelset_directory}:/levelset_gray_directory   ${levelset_csf_directory}:/levelset_csf_directory  ${levelset_bet_directory}:/levelset_bet_directory   ${output_directory}:/output_directory" 
# if [[  ${run_preprocessing} == "1" ]] ; then
# echo "RUNNING as FINAL"
# # bsub -K -G  compute-dharr  -o ./output1.txt -g /atulkumar/group2 -q general -a 
# bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/pythononly)'   /software/preprocesssingfilename.sh
# fi
# #######################################


# export LSF_DOCKER_VOLUMES="${original_CT_directory_names}:/original_CT_directory_names ${csvfile_directory}:/csv_file_directory  ${infarct_mask_directory}:/infarct_mask_directory   ${YashengDataCopy}:/YashengDataCopy   ${levelset_directory}:/levelset_gray_directory   ${levelset_csf_directory}:/levelset_csf_directory  ${levelset_bet_directory}:/levelset_bet_directory   ${output_directory}:/output_directory" 


# echo $csv_file_directory
# mkdir -p $csv_file_directory
# echo "I AM WORKING"

# echo "Filename" > ${csv_file_name}

# ################################## USER DEFINED VARIABLES ###################################################
# #### To run this script successfully the base name of all the files should be same and the extenstion of the files should be as follows:

# export LSF_DOCKER_PRESERVE_ENVIRONMENT=TRUE
# ${master_directory}  ${csfmaskext}  ${infarctmaskext} ${output_dir_extension1} ${output_dir_extension2}
intensity=0.01
lower_threshold=${4} #20  #$1 #0 #15 #20 #15
upper_threshold=${5} #80 #$2 #50 # 50 #80 #37

data_master_folder=${1} #output_directory} 
YashengFolder=${data_master_folder}/grayctimage
csf_mask_directory=${data_master_folder}/csfmask
infarct_mask_directory=${data_master_folder}/infarctmask
yasheng_bet_directory=${data_master_folder}/betmask
# ################################## USER DEFINED VARIABLES END ###################################################
# csv_file_directory=${output_directory}/csv_file_directory
# csv_file_name=${data_master_folder}/levelset_grayfiles_name.csv
# for levelset_file in ${YashengFolder}/*.nii* ;
# do
# eachfile_basename_1=$( basename -- ${levelset_file} )
# arrIN_1=(${eachfile_basename_1//_/ })
# echo  ${arrIN_1[0]}_${arrIN_1[1]}_${arrIN_1[2]}_${arrIN_1[3]} >> ${csv_file_name}
# # echo  ${eachfile_basename_1%_levelset.nii*} >> ${csv_file_name}
# done
############################################################################
result_output_directory="${data_master_folder}/OUTPUT_${lower_threshold}_${upper_threshold}"

mkdir -p ${result_output_directory}
mkdir -p ${result_output_directory}/TEMPLATEMASKS_OUTPUT_LR
timing_output=${result_output_directory}/TIMING
mkdir -p $timing_output
time_recording_BETGRAY=$timing_output/time_recording_BETGRAY.csv
echo "filename, time" > $time_recording_BETGRAY
time_recording_LINEAR_REGIS=$timing_output/time_recording_LINEAR_REGIS.csv
echo "filename, time" > $time_recording_LINEAR_REGIS
time_recording_MIDLINEMASK_TRANSFORM=$timing_output/time_recording_MIDLINEMASK_TRANSFORM.csv
echo "filename, time" > $time_recording_MIDLINEMASK_TRANSFORM
time_recording_generate_smooth_midline=$timing_output/time_recording_generate_smooth_midline.csv
echo "filename, time" > $time_recording_generate_smooth_midline
####
Time_recording_CSF_RL_CALCULATION=$timing_output/Time_recording_CSF_RL_CALCULATION.csv
echo "filename, time" > $Time_recording_CSF_RL_CALCULATION
time_recording_PDF_gnerations=$timing_output/time_recording_PDF_gnerations.csv
echo "Total number of files, time" > $time_recording_PDF_gnerations
run_IML_NWU_CSF_CALC()

{
this_filename=${1}
this_betfilename=${2}
this_csfmaskfilename=${3}
this_infarctmaskfilename=${4}
# echo "BET USING ORIGINAL FILES WITH FSL"
# docker run   -v ${YashengFolder}:/input -v ${result_output_directory}:/output  -v ${template_directory}:/templatenifti -v ${template_mask_directory}:/templatemasks -v ${yasheng_bet_directory}:/yasheng_bet_directory   sharmaatul11/fsl502only   /software/bet_fsl.sh ${this_filename} #  #$6 # $7 $8 $9 ${10}
echo "BET USING LEVELSET MASK"
# #Krak_089_04132015_0952_MOZG_3.0_H31s_do_3D_Tilt_1_levelset.nii.gz
start=`date +%s`
docker run -it  -v ${YashengFolder}:/input -v ${result_output_directory}:/output   -v   ${csf_mask_directory}:/csf_mask_directory -v ${infarct_mask_directory}:/infarct_mask_directory  -v ${yasheng_bet_directory}:/yasheng_bet_directory  sharmaatul11/pythononly1 /software/bet_withlevelset.sh $this_filename ${this_betfilename}

# ####### export LSF_DOCKER_VOLUMES="${YashengFolder}:/input  ${result_output_directory}:/output      ${csf_mask_directory}:/csf_mask_directory  ${infarct_mask_directory}:/infarct_mask_directory  ${yasheng_bet_directory}:/yasheng_bet_directory"
# ##### ${template_directory}:/templatenifti  ${template_mask_directory}:/templatemasks
# #bsub -G compute-dharr -g /atulkumar/group2 -q general -a
# # bsub -G compute-dharr -g /atulkumar/group2 -Is -a 
# # bsub -K -G compute-dharr  -o ./output.txt  -g /atulkumar/group2 -q general -a 
# # bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/pythononly1)'     /software/bet_withlevelset.sh $this_filename ${this_betfilename} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}
# #bsub -G compute-dharr -g /atulkumar/group2 -q general -a 'docker(sharmaatul11/pythononly)'     /software/bet_withlevelset.sh $this_filename ${this_betfilename} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}
# end=`date +%s`
# runtime=$((end-start))
# echo "${this_filename}, $runtime" >> $time_recording_BETGRAY
# #wait 
# this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
# BET_OUTPUT_DIR=${result_output_directory}/BET_OUTPUT #$data_master_folder/OUTPUT/BET_OUTPUT
echo "LINEAR REGISTRATION TO TEMPLATE"
# start=`date +%s`
# export LSF_DOCKER_VOLUMES="${BET_OUTPUT_DIR}:/input  ${result_output_directory}:/output   "
# # ${template_directory}:/templatenifti  ${template_mask_directory}:/templatemasks
# # bsub -G compute-dharr -g /atulkumar/group2 -q general -a 
# # bsub -G compute-dharr -g /atulkumar/group2 -Is -a  
# # bsub -K -G compute-dharr  -o ./output.txt  -g /atulkumar/group2 -q general -a 

# bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(
docker run -it -v ${BET_OUTPUT_DIR}:/input  -v ${result_output_directory}:/output sharmaatul11/fsl502only    /software/linear_rigid_registration.sh ${this_filename_brain} ${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz
# #wait 
# end=`date +%s`
# runtime=$((end-start))
# echo "${this_filename}, $runtime" >> $time_recording_LINEAR_REGIS

# echo "RUNNING IML FSL PART"
# start=`date +%s`
# export LSF_DOCKER_VOLUMES="${YashengFolder}:/input  ${result_output_directory}:/output    "
# # ${template_directory}:/templatenifti  ${template_mask_directory}:/templatemasks
# # bsub -G compute-dharr -g /atulkumar/group2 -q general -a  -o ./output.txt 
# # bsub -G compute-dharr -g /atulkumar/group2 -Is -a
# # bsub -K -G compute-dharr  -o ./output.txt -g /atulkumar/group2 -q general -a 
# bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/fsl502only)'  /software/ideal_midline_fslpart.sh ${this_filename}  ${templatefilename} ${mask_on_template}  #$9 #${10} #$8
# #wait 
# end=`date +%s`
# runtime=$((end-start))
# echo "${this_filename}, $runtime" >> $time_recording_MIDLINEMASK_TRANSFORM

# echo "RUNNING IML PYTHON PART"
# export LSF_DOCKER_VOLUMES="${YashengFolder}:/input  ${result_output_directory}:/output  ${result_output_directory}/TEMPLATEMASKS_OUTPUT_LR:/output/TEMPLATEMASKS_OUTPUT_LR   "
# # ${template_directory}:/templatenifti  ${template_mask_directory}:/templatemasks
# start=`date +%s`
# # bsub -G compute-dharr -g /atulkumar/group2 -q general -a
# # bsub -G compute-dharr -g /atulkumar/group2 -Is -a 
# # bsub -K -G compute-dharr  -o ./output.txt -g /atulkumar/group2 -q general -a 
# bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/pythononly1)'  /software/ideal_midline_pythonpart.sh  ${this_filename} ${templatefilename}  #$3 #$8 $9 ${10}
# #wait 
# end=`date +%s`
# runtime=$((end-start))
# echo "${this_filename}, $runtime" >> $time_recording_generate_smooth_midline

# echo "RUNNING NWU AND CSF VOLUME CALCULATION "
# start=`date +%s`
# export LSF_DOCKER_VOLUMES="${YashengFolder}:/input  ${result_output_directory}:/output   ${result_output_directory}/SMOOTH_IML_OUTPUT:/output/SMOOTH_IML_OUTPUT   ${csf_mask_directory}:/csf_mask_directory  ${infarct_mask_directory}:/infarct_mask_directory    ${yasheng_bet_directory}:/yasheng_bet_directory"

# # bsub -G compute-dharr -g /atulkumar/group2 -q general -a
# # bsub -G compute-dharr -g /atulkumar/group2 -Is -a  
# # bsub -o atul.txt -G compute-dharr -g /atulkumar/group2 -Is -a 
# # bsub -K -G compute-dharr -o ./output.txt -g /atulkumar/group2 -q general -a 
# bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/pythononly1)'   /software/nwu_csf_volume.sh  ${this_filename}   ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename}  ${lower_threshold} ${upper_threshold}
# # #wait 
# # # end=`date +%s`
# # # runtime=$((end-start))
# # # echo "${this_filename}, $runtime" >> $Time_recording_CSF_RL_CALCULATION
# # #######################################################################################################################################################################################################
# # ########## REPORT #########################
# # ###result_output_directory="${data_master_folder}/OUTPUT_${lower_threshold}_${upper_threshold}"
# # ##
# # report_numberofdata=$timing_output/report_numberofdata.csv
# # echo "NUMBER OF FILES ON WHICH  NWU AND CSF VOLUME CALCULATION WAS APPLIED" > $report_numberofdata
# # echo ${numberoffiles} >> $report_numberofdata
# # texfiles_folder=${result_output_directory}/CSF_RL_VOL_OUTPUT #"${data_master_folder}/OUTPUT/CSF_RL_VOL_OUTPUT"
# # imagefiles_folder=${result_output_directory}/CSF_RL_VOL_OUTPUT # "${data_master_folder}/OUTPUT/CSF_RL_VOL_OUTPUT"

# # export LSF_DOCKER_VOLUMES="${texfiles_folder}:/input  ${result_output_directory}:/output   ${imagefiles_folder}:/output/CSF_RL_VOL_OUTPUT"

# # #bsub -G compute-dharr -g /atulkumar/group2 -q general -a 
# # # bsub -K -G compute-dharr -o ./output.txt -g /atulkumar/group2 -q general -a 

# # # bsub -K -G compute-dharr -o ./output.txt -g /atulkumar/group2 -q general -a 
# #  bsub -K -G compute-dharr -o ./output.txt -g /atulkumar/group2 -q general -a  'docker(sharmaatul11/latex)' /software/make_pdfs_nwu_csfvol_eachfile.sh   ${this_filename} 
# # #bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/latex)'   /software/nwu_csf_volume.sh  ${this_filename}   ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename}  ${lower_threshold} ${upper_threshold}



}
csfmaskext=${2} #"_unet" #"_final_seg" #"_unet"
infarctmaskext=${3} ##"_infarct_auto_removesmall"  #"_seg" #"_normalized.nii.gz_pos" #"_seg" #"_infarct_auto_removesmall" #"_infarct_auto"

for gray_file in ${YashengFolder}/*.nii* ;
do 
    echo ${x}
    gray_file_basename=$(basename ${gray_file})
    gray_file_basename_noext=${gray_file_basename%_levelset.nii*}
    betmaskfilename=${gray_file_basename_noext}_levelset_bet.nii.gz
    csfmaskfilename=${gray_file_basename_noext}${csfmaskext}.nii.gz
    infarctmaskfilename=${gray_file_basename_noext}${infarctmaskext}.nii.gz

    echo ${infarctmaskfilename}_${csfmaskfilename}_${betmaskfilename}
    run_IML_NWU_CSF_CALC  ${gray_file_basename} ${betmaskfilename} ${csfmaskfilename} ${infarctmaskfilename} 
done

# 

# COUNTER=0
# numberoffiles=1 #50
# numberoffiles_fornow=1
# upper_limit=999999999999
# if [[  ${mode} == "1" ]] ; then 
# upper_limit=1
# fi 
# lower_limit=0
# ### ITERATE TRHOUGH ECAH FILE
# file_count=0
# csfmaskext=${2} #"_unet" #"_final_seg" #"_unet"
# infarctmaskext=${3} ##"_infarct_auto_removesmall"  #"_seg" #"_normalized.nii.gz_pos" #"_seg" #"_infarct_auto_removesmall" #"_infarct_auto"

# for x in ${YashengFolder}/*_levelset.nii* ; do
# echo "X:  $x"
# # if [ "$numberoffiles" -lt  $numberoffiles_fornow ] ; then

# if [ $numberoffiles -lt  $upper_limit ] && [ $numberoffiles -ge  $lower_limit ] ; then
#     # x=${YashengFolder}/Krak_089_04132015_0952_MOZG_3.0_H31s_do_3D_Tilt_1_levelset.nii.gz
#         x_basename=$(basename $x)
# #         echo ${x_basename}
#     while IFS=, read -r Filename ; do
# #     echo ${Filename}
# #       Filename_=${Filename//[[:blank:]]/}
#       echo $Filename_
# #       echo ${#Filename_}
# #       echo $x_basename
#     if [[ "${x_basename}" == *"$Filename"*  ]] && [[ "${#Filename}" -gt 9  ]] ; then
# #     if [[ "${Filename}" ==  "WUSTL_219_09022015_1052" ]] ; then
#   echo "It's there."
#   file_count=$(( file_count + 1 ))

#   # do something... Don't forget to skip the header line!
#   [[ "$name" != "Name" ]] && echo "$name"

# echo $upper_limit
# echo $numberoffiles

#     subjectid=${x_basename%_levelset*}
#     echo "GRAY FILE NAME!"
#     echo $x
#     echo $subjectid

# bet_mask_filename=""    

# infarct_mask_filename=""
# csf_mask_filename=""
#     if compgen -G "${csf_mask_directory}/${subjectid}*${csfmaskext}.nii.gz" > /dev/null; then
#         # echo "CSF FILE exists!"
#         csf_mask_file=("${csf_mask_directory}/${subjectid}*${csfmaskext}.nii.gz")
#         # echo ${csf_mask_file[0]}
#         csf_mask_filename=${csf_mask_file[0]}
#     fi
#         if compgen -G "${yasheng_bet_directory}/${subjectid}*_bet.nii.gz" > /dev/null; then
#                 # echo "BET FILE exists!"
#                     bet_mask_file=("${yasheng_bet_directory}/${subjectid}*bet.nii.gz")
#                 # echo ${bet_mask_file[0]}
#                 yasheng_bet_filename=${bet_mask_file[0]}
#                 bet_mask_filename=${bet_mask_file[0]}
#                 # echo $yasheng_bet_filename
#         fi
#         if compgen -G "${infarct_mask_directory}/${subjectid}*${infarctmaskext}.nii.gz" > /dev/null; then
#             # echo "INFARCT FILE exists!"
#             infarct_mask_file=("${infarct_mask_directory}/${subjectid}*${infarctmaskext}.nii.gz")
#             # echo ${infarct_mask_file[0]}
#             infarct_mask_filename=${infarct_mask_file[0]}
#         fi
#         if [ ${#bet_mask_filename} -gt 5 ] && [ ${#csf_mask_filename} -gt 5 ] &&  [ -f $bet_mask_filename ] &&  [ -f  $csf_mask_filename  ]  ;     then

#             if  [ ${#infarct_mask_filename} -gt 5 ] &&  [ -f  $infarct_mask_filename  ]  ;     then
#             echo "ALL THREE FILE EXISTS"
#             echo $infarct_mask_filename
#             echo $csf_mask_filename
#             echo $bet_mask_filename
#             run_IML_NWU_CSF_CALC  $(basename $x) $(basename ${bet_mask_filename}) $(basename ${csf_mask_filename}) $(basename ${infarct_mask_filename})   &
#             numberoffiles=$(( numberoffiles + 1 ))
# #             break
#         else
#             echo "ONLY CSF MASK and BET MASK FILE EXISTS"
#             echo $bet_mask_filename
#             echo $csf_mask_filename
#             run_IML_NWU_CSF_CALC  $(basename $x) $(basename ${bet_mask_filename}) $(basename ${csf_mask_filename})  "XX"  &
#             numberoffiles=$(( numberoffiles + 1 ))
#         fi

#         fi


# fi

# done < ${csv_file_name}   

# fi
# # COUNTER=$(( COUNTER + 1 ))
# done
# echo ${file_count} 

# # ### combine csvs:
# # fileinput_directory=${result_output_directory}/CSF_RL_VOL_OUTPUT/TOTAL
# # mkdir -p ${fileinput_directory}
# # mv ${result_output_directory}/CSF_RL_VOL_OUTPUT/*TOTAL*.csv ${fileinput_directory}/

# # export LSF_DOCKER_VOLUMES="${fileinput_directory}:/fileinput_directory"

# # ## combine csvs:
# # fileinput_directory=${result_output_directory}/CSF_RL_VOL_OUTPUT/TOTAL
# # mkdir -p ${fileinput_directory}
# # mv ${result_output_directory}/CSF_RL_VOL_OUTPUT/*TOTAL*.csv ${fileinput_directory}/

# # bsub -K -G compute-dharr -o ./output.txt -g /atulkumar/group2 -q general -a   'docker(sharmaatul11/pythononly)'  /software/call_combine_csv_files.sh # python /software/combine_csv_files.py


