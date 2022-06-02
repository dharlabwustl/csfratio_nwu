#!/usr/bin/env bash
grayimage=/preprocessing_output/grayctimage/${1} 
echo " I AM WORKING IN DOCKER NWU_CSF_VOLUME.sh"
betimage=/preprocessing_output/betmask/${2}
csfmaskimage=/preprocessing_output/csfmask/${3}
infarctmaskimage=/preprocessing_output/infarctmask/${4}
npyfiledirectory=/SMOOTH_IML_OUTPUT
output_directory=/CSF_RL_VOL_OUTPUT #/outputdirectory #$(realpath -- $2) #"/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LEARNING/dockermount/BRAIN_EXTRACTION_OUTPUT"
mkdir -p $output_directory
lower_threshold=${5}
upper_threshold=${6}
python3 -c "
import sys ;
print('I AM HERE')
sys.path.append('/software');
from module_NWU_CSFCompartment_Calculations  import * ;    measure_compartments_with_reg_round5_one_file_sh_v1()"  $grayimage $betimage  $csfmaskimage ${infarctmaskimage}  ${npyfiledirectory}     ${output_directory}  ${lower_threshold} ${upper_threshold}  #$gray_bet_extension $yashengfolder $infarct_mask_ext $lower_threshold $upper_threshold  ${levelsetfile_directory}  #$method_type  $method_type_name #$static_template_image $new_image $backslicenumber #$single_slice_filename


