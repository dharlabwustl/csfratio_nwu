#!/usr/bin/env bash

## bash functions:

remove_nii_extension()
{
	arrIN1=(${1//.nii/ })
	arrIN_noext=${arrIN1[0]} 
	echo $arrIN_noext
}
remove_custom_extension()
{
	arrIN1=(${1//$2/ })
	arrIN_noext=${arrIN1[0]} 
	echo $arrIN_noext
}

make_subjectid()
{
	filebasename_fororiginal=$(basename  $1)   #"Helsinki2000_742_2_01202014_1157_Head_4.0_ax_Tilt_1" # "Helsinki2000_481_3_03282013_1045_Head_4.0_ax_e1_Tilt_1" #
	sub_string_tocheck="helsinki" 
	current_filename_lower=$(echo "$filebasename_fororiginal" | tr '[:upper:]' '[:lower:]')
	# echo $current_filename_lower
	# echo "$sub_string_tocheck"
	# echo *"$current_filename_lower"*
	firstString="$filebasename_fororiginal"
	secondString="Helsinki2000_"
	stringtoreplace="Helsinki2000-"

	filebasename_fororiginal="${firstString/$stringtoreplace/$secondString}"
	IN="$filebasename_fororiginal"
	arrIN1=(${IN//.nii/ })
	arrIN_noext=${arrIN1[0]} 
	local filebasename_forlevelset=""
	if [[ "$current_filename_lower" == "$sub_string_tocheck"* ]]; then

		# echo $arrIN_noext
		arrIN=(${arrIN_noext//_/ })

		length_split=$(echo "${#arrIN[@]}" )
		# echo   "$(($length_split + 1))"
		# echo "It's there."
		# echo "$(($a + 1))"
		# for i in  $(seq 1 $length_split); do echo "$(($i + 1))" ; done

		for ((i=0;i<length_split;i++)); # do echo "$(($i))" ; done
			do 
				# echo ${arrIN[i]} ; 
			if [[ $i -lt  $(($length_split - 1)) ]]; then
				if [ $i -ne 2 ]
				then
					# echo "Number to delete"
					filebasename_forlevelset="$filebasename_forlevelset""${arrIN[i]}""_"
				fi
			fi

			if [ $i -eq $(($length_split - 1)) ]
			then
				# echo "Number is END."
				filebasename_forlevelset="$filebasename_forlevelset""${arrIN[i]}"
				
			fi

		done
	else
		filebasename_forlevelset=$arrIN_noext

	fi
        arrIN=(${filebasename_forlevelset//_/ })
        filebasename_forlevelset=""
		length_split=$(echo "${#arrIN[@]}" )
		# echo   "$(($length_split + 1))"
		# echo "It's there."
		# echo "$(($a + 1))"
		# for i in  $(seq 1 $length_split); do echo "$(($i + 1))" ; done

		for ((i=0;i<length_split;i++)); # do echo "$(($i))" ; done
			do 
				# echo ${arrIN[i]} ; 
			if [[ $i -lt  3 ]]; then
# 				if [ $i -ne 2 ]
# 				then
					# echo "Number to delete"
					filebasename_forlevelset="$filebasename_forlevelset""${arrIN[i]}""_"
# 				fi
			fi

			if [ $i -eq 3 ]
			then
				# echo "Number is END."
				filebasename_forlevelset="$filebasename_forlevelset""${arrIN[i]}"
				
			fi

		done
    
    
    
    
	echo $filebasename_forlevelset

}

make_subjectid_numonly()
{
	filebasename_fororiginal=$(basename  $1)   #"Helsinki2000_742_2_01202014_1157_Head_4.0_ax_Tilt_1" # "Helsinki2000_481_3_03282013_1045_Head_4.0_ax_e1_Tilt_1" #
	sub_string_tocheck="helsinki" 
	current_filename_lower=$(echo "$filebasename_fororiginal" | tr '[:upper:]' '[:lower:]')
	# echo $current_filename_lower
	# echo "$sub_string_tocheck"
	# echo *"$current_filename_lower"*
	firstString="$filebasename_fororiginal"
	secondString="Helsinki2000_"
	stringtoreplace="Helsinki2000-"

# 	filebasename_fororiginal="${firstString/$stringtoreplace/$secondString}"
	IN="$filebasename_fororiginal"
	arrIN1=(${IN//.nii/ })
	arrIN_noext=${arrIN1[0]} 
	local filebasename_forlevelset=""
# 	if [[ "$current_filename_lower" == "$sub_string_tocheck"* ]]; then

		# echo $arrIN_noext
		arrIN=(${arrIN_noext//_/ })

		length_split=$(echo "${#arrIN[@]}" )
		# echo   "$(($length_split + 1))"
		# echo "It's there."
		# echo "$(($a + 1))"
		# for i in  $(seq 1 $length_split); do echo "$(($i + 1))" ; done

		for ((i=0;i<length_split;i++)); # do echo "$(($i))" ; done
			do 
				# echo ${arrIN[i]} ; 
			if [[ $i -lt  3 ]]; then
# 				if [ $i -ne 2 ]
# 				then
					# echo "Number to delete"
					filebasename_forlevelset="$filebasename_forlevelset""${arrIN[i]}""_"
# 				fi
			fi

			if [ $i -eq 3 ]
			then
				# echo "Number is END."
				filebasename_forlevelset="$filebasename_forlevelset""${arrIN[i]}"
				
			fi

		done
# 	else
# 		filebasename_forlevelset=$arrIN_noext

# 	fi
	echo $filebasename_forlevelset

}


get_matchingfile()
{
        if compgen -G "${1}/${2}*${3}" > /dev/null; then
        	        # if compgen -G "${yasheng_bet_directory}/${subjectid}*bet.nii.gz" > /dev/null; then
                # echo "FILE exists!"
                    bet_mask_file=("${1}/${2}*${3}")
                # echo ${bet_mask_file[0]}
                levelset_filename=${bet_mask_file[0]}
                echo $levelset_filename
        # else
        # 	echo "FILE DOES NOT EXIST"
        fi

}

get_matching_infarctmask_file()
{
		arrIN=(${2//_/ }) # filename without extension

		length_split=$(echo "${#arrIN[@]}" )
		# echo   "$(($length_split + 1))"
		# echo "It's there."
		# echo "$(($a + 1))"
		# for i in  $(seq 1 $length_split); do echo "$(($i + 1))" ; done
		filebasename_forinfarctmask=
		for ((i=0;i<length_split;i++)); # do echo "$(($i))" ; done
			do 
				# echo ${arrIN[i]} ; 
			if [[ $i -lt  4 ]]; then
				# if [ $i -ne 2 ]
				# then
					# echo "Number to delete"
					filebasename_forinfarctmask="$filebasename_forinfarctmask""${arrIN[i]}""_"
				# fi
			fi

			# if [ $i -eq $(($length_split - 1)) ]
			# then
			# 	# echo "Number is END."
			# 	filebasename_forlevelset="$filebasename_forlevelset""${arrIN[i]}"
				
			# fi

		done

        if compgen -G "${1}/${filebasename_forinfarctmask}*${3}" > /dev/null; then
        	        # if compgen -G "${yasheng_bet_directory}/${subjectid}*bet.nii.gz" > /dev/null; then
                # echo "FILE exists!"
                    bet_mask_file=("${1}/${filebasename_forinfarctmask}*${3}")
                # echo ${bet_mask_file[0]}
                levelset_filename=${bet_mask_file[0]}
                echo $levelset_filename
        # else
        # 	echo "FILE DOES NOT EXIST"
        fi

}