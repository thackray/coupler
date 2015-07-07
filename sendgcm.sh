source /etc/profile.d/modules.csh

module add matlab
cd @RUNDIR
rm MGsent
touch MGsending
matlab -nodesktop -nojvm -nodisplay -nosplash -r gcmtogeos -logfile gcmtogeos.log
rm MGsending
touch MGsent
