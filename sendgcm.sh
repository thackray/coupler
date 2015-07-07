source modules.csh

module add matlab
rm MGsent
touch MGsending
matlab -nodesktop -nojvm -nodisplay -nosplash -r gcmtogeos -logfile gcmtogeos.log
rm MGsending
touch MGsent
