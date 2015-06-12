"""Model definitions to be used by the model coupler
thackray@mit.edu
"""

import shutil
import os

def cp(origin, destination):
    shutil.copy(origin, destination)
    return

def cd(destination):
    return os.chdir(destination)

def submit(scriptname):
    return os.system('qsub '+scriptname)

class FileTemplate(object):
    def __init__(self, filename):
        self.filename = filename
        self.content = ''
        return

    def load_template(self, template_path):
        with open(template_path, 'r') as f:
            self.content = f.read()
        return

    def fill_template(self, fill_dict):
        for tag in fill_dict:
            self.set_value(tag, fill_dict[tag])
        return

    def set_value(self, tag, value):
        self.content = self.content.replace(tag, value)
        return

    def write(self, ):
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
        self.rundir = os.path.join(self.rootdir,
                                   str(tstart.date())+str(tstart.hour))
        os.mkdir(self.rundir)
        for fil in self.input_files:
            self._make_input_file(fil,self.rundir)
        cp(self.executable,self.rundir)
        self._make_runscript(self.runscript,
                             os.path.join(self.rundir,
                                          os.path.basename(self.runscript)))
        return
        
    def send_output(self, shared_dir):
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
        for for_model in self.out_for:
            dirname = '%s_to_%s'%(self.name,for_model)
            os.mkdir(os.path.join(shared_dir,dirname))

    def get_input(self, shared_dir):
        for from_model in self.in_from:
            dirname = '%s_to_%s'%(from_model,self.name)
            shared = os.path.join(shared_dir,dirname)
            for fil in os.listdir(shared):
                cp(os.path.join(shared,fil),
                   os.path.join(self.rundir,fil))
        return

    def _make_from_template(self, template, destination, fill_dict):
        F = FileTemplate(destination)
        F.load_template(template)
        F.fill_template(fill_dict)
        F.write()
        return
         
    def go(self,):
        cd(self.rundir)
        submit(self.runscript)
        cd(self.homedir)

class GEOSChem(Model):
    def _make_shared_files(self,):
        # needs to make the dir name_to_for_model, fill it
        pass

    def _make_input_file(self, template, destination):
        pass

    def _make_runscript(self, template, destination):
        pass

class MITgcm(Model):
    def _make_shared_files(self,):
        pass

    def _make_input_file(self, template, destination):
        pass

    def _make_runscript(self, template, destination):
        pass
 
class DummyM(Model):
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

   

