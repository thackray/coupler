#!/bin/csh -f
#
#PBS -l nodes=13:sandy
#PBS -N test_mitgcm
#PBS -j oe
#PBS -q xlong
source /etc/profile.d/modules.csh

module add gcc
module add intel
module add netcdf/20130909
module add openmpi/1.7.2

setenv MPI_INC_DIR /home/software/intel/intel-2013_sp1.0.080/pkg/openmpi/openmpi-1.7.2/include/
setenv NETCDF_ROOT /home/software/intel/intel-2013_sp1.0.080/pkg/netcdf/netcdf-20130909/

cd @RUNDIR
while ( ! -e STOP )
if ( -e GO ) then 
    rm GO
    rm MGdone
    touch MGrunning
    mpirun -np 13 ./@EXECUTABLE
    rm MGrunning
    touch MGdone
else
    sleep 2
endif
end
exit 0

