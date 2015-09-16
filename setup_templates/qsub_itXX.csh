#!/bin/csh
#
#PBS -l nodes=13:sandy
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
    touch DONE
else
    sleep 2
endif
end
exit 0

