source /etc/profiles.d/modules.csh

module add matlab
cd @RUNDIR
rm GCsent
touch GCsending
matlab -nodesktop -nojvm -nodisplay -nosplash -r geostogcm -logfile geostogcm.log
rm GCsending
touch GCsent
