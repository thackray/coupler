function regrid_dep_ll2llc( infile_bpch, GC_path,outfile_gasdep, outfile_partdep, LPLOT )

%=================================================================
% OBJECTIVE
%  Regrid 2D GEOS-Chem atmospheric deposition from a 4x5 lat-lon
%  grid to the MITgcm ECCOv4 lat-lon-cap ("llc90") grid. Write
%  result to binary files to be read by MITgcm as forcing fields. 
%
% INPUTS
%   infile_bpch     : Character string providing filename for the 
%                     GEOS-Chem atmospheric deposition. Must end in 
%                     ".bpch".
%   GC_path         : Character string with filepath to the directory
%                     where infile_bpch is, as well as the tracerinfo.dat
%                     and diaginfo.dat files.
%   outfile_gasdep  : Character string to name regridded gas-phase
%                     deposition to feed to the MITgcm. Must end in
%                     ".bin".
%   outfile_partdep : Character string to name regridded part-phase
%                     deposition to feed to the MITgcm. Must end in
%                     ".bin".
%   LPLOT           : Logical for plotting regridded depostion. 
%                     'TRUE'  will produce plots.
%                     'FALSE' will supress plots. 
%
% NOTES
%   (01) Currently assumes GEOS-Chem output is on a 4x5 global grid.
%   (02) Currently assumes MITgcm output is on a LLC90 grid.
%   (03) You need a copy of Gael Forget's gcmfaces package and Seb
%        Eastham's BPCHFunctions_v2 package.
%
%        gcmfaces available here:
%        /home/geos_harvard/helen/MATLAB/BPCHFunctions_v2/
%
%        BPCHFunctions_v2 available here:
%        http://wiki.seas.harvard.edu/geos-chem/index.php/Matlab_software_tools_for_use_with_GEOS-Chem
%    
%
% REVISION HISTORY
%   25 May 2015 - H. Amos - v1.0 created. 
%
% Helen M. Amos (hamos@hsph.harvard.edu)
%=================================================================

% path to BPCH functions
addpath('/home/geos_harvard/helen/MATLAB/BPCHFunctions_v2/')

%-----------------------------------------------------------------
% read monthly total PCB deposition (kg)
%   --> 2D field
%   --> sum of dry + wet deposition
%   --> dimensions of output are [longitude latitude time]
%-----------------------------------------------------------------

% deposition of gas-phase PCB
disp(' '); disp('Reading GasDep from GEOS-Chem bpch output.');
gasdep_latlon  = readBPCHSingle( [GC_path, infile_bpch],... 
                                 'C_POP_DEPO',...
                                 'T_GasDep',...
                                 [GC_path 'tracerinfo.dat'],...
                                 [GC_path 'diaginfo.dat'],...
                                 true, false );

% deposition of OCPO-phase PCB
disp(' '); disp('Reading OCPODep from GEOS-Chem bpch output.'); 
ocpodep_latlon = readBPCHSingle( [GC_path, infile_bpch],... 
                                 'C_POP_DEPO',...
                                 'T_OCPODep',...
                                 [GC_path 'tracerinfo.dat'],...
                                 [GC_path 'diaginfo.dat'],...
                                 true, false );

% deposition of OCPI-phase PCB
disp(' '); disp('Reading OCPIDep from GEOS-Chem bpch output.'); 
ocpidep_latlon = readBPCHSingle( [GC_path, infile_bpch],... 
                                 'C_POP_DEPO',...
                                 'T_OCPIDep',...
                                 [GC_path 'tracerinfo.dat'],...
                                 [GC_path 'diaginfo.dat'],...
                                 true, false );
% deposition of BCPO-phase PCB
disp(' '); disp('Reading BCPODep from GEOS-Chem bpch output.'); 
bcpodep_latlon = readBPCHSingle( [GC_path, infile_bpch],... 
                                 'C_POP_DEPO',...
                                 'T_BCPODep',...
                                 [GC_path 'tracerinfo.dat'],...
                                 [GC_path 'diaginfo.dat'],...
                                 true, false );

% deposition of BCPI-phase PCB
disp(' '); disp('Reading BCPIDep from GEOS-Chem bpch output.'); 
bcpidep_latlon = readBPCHSingle( [GC_path, infile_bpch],... 
                                 'C_POP_DEPO',...
                                 'T_BCPIDep',...
                                 [GC_path 'tracerinfo.dat'],...
                                 [GC_path 'diaginfo.dat'],...
                                 true, false );

% sum OC and BC deposition
partdep_latlon = ocpodep_latlon + ocpidep_latlon + ...
                 bcpodep_latlon + bcpidep_latlon; 

% ----> Comeback and remove this when coupling is live <----
%
% we'll be regridding/passing one snapshot at a time, so for now
% just take the last time month of GEOS-Chem output and write the
% regridding code with that
gasdep_latlon  = squeeze( gasdep_latlon(:,:,end) );
partdep_latlon = squeeze( partdep_latlon(:,:,end) );

% make sure data is double
gasdep_laton  = double(gasdep_latlon);
partdep_laton = double(partdep_latlon);


%-----------------------------------------------------------------
% GEOS-Chem 4x5 grid information
%
% lat and lon from GEOS-Chem Users' Guide:
% http://acmg.seas.harvard.edu/geos/doc/man/
%-----------------------------------------------------------------

% load lat-lon grid info
GC_gridinfo

% grid box surface area
% ** Hannah's sending it to me ** (hma, 27 may 2015)

% ----> Comeback when you have SA from Hannah  <----
%
% convert deposition from units of kg to kg/m2/sec

%=================================================================
% Regrid 2D GEOS-Chem 4x5 lat-lon output to MITgcm ECCOv4 llc90 
%=================================================================

% add gcmfaces library
addpath( genpath('/home/geos_harvard/helen/MATLAB/gcmfaces/gcmfaces/') )

% load ECCOv4 grid information
grid_load('/home/geos_harvard/helen/MATLAB/gcmfaces/GRID/',5,'compact');

% remap lat-lon to llc90
disp('Regridding lat-lon deposition to llc90.'); disp(' ');
gasdep_llc90  = gcmfaces_remap_2d( lon_gc, lat_gc, gasdep_latlon , 4 );
partdep_llc90 = gcmfaces_remap_2d( lon_gc, lat_gc, partdep_latlon, 4 );

% write llc90 file to binary to feed into MITgcm
disp('Writting llc90 deposition to binary.'); disp(' ');
write2file( outfile_gasdep , convert2gcmfaces( gasdep_llc90  ) );
write2file( outfile_partdep, convert2gcmfaces( partdep_llc90 ) );

% success message
disp('Regridding lat-lon to llc90 was a success!'); disp(' ');


%-----------------------------------------------------------------
% Visual check that regridding didn't produce garbarge
%-----------------------------------------------------------------

if strcmp( LPLOT, 'TRUE' )
  figure (1)
  m_map_gcmfaces( gasdep_llc90 );
  title('GAS DEP')

  figure (2)
  m_map_gcmfaces( partdep_llc90 );
  title('PART DEP')
end
