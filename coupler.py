"""MITgcm + GEOS-Chem coupler used for PCB simulations (and PFCs in the future)
"""
import sys
import os
import time
from datetime import datetime, timedelta


def check_state(path,state_tag):
    print "Checking for state tag ( %s ) in %s"%(state_tag,path)
    result = (state_tag in os.listdir(path))
    print result
    return result

class Coupler(object):
    """Coupler for coupling two (or more?) models. Will handle the 
    initialization, running, info swapping, etc. for the coupled runs.
    """
    def __init__(self, start_time, end_time, coupled_timestep,
                 model_objs=[], check_frequency=5*60):
        """Initialize Coupler object.

        Arguments:
        start_time - datetime object corresponding to start
        end_time - datetime object corresponding to end
        coupled_timestep - timestep in HOURS for the models swapping info

        Keyword Arguments:
        model_objs - list containing Model objects of models to be coupled, 
                    default value = empty list
        check_frequency - number of SECONDS to sleep between state checks,
                          default value = 5 mins
        """

        self.tstart = start_time
        self.tend = end_time
        self.dt = timedelta(hours=coupled_timestep)
        self.models = model_objs
        self.check_frequency = check_frequency
        return

    def startup(self,):
        """Perform the operations needed to prepare for the run stage."""
        # make temp store for shared data
        self.shared_dir = 'shared' # location of shared data
        if not os.path.exists(self.shared_dir):
            os.mkdir(self.shared_dir)
        # then make subdir for model to/froms
        for model in self.models:
            model.init_shared(self.shared_dir)
        # check for necessary templates from models
        return

    def run(self, ):
        """Run the coupled models."""
        self.tcurrent = self.tstart
        while (self.tcurrent < self.tend) and not check_state(models[0].rundir,
                                                          'STOP'):
            print self.tcurrent
            self.tnext = self.tcurrent + self.dt
            self._prep_models(self.tcurrent, self.tnext)
            self._run_models()
            DONE = False
            while not DONE:
                DONE = True
                for model in self.models:
                    DONE *= check_state(model.rundir, 'DONE')
                time.sleep(self.check_frequency)
            self._swap_info()
            self.tcurrent = self.tnext
        self._cleanup()
        return 

    def _prep_models(self, mini_tstart, mini_tend):
        """Prep the models for the next chunk of running."""
        for model in self.models:
            model.setup(mini_tstart, mini_tend)
            model.get_input(self.shared_dir)
        return

    def _run_models(self, ):
        """Tell the models to run and check that they are running."""
        for model in self.models:
            model.go()
        RUNNING = False
        isrunning = {}
        for model in self.models:
            isrunning[model] = False
        while not RUNNING:
            RUNNING = True
            for model in self.models:
                if not isrunning[model]:
                    isrunning[model] = check_state(model.rundir, 
                                                   'RUNNING') 
                RUNNING *= isrunning[model]
            time.sleep(self.check_frequency)
        return

    def _swap_info(self,):
        """Tell the models to send their output to shared location."""
        for model in self.models:
            model.send_output(self.shared_dir)
        return


    def _cleanup(self, ):
        """Submit the cleanup job to group the outputs, remove temps, etc."""  
        for model in self.models:
            model.stop()
        print "All Done! Thanks for using coupler.py"
        return


