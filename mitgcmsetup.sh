#!/bin/csh

#setup script for mitgcm runs
cd $workingdir
mkdir verification/
cd verification/

mkdir run/mkdir global_pcb_llc90/ #(if you are running the PCB package)
cd global_pcb_llc90/
mkdir run/
set rundir $workingdir/verification/global_pcb_llc90/run

#6.1 Copy first batch of files
#Copy these folders to verification/:
cp /home/geos_harvard/yanxu/MITgcm/verification/global_oce_cs32 ../

cp /home/geos_harvard/yanxu/MITgcm/verification/global_oce_input_fields ../
/home/geos_harvard/yanxu/MITgcm/verification/global_pcb_llc90/input/
/home/geos_harvard/yanxu/MITgcm/verification/global_pcb_llc90/input.core2
/home/geos_harvard/yanxu/MITgcm/verification/global_pcb_llc90/input.ecco_v4
/home/geos_harvard/yanxu/MITgcm/verification/global_pcb_llc90/input.ecmwf
/home/geos_harvard/yanxu/MITgcm/verification/global_pcb_llc90/input_itXX

#Go into the input_itXX/ directory and update the file paths:
set dirInputFields = $rundir/verification/global_oce_input_fields
setdirLlc90 = /home/geos_harvard/yanxu/MITgcm/verification/global_ocea_llc90

#Execute this command in your run/ directory.
cd $rundir
csh #(note: this command opens a c-shell)
../input_itXX/prepare_run
exit #(note: this closes the c-shell)

#6.2 Link forcing files to your run folder
#Go to your run/ folder:
cd $rundir
ln -s ~gforget/ecco_v4_input/controls/* .
ln -s ~gforget/ecco_v4_input/MITprof/* .
ln -s ~gforget/ecco_v4_input/pickups/* .
ln -s ~gforget/ecco_v4_input/era-interim/* .

#6.3 Forcing folder
#Still in your run/ directory, make a forcing/ subdirectory:
mkdir forcing
#Move all the forcing files insde:
mv EIG* forcing/
mv runoff-2d-Fekete-1deg-mon-V4-SMOOTH.bin forcing/

#6.4 Initial conditions and other forcing files
#Still in your run/ directory, make an initial/ subdirectory:
mkdir initial/
#In this folder, you can put the initial conditions of your tracers. If you need a copy of the initial conditions for the ECCOv4 DARWIN
#simulation, they're available here:
cp /home/yanxu/MITgcm/verification/global_darwin_llc90/run1/initial/* initial/

#6.5 Control files
#Still in your run/ directory, make a control/ subdirectory:
mkdir control
#Move all the control files into this folder
mv wt_* xx_* control/

#6.6 data* files
#If you're running the PCB simulation, copy data* files to your run/ directory from here:
cp /net/fs02/d2/geos_harvard/helen/MITgcm_ECCOv4/verification/global_pcb_llc90/run/data* .
 