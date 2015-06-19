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
import datetime
import os

# Convenience functions to help make things easier to follow in the code. 

def cp(origin, destination):
    shutil.copy(origin, destination)
    return

def cd(destination):
    return os.chdir(destination)

def submit(scriptname):
    return os.system('qsub '+scriptname)

def format_time(dtime,out_type='str'):
    """Change the time to the format that a particular model likes."""
    if out_type.lower() in ['str','string']:
        return datetime.whatever(dtime,formt)
    if out_type.lower() in ['gc','geos-chem', 'gchem', 'geoschem']:
        return whatever
    if out_type.lower() in ['mg', 'mitgcm', 'mit-gcm', 'mgcm']:
        return whatever


class FileTemplate(object):
    """Governs the reading and filling of file templates.
    Arguments:
       - filename: name of file that will eventually be written to

    Methods:
       - load_template: load given template for filling
       - fill_template: fill template using dictionary of fillers
       - set_value: replace a single tag with a filler
       - write: save file with previously defined replacements
    """

    def __init__(self, filename):
        "Save filename to write to and initialize content."
        self.filename = filename
        self.content = ''
        return

    def load_template(self, template_path):
        "Load template from given path to memory to be filled"
        with open(template_path, 'r') as f:
            self.content = f.read()
        return

    def set_value(self, tag, value):
        """Replace tag in template with value. 
        e.g. set_value('@USERNAME','thackray')
        """
        self.content = self.content.replace(tag, value)
        return

    def fill_template(self, fill_dict):
        """Take a dictionary of tag:value pairs and use them to fill template"""
        for tag in fill_dict:
            self.set_value(tag, fill_dict[tag])
        return

    def write(self, newfilename=None):
        """Save filled template to location newfilename. If newfilename is not
        given, save to location given in object initilization.
        """
        if newfilename:
            self.filename = newfilename
        with open(self.filename, 'w') as f:
            f.write(self.content)
            

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
        self.done_tag = modelinfo['done_tag']
        self.running_tag = modelinfo['running_tag']
        self.error_tag = modelinfo['error_tag']
        self.in_from = modelinfo['in_from']
        self.out_for = modelinfo['out_for']
        self.runscript = modelinfo['runscript']
        self.input_files = modelinfo['input_files']
        self.executable = modelinfo['executable']

    def setup(self, tstart, tend):
        """Do the general setup procedures. Procedures speific to the 
        individual models should not be defined here.
        """
        self.rundir = os.path.join(self.rootdir,
                                   str(tstart.date())+str(tstart.hour))
        self.tstart = tstart
        self.tend = tend
        os.mkdir(self.rundir)
        for fil in self.input_files:
            self._make_input_file(fil,self.rundir)
        cp(self.executable,self.rundir)
        self._make_runscript(self.runscript,
                             os.path.join(self.rundir,
                                          os.path.basename(self.runscript)))
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
         
    def go(self,):
        """Run the model."""
        cd(self.rundir)
        submit(self.runscript)
        cd(self.homedir)

class GEOSChem(Model):
    """Child object for GEOSChem specifically. Defines how GEOSChem does the
    specific operations. 

    Arguments:
       - modelinfo: model info dictionary for Model object.
    
    Methods:
       - _make_shared_files: send outputs for other models
       - _make_input_file: make filled input.geos file
       - _make_runscript: make runscript for GEOSChem
    """

    def _make_shared_files(self,):
        for for_model in self.out_for:
            dirname = '%s_to_%s'%(self.name,for_model)
            localdirname = os.path.join(self.rundir,dirname)
            os.mkdir(localdirname)
        # needs to make the dir name_to_for_model, fill it
        pass

    def _make_input_file(self, template, destination):
        fill_dict = {'@STARTTIME':format_time(self.tstart,'GC'),
                     '@ENDTIME':format_time(self,tend,'GC'),
                     }
        self._make_from_template(template, destination, fill_dict)
        return

    def _make_runscript(self, template, destination):
        fill_dict = {'@RUNDIR':self.rundir}
        self._make_from_template(template, destination, fill_dict)
        return

class MITgcm(Model):
    """Child object for MITgcm specifically. Defines how MITgcm does the
    specific operations. 

    Arguments:
       - modelinfo: model info dictionary for Model object.
    
    Methods:
       - _make_shared_files: send outputs for other models
       - _make_input_file:
       - _make_runscript: make runscript for MITgcm
    """

    def _make_shared_files(self,):
        for for_model in self.out_for:
            dirname = '%s_to_%s'%(self.name,for_model)
            localdirname = os.path.join(self.rundir,dirname)
            os.mkdir(localdirname)
        # needs to make the dir name_to_for_model, fill it
        return

    def _make_input_file(self, template, destination):
        fill_dict = {'@RUNDIR':self.rundir,
                     '@STARTTIME':format_time(self.tstart,'MG'),
                     '@ENDTIME':format_time(self.tend,'MG'),
                     }
        self._make_from_template(template, destination, fill_dict)
        return

    def _make_runscript(self, template, destination):
        fill_dict = {'@RUNDIR':self.rundir}
        self._make_from_template(template, destination, fill_dict)
        return
 
class DummyM(Model):
    """Was using this for building the general coupling stuff."""
    def _make_shared_files(self,):
        for for_model in self.out_for:
            dirname = '%s_to_%s'%(self.name,for_model)
            localdirname = os.path.join(self.rundir,dirname)
            os.mkdir(localdirname)
        # needs to make the dir name_to_for_model, fill it
        pass

    def _make_input_file(self, template, destination):
        cp(template, destination)
        return

    def _make_runscript(self, template, destination, ):
        fill_dict = {'@RUNDIR':self.rundir}
        self._make_from_template(template, destination, fill_dict)
        return

   

