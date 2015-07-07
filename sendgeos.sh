source modules.csh

module add matlab
rm GCsent
touch GCsending
matlab -nodesktop -nojvm -nodisplay -nosplash -r geostogcm -logfile geostogcm.log
rm GCsending
touch GCsent
