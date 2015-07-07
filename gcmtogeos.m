clear all; close all; 

%=================================================================
% OBJECTIVE
%   Driver for series of functions that allows you to regrid GEOS-
%   Chem output to MITgcm and vice versa. 
%
% NOTES
%   (01) Currently assumes GEOS-Chem output is on a 4x5 global grid.
%   (02) Currently assumes MITgcm output is on a LLC90 grid.
%   (03) You need a copy of two MATLAB packages:
%
%        gcmfaces available here:
%          /home/geos_harvard/helen/MATLAB/BPCHFunctions_v2/
%
%        BPCHFunctions_v2 available here:
%          http://wiki.seas.harvard.edu/geos-chem/index.php/Matlab_
%          software_tools_for_use_with_GEOS-Chem
%    
%
% REVISION HISTORY
%   25 May 2015 - H. Amos - v1.0 created. 
%
% Helen M. Amos (hamos@hsph.harvard.edu)
%=================================================================

%-----------------------------------------------------------------
% Regrid evasion: llc90 --> lat-lon
%-----------------------------------------------------------------

% read MITgcm evasion (units?)
%ocnpath       = '/net/fs02/d2/geos_harvard/helen/MITgcm_ECCOv4/verification/global_pcb_llc90/run/';
ocnpath       = '@OCNPATH/'
%ocndiag       = 'PTRACER01'; % this is a placeholder for EVASION diagnostic
ocndiag       = '@OCNDIAG'
%time_llc90    = 9;           % <-- this has to be updated every timestep we
                             %     pass information from the ocean to atmosphere
time_llc90    = @LLC90TIME

% name of netcdf file containing regridded evasion to pass to GEOS-Chem
outfile_evas = 'evasion_latlon.nc';

% regrid MITgcm evasion from llc90 to GEOS-Chem 4x5 lat-lon grid
regrid_evas_llc2ll( ocnpath, ocndiag, time_llc90, outfile_evas, 'TRUE' )
