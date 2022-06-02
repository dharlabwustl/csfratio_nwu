#!/usr/bin/env bash

lower_threshold=0 #$1 #0 #15 #20 #15
upper_threshold=20 #$2 #50 # 50 #80 #37
# template_directory=${template_gray_folder} #"/storage1/fs1/dharr/Active/ATUL/TEMPLATE/" #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LEARNING/dockermount/TEMPLATENIFTI" 
# template_mask_directory=${template_midline_mask_folder} #"/storage1/fs1/dharr/Active/ATUL/TEMPLATEMASKS" #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LEARNING/dockermount/TEMPLATEMASKS"
templatefilename=scct_strippedResampled1.nii.gz 
mask_on_template=midlinecssfResampled1.nii.gz
# # data_master_folder="/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/OriginalWithLevelset/nwu_csf_data" 
data_master_folder=/preprocessing_output #/maindirectory #${output_directory} #/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/OriginalWithLevelset/nwu_csf_data  
# #/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/Krakow2_20200902/preprocessing_output #/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/CTPDATA/Atul_20210408/preprocessing_output #/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/CTPDATA/Atul_20210408/preprocessing_output # /storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/CTPDATA/BASELINE/preprocessing_output ##/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/CTPDATA/BASELINE/preprocessing_output #"/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/TESTING_DIR/threshold_testing/preprocessing_output"
# # data_master_folder="/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/TESTING_DIR/threshold_testing/preprocessing_output" 

YashengFolder=${data_master_folder}/grayctimage 
csf_mask_directory=${data_master_folder}/csfmask 
infarct_mask_directory=${data_master_folder}/infarctmask 
yasheng_bet_directory=${data_master_folder}/betmask 
# # ################################## USER DEFINED VARIABLES END ###################################################
csv_file_name=${data_master_folder}/levelset_grayfiles_name_1.csv 
echo "Filename" > ${csv_file_name} 
for leveset_file in ${YashengFolder}/*.nii* ; 
do
	echo  $leveset_file >> ${csv_file_name} 
done


# ############################################################################

result_output_directory=/result_directory #"${data_master_folder}"

# # mkdir -p ${result_output_directory}
# timing_output=${result_output_directory}/TIMING 
# # mkdir -p $timing_output
# time_recording_BETGRAY=$timing_output/time_recording_BETGRAY.csv
# echo "filename, time" > $time_recording_BETGRAY
# time_recording_LINEAR_REGIS=$timing_output/time_recording_LINEAR_REGIS.csv
# echo "filename, time" > $time_recording_LINEAR_REGIS
# time_recording_MIDLINEMASK_TRANSFORM=$timing_output/time_recording_MIDLINEMASK_TRANSFORM.csv
# echo "filename, time" > $time_recording_MIDLINEMASK_TRANSFORM
# time_recording_generate_smooth_midline=$timing_output/time_recording_generate_smooth_midline.csv
# echo "filename, time" > $time_recording_generate_smooth_midline
# ####
# Time_recording_CSF_RL_CALCULATION=$timing_output/Time_recording_CSF_RL_CALCULATION.csv
# echo "filename, time" > $Time_recording_CSF_RL_CALCULATION
# time_recording_PDF_gnerations=$timing_output/time_recording_PDF_gnerations.csv
# echo "Total number of files, time" > $time_recording_PDF_gnerations



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
# start=`date +%s`
# export LSF_DOCKER_VOLUMES="${YashengFolder}:/input  ${result_output_directory}:/output   ${template_directory}:/templatenifti  ${template_mask_directory}:/templatemasks   ${csf_mask_directory}:/csf_mask_directory  ${infarct_mask_directory}:/infarct_mask_directory  ${yasheng_bet_directory}:/yasheng_bet_directory"

# bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/pythononly)'     
/software/bet_withlevelset.sh $this_filename ${this_betfilename} #Helsinki2000_1019_10132014_1048_Head_2.0_ax_Tilt_1_levelset # ${3} # Helsinki2000_702_12172013_2318_Head_2.0_ax_levelset.nii.gz #${3} # $6 $7 $8 $9 ${10}
# end=`date +%s`
# runtime=$((end-start))
# echo "${this_filename}, $runtime" >> $time_recording_BETGRAY

this_filename_brain=${this_filename%.nii*}_brain_f.nii.gz
# BET_OUTPUT_DIR=${result_output_directory}/BET_OUTPUT #$data_master_folder/OUTPUT/BET_OUTPUT
echo "LINEAR REGISTRATION TO TEMPLATE"
# start=`date +%s` 
# export LSF_DOCKER_VOLUMES="${BET_OUTPUT_DIR}:/input  ${result_output_directory}:/output   ${template_directory}:/templatenifti  ${template_mask_directory}:/templatemasks"
# # bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/fsl502only)'    
/software/linear_rigid_registration.sh ${this_filename_brain} ${templatefilename} #$3 ${6} WUSTL_233_11122015_0840__levelset_brain_f.nii.gz 
# end=`date +%s`
# runtime=$((end-start))
# echo "${this_filename}, $runtime" >> $time_recording_LINEAR_REGIS

echo "RUNNING IML FSL PART"
# # start=`date +%s` 
# # export LSF_DOCKER_VOLUMES="${YashengFolder}:/input  ${result_output_directory}:/output   ${template_directory}:/templatenifti  ${template_mask_directory}:/templatemasks "
# # # bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/fsl502only)'  
/software/ideal_midline_fslpart.sh ${this_filename}  ${templatefilename} ${mask_on_template}  #$9 #${10} #$8 
# end=`date +%s`
# runtime=$((end-start))
# echo "${this_filename}, $runtime" >> $time_recording_MIDLINEMASK_TRANSFORM

echo "RUNNING IML PYTHON PART"
# export LSF_DOCKER_VOLUMES="${YashengFolder}:/input  ${result_output_directory}:/output  ${result_output_directory}/TEMPLATEMASKS_OUTPUT_LR:/output/TEMPLATEMASKS_OUTPUT_LR   ${template_directory}:/templatenifti  ${template_mask_directory}:/templatemasks"

# start=`date +%s` 
# # bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/pythononly)'  
/software/ideal_midline_pythonpart.sh  ${this_filename} ${templatefilename}  #$3 #$8 $9 ${10}
# end=`date +%s`
# runtime=$((end-start))
# echo "${this_filename}, $runtime" >> $time_recording_generate_smooth_midline

echo "RUNNING NWU AND CSF VOLUME CALCULATION "
# start=`date +%s` 
# export LSF_DOCKER_VOLUMES="${YashengFolder}:/input  ${result_output_directory}:/output   ${result_output_directory}/SMOOTH_IML_OUTPUT:/output/SMOOTH_IML_OUTPUT   ${csf_mask_directory}:/csf_mask_directory  ${infarct_mask_directory}:/infarct_mask_directory    ${yasheng_bet_directory}:/yasheng_bet_directory"

# bsub -G compute-dharr -g /atulkumar/group2 -Is -a 'docker(sharmaatul11/pythononly)'  
/software/nwu_csf_volume.sh  ${this_filename}   ${this_betfilename} ${this_csfmaskfilename} ${this_infarctmaskfilename}  ${lower_threshold} ${upper_threshold}
# # end=`date +%s`
# # runtime=$((end-start))
# # echo "${this_filename}, $runtime" >> $Time_recording_CSF_RL_CALCULATION
pdflatex -output-directory=/MIDLINE_PDF /CSF_RL_VOL_OUTPUT/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.tex
cp /MIDLINE_PDF/$(/usr/lib/fsl/5.0/remove_ext $this_filename)*.pdf /output/
echo "program successful" > /output/success.txt 
}

COUNTER=0
numberoffiles=1 #50
numberoffiles_fornow=1
upper_limit=99999999999
lower_limit=0
### ITERATE TRHOUGH ECAH FILE 
file_count=0
betmaskext="_bet"
csfmaskext="_unet"  ## "_final_seg" #
infarctmaskext=_infarct_auto_removesmall ##  "_seg" #"_normalized.nii.gz_pos" #"_seg" #"_infarct_auto_removesmall" #"_infarct_auto"
for gray_file in ${YashengFolder}/*.nii* ;
do 
    echo ${x}
    gray_file_basename=$(basename ${gray_file})
    gray_file_basename_noext=${gray_file_basename%.nii*}
    betmaskfilename=${gray_file_basename_noext}${betmaskext}.nii.gz
    csfmaskfilename=${gray_file_basename_noext}${csfmaskext}.nii.gz
    infarctmaskfilename=${gray_file_basename_noext}${infarctmaskext}.nii.gz

    echo ${infarctmaskfilename}_${csfmaskfilename}_${betmaskfilename}
    run_IML_NWU_CSF_CALC  ${gray_file_basename} ${betmaskfilename} ${csfmaskfilename} ${infarctmaskfilename} 
done

# for x in ${YashengFolder}/*_levelset.* ; do 
# # if [ "$numberoffiles" -lt  $numberoffiles_fornow ] ; then
# echo x:${x}

# # done
# # if [ $numberoffiles -lt  $upper_limit ] && [ $numberoffiles -ge  $lower_limit ] ; then
# #     # x=${YashengFolder}/Krak_089_04132015_0952_MOZG_3.0_H31s_do_3D_Tilt_1_levelset.nii.gz 
#         x_basename=$(basename $x)
# #         echo ${x_basename}
#     while IFS=, read -r Filename ; do
#     echo Filename:${Filename}
# # #       Filename_=${Filename//[[:blank:]]/}
# #       echo $Filename_
# # #       echo ${#Filename_}
# # #       echo $x_basename
#     if [[ "${x_basename}" == *"$Filename"*  ]] && [[ "${#Filename}" -gt 9  ]] ; then
# # #     if [[ "${Filename}" ==  "WUSTL_219_09022015_1052" ]] ; then
#   echo "It's there."
# #   file_count=$(( file_count + 1 ))


# #   # do something... Don't forget to skip the header line!
# #   [[ "$name" != "Name" ]] && echo "$name"

# # echo $upper_limit
# # echo $numberoffiles

#     subjectid=${x_basename%_levelset*}
# #     echo "GRAY FILE NAME!"
# #     echo $x
#     echo $subjectid

# # 
# bet_mask_filename=""
# infarct_mask_filename=""
# csf_mask_filename=""
#     if compgen -G "${csf_mask_directory}/${subjectid}*${csfmaskext}.nii.gz" > /dev/null; then
#         echo "CSF FILE exists!"
#         csf_mask_file=("${csf_mask_directory}/${subjectid}*${csfmaskext}.nii.gz")
# #         # echo ${csf_mask_file[0]}
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
#             run_IML_NWU_CSF_CALC  $(basename $x) $(basename ${bet_mask_filename}) $(basename ${csf_mask_filename}) $(basename ${infarct_mask_filename})    
#             numberoffiles=$(( numberoffiles + 1 ))
# #             break
#         else 
#             echo "ONLY CSF MASK and BET MASK FILE EXISTS" 
#             echo $bet_mask_filename
#             echo $csf_mask_filename
#             run_IML_NWU_CSF_CALC  $(basename $x) $(basename ${bet_mask_filename}) $(basename ${csf_mask_filename})  "XX"  
#             numberoffiles=$(( numberoffiles + 1 ))
#         fi

#         fi


# fi
# # ##    done < /storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/SOFTWARE/testfile.csv   
# done < ${csv_file_name} #"/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/OriginalWithLevelset/nwu_csf_data/grayctimage/gray_ct_three_data.csv" 

# # # "/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/DATA/OriginalWithLevelset/nwu_csf_data/image_size_few_xy_matched.csv"



# # fi 
# # # COUNTER=$(( COUNTER + 1 ))
# done 
# # echo ${file_count}





for x in "/CSF_RL_VOL_OUTPUT/"*.tex ;
do 
    pdflatex -output-directory=/MIDLINE_PDF $x 
done
for each_pdf in "/MIDLINE_PDF/*.pdf" ;
do 

# dcm2niix -o "/DATA/NIFTI/" ${each_folder}
# dcm2niix -o "/output/" ${each_folder}
cp $each_pdf  "${result_output_directory}/"

done 