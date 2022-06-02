### CSF ratio and NWU in NCCT with infarct

## Introduction
For a non-contrast CT scan (NCCT) of a brain with infarct, this project calculates CSF (cerebrospinal fluid) ratio of the infarct side vs non-infarct side, and its net water updake (NWU) based on the Hounsfield Unit (HU) values of the CT voxels.
$$ CSF\ ratio = \frac{CSF\ volume\ on\ infarct\ side}{CSF\ volume\ on\ non-infarct\ side}$$
$$ NWU = (1- \frac{average\ HU\ of\ the\ infarct\ volume}{average\ HU\ of\ the\ non-infarct\ volume})\ X\ 100$$ 
## Requirements:
To calculate CSF ratio and NWU following image files in nifti format are required:
  - NCCT 
  - CSF mask
  - BET (brain extraction) mask
  - Infarct mask

Different kinds of images should be located in separate directories.

The directory structure must be as follows:
```
 DATADIRECTORY
    ├── betmask (contains BET mask)
    ├── csfmask (contains CSF maks)
    ├── grayctimage (contains NCCT)
    └── infarctmask (contains infarct mask)
```
File  name of the different masks MUST be derived from the NCCT file. For example, if 
NCCT file name is "abc.nii.gz" then :
 - bet mask file must be "abc_bet.nii.gz"
 - csf mask file must be "abc_unet.nii.gz"
 - infarct mask file must be "abc_infarct_auto_removesmall.nii.gz"
 
 
## Running the script for calculation:

```
docker run -it -v (path to DATADIRECTORY):/preprocessing_output -v (path to OUTPUTDIRECTORY):/result_directory sharmaatul11/csfrationwu   /software/bet_linreg_midline_nwu.sh 
```

## Output:
The result for each NCCT will be stored as a PDF file. The PDF file would contain the images with several masks and midline superimposed on the NCCT as well as the calculated values as a table.
The PDF files would be stored int he OUTPUTDIRECTORY


