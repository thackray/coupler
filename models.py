"""Model definitions to be used by the model coupler.
Contents:
Convenience functions:
   - cp, cd : file operations
   - submit : submit script to queue
   - format_time : make the coupler's datetime fit a model's time format
Class definitions:
   - FileTemplate : object to read and fill templates with specifics for each
                    model run
   - Model : parent object to control all the general methods of the models
   - GEOSChem : child object uses Model's methods plus more specifics
   - MITgcm : child object uses Model's methods plus more specifics
   - DummyM : child object from test phase.
 
thackray@mit.edu
"""

import shutil
from datetime import datetime, timedelta
import os
import time
from coupler import check_state
from templates import FileTemplate
# Convenience functions to help make things easier to follow in the code. 

def cp(origin, destination):
    shutil.copy(origin, destination)
    return

def cd(destination):
    return os.chdir(destination)

def submit(scriptname):
    return os.system('qsub '+scriptname)

def submit_prequeued(pathname, code='GO'):
    os.system('touch '+os.path.join(pathname,code))
    return 

def format_time(dtime,out_type='str',abststart=None):
    """Change the time to the format that a particular model likes."""
    if out_type.lower() in ['str','string']:
        return dtime.strftime()
    elif out_type.lower() in ['gc','geos-chem', 'gchem', 'geoschem']:
        return dtime.strftime('%Y%m%d %H%M%S')
    elif out_type.lower() in ['mg', 'mitgcm', 'mit-gcm', 'mgcm']:
        assert abststart, "must give absolute start date and time"
        hours = int((dtime-abststart).total_seconds()/3600.)
        return '%.10i'%hours
    elif out_type.lower() in ['restart']:
        return dtime.strftime('%Y%m%d%H')

def put_a_three(date):
    template = "Schedule output for JAN : 3000000000000000000000000000000\nSchedule output for FEB : 30000000000000000000000000000\nSchedule output for MAR : 3000000000000000000000000000000\nSchedule output for APR : 300000000000000000000000000000\nSchedule output for MAY : 3000000000000000000000000000000\nSchedule output for JUN : 300000000000000000000000000000\nSchedule output for JUL : 3000000000000000000000000000000\nSchedule output for AUG : 3000000000000000000000000000000\nSchedule output for SEP : 300000000000000000000000000000\nSchedule output for OCT : 3000000000000000000000000000000\nSchedule output for NOV : 300000000000000000000000000000\nSchedule output for DEC : 3000000000000000000000000000000"

    firstdayspot = 26 # number of characters from left   
    """Puts a three on the last day of a run for GEOS-Chem's silly 
    output system.
    """
    template = template.splitlines()
    imonth = date.month - 1
    iday = date.day
    template[imonth]=template[imonth][:25+iday]+'3'+template[imonth][26+iday:]
    return '\n'.join(template)


class Model(object):
    """Highest-level Model object for use in the Coupler class.

    Required Attributes:
    name - string
    rundir - name of current run directory, made by setup()
    done_tag - filename that indicates model finished
    running_tag - filename that indicates model is running
    error_tag - filename that indicates model crashed
    in_from - list of other models this one needs to get input from
    out_for - list of other models this one needs to make output for
    runscript - name of script to run this model if the inputs are set up

    Required Methods:
    setup(tstart, tend) - set model up for run from tstart to tend, define new
                          rundir
    go() - submit model run to queue, collect output needed by other
                     models listed in output_for
    get_input() - get inputs corresponding to other models' outputs
    """

    def __init__(self, modelinfo):
        """Unpack modelinfo dictionary to define relevant attributes"""
        self.homedir = os.getcwd()
        self.name = modelinfo['Name']
        self.rootdir = modelinfo['rootdir']
        self.shared_dir = os.path.join(self.rootdir,'shared')
        self.in_from = modelinfo['in_from']
        self.out_for = modelinfo['out_for']
        self.input_files = modelinfo['input_files']
        self.share_script = modelinfo['share_script']
        self.mat_output_files = modelinfo['mat_output_files']
        self.rundirname = modelinfo['rundirname']
        self.abststart = None
        self.rundir = os.path.join(self.rootdir,self.rundirname)

    def _do_more_init(self,):
        """Defined, if needed, in children"""
        return

    def setup(self, tstart, tend):
        """Do the general setup procedures. Procedures speific to the 
        individual models should not be defined here.
        """
        if not self.abststart:
            self.abststart = tstart
        self.tstart = tstart
        self.tend = tend
        self._do_more_init()
        for fil in self.input_files:
            self._make_input_file(os.path.join('templates',fil),
                                  os.path.join(self.rundir,fil))
        return
        
    def send_output(self, shared_dir):
        """Send outout from this model to the shared directory for use by 
        other coupled members.
        """
        print "Copying files. Maybe move the copying to a submitted job?"
        self._make_shared_files()
        for for_model in self.out_for:
            dirname = '%s_to_%s'%(self.name,for_model)
            localdirname = os.path.join(self.rundir,dirname)
            for fil in os.listdir(localdirname):
                cp(os.path.join(localdirname,fil),
                   os.path.join(self.shared_dir,dirname,fil))
        return

    def init_shared(self, shared_dir):
        """Make a directory to put shared info in."""
        for for_model in self.out_for:
            dirname = '%s_to_%s'%(self.name,for_model)
            if not os.path.exists(os.path.join(shared_dir,dirname)):
                os.mkdir(os.path.join(shared_dir,dirname))

    def get_input(self, shared_dir):
        """Get info from other models from shared_dir."""
        for from_model in self.in_from:
            dirname = '%s_to_%s'%(from_model,self.name)
            shared = os.path.join(shared_dir,dirname)
            for fil in os.listdir(shared):
                cp(os.path.join(shared,fil),
                   os.path.join(self.rundir,fil))
        return

    def _make_from_template(self, template, destination, fill_dict):
        """Wrapper for template functions."""
        F = FileTemplate(destination)
        F.load_template(template)
        F.fill_template(fill_dict)
        F.write()
        return

    def _make_shared_files(self,):
        "Make file(s) to be traded with other models"
        for for_model in self.out_for:
            dirname = '%s_to_%s'%(self.name,for_model)
            localdirname = os.path.join(self.rundir,dirname)
            if not os.path.exists(localdirname):
                os.mkdir(localdirname)
            self._make_from_template(os.path.join('templates',
                                                  self.share_script),
                                     os.path.join(self.rundir,
                                                  self.share_script),
                                     self._make_shared_dict())
            cd(self.rundir)
            submit_prequeued(self.rundir,code='SEND')
            cd(self.rootdir)
            while not check_state(self.rundir,'SENDING'):
                time.sleep(5)
            while not check_state(self.rundir,'SENT'):
                time.sleep(5)
#            for outputname in self.mat_output_files: 
#                cp(outputname,os.path.join(localdirname,outputname))

        return

    def go(self,):
        """Run the model."""
        #cd(self.rundir)
        #submit(self.runscript)
        submit_prequeued(self.rundir)
        cd(self.homedir)
        return

    def stop(self,):
        """Stop the model job."""
        submit_prequeued(self.rundir,code='STOP')
        return

class GEOSChem(Model):
    """Child object for GEOSChem specifically. Defines how GEOSChem does the
    specific operations. 

    Arguments:
       - modelinfo: model info dictionary for Model object.
    
    Methods:
       - _make_shared_dict: used by Model's _make_shared_files
       - _make_input_file: make filled input.geos file
       - _make_runscript: make runscript for GEOSChem
    """

    def _do_more_init(self,):
        self.bpch_name = 'PCB%s.bpch'%format_time(self.tend,'restart')

    def _make_shared_dict(self,):
        "Make fill_dict for shared_script"
        fill_dict = {'@GCPATH':self.rundir,
                     '@GCFILE':self.bpch_name,
                     '@GCYEAR':str(self.tstart.year),
                     '@GCMONTH':str(self.tstart.month)
                     }
                     
        return fill_dict

    def _make_input_file(self, template, destination):
        outputschedule = put_a_three(self.tend)
        fill_dict = {'@STARTTIME':format_time(self.tstart,'GC'),
                     '@ENDTIME':format_time(self.tend,'GC'),
                     '@BPCHNAME':self.bpch_name,
                     '@RESTARTTIME':format_time(self.tstart,'restart'),
                     '@OUTPUTSCHEDULE':outputschedule
                     }
        self._make_from_template(template, destination, fill_dict)
        return


class MITgcm(Model):
    """Child object for MITgcm specifically. Defines how MITgcm does the
    specific operations. 

    Arguments:
       - modelinfo: model info dictionary for Model object.
    
    Methods:
       - _make_shared_dict: used by Model's _make_shared_files
       - _make_input_file:
       - _make_runscript: make runscript for MITgcm
    """

    def _make_shared_dict(self,):
        "Make fill_dict for shared_script"
        fill_dict = {'@OCNPATH':os.path.join(self.rundir,'diags'),
                     '@OCNDIAG':'PCBaEVAS',
                     '@LLC90TIME':format_time(self.tend,'MG',
                                              self.abststart)
                     }
                     
        return fill_dict

    def _make_input_file(self, template, destination):
        tadj = timedelta(hours=1)
        fill_dict = {'@RUNDIR':self.rundir,
                     '@STARTTIME':str(int(format_time(self.tstart,
                                                      'MG',self.abststart))+1),
                     '@TIMESTEP':str(int(format_time(self.tend,
                                                 'MG',self.tstart))),
                     '@HOURTIMESTEP':str(int(format_time(self.tend,
                                                 'MG',self.tstart))*3600),
                     '@PICKUPSTEP':str(int(format_time(self.tend,
                                                    'MG',self.tstart))*3600),
                     }
        if self.tstart==self.abststart:
            fill_dict['@PICKUPSUFF'] = '#'
        else:
            fill_dict['@PICKUPSUFF'] = "pickupSuff='%s'"%\
                format_time(self.tstart, 'MG', self.abststart)
        self._make_from_template(template, destination, fill_dict)
        return

 
