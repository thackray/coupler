#!/bin/csh
#PBS -q short
source /etc/profile.d/modules.csh

module add matlab
cd @INSTALLPATH/MITgcm/verification/global_pcb_llc90/run
rm MGsent
touch MGsending
matlab -nodesktop -nojvm -nodisplay -nosplash -r gcmtogeos -logfile gcmtogeos.log
rm MGsending
touch MGsent
