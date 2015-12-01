#!/bin/csh
#
#PBS -l nodes=13
#PBS -N MITgcm
#PBS -j oe
#PBS -q xlong
source /etc/profile.d/modules.csh

module add gcc
module add intel
module add netcdf/20130909
module add openmpi/1.7.2

setenv MPI_INC_DIR /home/software/intel/intel-2013_sp1.0.080/pkg/openmpi/openmpi-1.7.2/include/
setenv NETCDF_ROOT /home/software/intel/intel-2013_sp1.0.080/pkg/netcdf/netcdf-20130909/

cd @INSTALLPATH/MITgcm/verification/global_pcb_llc90/run
while ( ! -e STOP )
if ( -e GO ) then 
    rm GO
    rm DONE
    touch RUNNING
    mpirun -np 13 ./mitgcmuv
    rm RUNNING
    if (`tail -n 1 STDOUT.0000` == "PROGRAM MAIN: Execution ended Normally") then
	touch DONE
    else
	touch STOP
	touch ../../../../GEOS-Chem/run/STOP
    endif
else
    sleep 2
endif
end

sleep 60
rm STOP

exit 0

