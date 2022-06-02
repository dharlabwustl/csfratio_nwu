#!/usr/bin/env bash
export LSF_DOCKER_PRESERVE_ENVIRONMENT=TRUE
input_csv=$1
echo $input_csv

while IFS=, read -r field1 field2
do

    if [[ $field1 == *master_directory* ]] ; then 
      echo "$field1 and $field2"  
      master_directory=${field2}
    fi
    if [[ $field1 == *original_CT_directory_name* ]] ; then 
      echo "$field1 and $field2" 
            original_CT_directory_name=${field2}
    fi
    if [[ $field1 == *YashengData_directory* ]] ; then 
      echo "$field1 and $field2"  
            YashengData_directory=${field2}
    fi
    if [[ $field1 == *infarct_mask_directory* ]] ; then 
      echo "$field1 and $field2"  
            infarct_mask_directory=${field2}
    fi
    if [[ $field1 == *csfmaskext* ]] ; then 
      echo "$field1 and $field2"  
            csfmaskext=${field2}
    fi
    if [[ $field1 == *infarctmaskext* ]] ; then 
      echo "$field1 and $field2"  
            infarctmaskext=${field2}
    fi
    if [[ $field1 == *output_dir_extension1* ]] ; then 
      echo "$field1 and $field2"  
            output_dir_extension1=${field2}
    fi
    if [[ $field1 == *output_dir_extension2* ]] ; then 
      echo "$field1 and $field2"  
        output_dir_extension2=${field2}
    fi
    if [[ $field1 == *istesting* ]] ; then 
      echo "$field1 and $field2"  
        istesting=${field2}
    fi
        if [[ $field1 == *run_preprocessing* ]] ; then 
      echo "$field1 and $field2"  
        run_preprocessing=${field2}
    fi
done < $input_csv
echo master_directory:${master_directory}
echo $output_dir_extension1
echo $output_dir_extension2
echo $master_directory
echo $infarctmaskext
echo $csfmaskext
echo $infarct_mask_directory
echo $YashengData_directory
echo $original_CT_directory_name
echo $istesting
echo $run_preprocessing

csv_file_name=${master_directory}/timetocompleteFU_DATA.csv
echo "Filename" > ${csv_file_name}
echo `date` >> ${csv_file_name}
./csfrationwu_preproandcal_withcsv_123_1.sh ${master_directory}  ${csfmaskext}  ${infarctmaskext} ${output_dir_extension1} ${output_dir_extension2}   
echo `date` >> ${csv_file_name}