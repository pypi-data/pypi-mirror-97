import os
import pickle
import random
import re

import mdtraj
import numpy as np
from scipy.spatial import distance

from simtk.openmm import unit

from .ommtk import MetadynamicSimulation


class SegmentMappingSim(MetadynamicSimulation):
    """
    This is a specialized version of the metaD simulation that runs a short run with a high bias,
    saves the coordinates and CV values and uses them to seed a forced sampling of the unbinding pathway
    (without previous knowledge of needed restraints. It begins a run with scan bias, and continues in .5ns
    intervals until the distance CV has reached the value of the unbound_distance variable.

    Once the distance is reached, suitable (equidistant in CV distance space) frames are chosen to represent the
    unbinding pathway and used as seeds for a sequential multiple walkers metaD run.

    Params

    num_segs int
        number of segments along the unbinding pathway to seed
    seg_sim_time unit.Quantity
        length of simulation time to spend in each segment
    scan_bias int
        initial bias_factor for scan portion of the protocol
    scan_time unit.Quantity
        time to run the initial scan
    unbound_distance unit.quantity
        estimate of the max value of the CV. Can be determined using find_max_distance in utils

    """
    def __init__(self, num_segs_per_replica = 10, seg_sim_time=.5 * unit.nanosecond, scan_bias=40,
                 scan_time = 1 * unit.nanosecond, scan_bias_freq= .5 * unit.picosecond,
                 max_scan_time=6 * unit.nanosecond, prod_bias=5, prod_bias_freq = 1 * unit.picosecond,
                 scan_bias_height=2.5 * unit.kilojoules_per_mole, prod_bias_height= 2 * unit.kilojoule_per_mole,
                 num_replicas=1, CV2_target_range = None,
                 total_production_time = 100 * unit.nanosecond, **kwargs):

        super().__init__(**kwargs)


        #setup init vars
        self.num_segs = num_segs_per_replica
        self.seg_sim_time = seg_sim_time
        self.scan_bias = scan_bias
        self.scan_time = scan_time
        self.scan_bias_freq = int(scan_bias_freq/self.step_length)
        self.scan_bias_height = scan_bias_height
        self.max_scan_time = max_scan_time
        self.prod_bias = prod_bias
        self.prod_bias_freq = int(prod_bias_freq/self.step_length)
        self.num_replicas = num_replicas
        self.total_production_time = total_production_time
        self.prod_bias_height = prod_bias_height


        self.CV2_target_range = CV2_target_range


        for cv in self.CV_list:
            if cv[0]=='Distance' and cv[4]<self.unbound_distance:
                self.unbound_distance=cv[4]
                print("""Warning, Distance CV upper bound set to less than unbound distance, replacing
                unbound_distance with max distance CV, new value is {}""".format(cv[4]))

        if self.CV_list[0][0]!='Distance':
            raise ValueError('Segment Map Sim where the first CV is not distance not yet supported')

        if self.scan_bias < self.prod_bias:
            print('WARNING: scan bias should be high (40-50) and prod bias should be low (5-10)')



    def run(self):
        """
        Run the segment mapping protocol defined by input variables.

        :return: updated parmed.Structure object
        """

        self._remove_custom_forces()
        self.bias_factor = self.scan_bias
        self.bias_save_frequency = self.scan_bias_freq * 50
        self.bias_frequency = self.scan_bias_freq
        self.initial_bias_height=self.scan_bias_height
        self._build_custom_forces()

        print('saving coords')
        initial_coords = self.positions

        scan_times = []
        segment_coords = []
        chosen_CVs_all_replicas = []
        for i in range(self.num_replicas):

            print('Starting scan run for replica {}'.format(i+1))

            self.simulation.context.reinitialize()
            self.simulation.context.setPositions(initial_coords)

            nsteps = int(self.scan_time / self.step_length)

            #fix the reporter intervals to make sure there are enough frames for populating replicas
            #this also ensures that the CV value matches the trajectory frame by index

            self._add_reporters(total_steps=nsteps + self.simulation.currentStep, traj_interval= .01 * unit.nanosecond)
            self._add_FESReporter(fes_interval=.01 * unit.nanosecond)

            self.metaD.step(self.simulation, nsteps)
            self.update_parmed()

            #continually run .5ns runs until distance CV exceeds unbound_distance
            with open(os.path.join(self.cwd, 'CV_values.pickle'), 'rb') as handle:
                CVs = pickle.load(handle)

            distances = np.array(CVs)[:, 0]

            scan_clock = self.scan_time
            while all(distances < distances[0]+self.unbound_distance) and  scan_clock<self.max_scan_time:

                print('failed to unbind, scanning for another .5 ns')
                print('CV distance range {} to {}'.format(distances[0],np.max(distances)))
                scan_clock += .5 * unit.nanosecond
                nsteps = int(.5 * unit.nanosecond / self.step_length)

                self.metaD.step(self.simulation, nsteps)

                with open(os.path.join(self.cwd,'CV_values.pickle'), 'rb') as handle:
                    CVs = pickle.load(handle)
                distances = np.array(CVs)[:, 0]
            else:
                if scan_clock<self.max_scan_time:
                    scan_times.append(scan_clock)
                    print('ligand reached unbinding distance in {}, proceeding with forced sampling'.format(scan_clock))
                else:
                    scan_times.append(scan_clock)
                    print('failed to unbind in max_scan_time, proceeding anyway')


            print('distances from scan: {}'.format(distances))

            self.simulation.reporters.clear()

            # find traj frames where the CV is evenly spaced along num_seg segments in distance CV but
            # but optionally constrain CV2 values to a uniform distribution within a specified range
            distance_targets = np.linspace(np.min(distances), self.unbound_distance, self.num_segs)
            if self.CV2_target_range:
                #make sure min and max aren't outside the CV range
                min = np.max([self.CV_list[1][3],CVs[0][1]-self.CV2_target_range])
                max = np.min([CVs[0][1]+self.CV2_target_range,self.CV_list[1][4]])
                CV2_targets = np.random.uniform(min,max,self.num_segs)
                print('CV2_targets',CV2_targets)

            segment_frames = []
            chosen_CVs = []
            for k,target in enumerate(distance_targets):
                if self.CV2_target_range:
                    idx = np.argmin(distance.cdist([(target, CV2_targets[k])], CVs))
                else:
                    idx = (np.abs(distances - target)).argmin()
                #if idx is already in the list, try 100 times to choose another with similar value
                counter=0
                while idx in segment_frames and counter<100:
                    counter+=1
                    target+=random.randint(-100,100)* .01
                    if self.CV2_target_range:
                        idx = np.argmin(distance.cdist([(target, CV2_targets[k])], CVs))
                    else:
                        idx = (np.abs(distances - target)).argmin()
                segment_frames.append(idx)
                chosen_CVs.append(distances[idx])
                print('choosing CV values {} {}'.format(idx,CVs[idx]))

            #load trajectory and slice for chosen frames
            traj = mdtraj.load_hdf5(os.path.join(self.cwd,self.traj_out))
            segment_coords.append(traj.xyz[segment_frames])
            chosen_CVs_all_replicas.append(chosen_CVs)

            #now we have the coordinates we use for seeding, get the seg steps and delete the bias file and previous
            #objects
            pattern = re.compile('bias(.*)\.npy')
            matches = [pattern.match(filename) for filename in os.listdir(self.cwd) if pattern.match(filename)!=None]
            bias_file = os.path.join(self.cwd, matches[-1].string)
            os.remove(bias_file)
            self.simulation.reporters.clear()

        with open(os.path.join(self.cwd,'scan_coords.pickle'), 'wb') as handle:
            pickle.dump(segment_coords, handle)

        with open(os.path.join(self.cwd,'scan_times.pickle'), 'wb') as handle:
            pickle.dump(scan_times, handle)

        # remove and rebuild the metaD wrapper force with the new metaD params
        self._remove_custom_forces()
        self.bias_factor = self.prod_bias
        self.bias_save_frequency = self.prod_bias_freq * 100
        self.bias_frequency = self.prod_bias_freq
        self.initial_bias_height = self.prod_bias_height
        self._build_custom_forces()

        #sometimes restarts show instability and lead to hangs on startup so we minimize just to be safe
        self.simulation.minimizeEnergy()

        #get total num steps for reporters
        nsteps = int(round(self.total_production_time/self.step_length))
        print('nsteps for production phase',nsteps)
        self.simulation.reporters = []
        self._add_reporters(total_steps = nsteps + self.simulation.currentStep)
        self._add_FESReporter()



        total_scan_time = np.sum(scan_times)

        #loop across all replicas
        for replica in range(self.num_replicas):
            print('starting replica {}'.format(replica+1))
            replica_seg_time= scan_times[replica]* (self.total_production_time/(total_scan_time* self.num_segs))
            replica_seg_steps = int(round(replica_seg_time/self.step_length))
             #loop across the segments with chosen frames running short sims and writing to the bias
            for i,frame in enumerate(segment_coords[replica]):
                print('replica {}: swapping in coordinates for CV value {} from frame {}'.format(replica+1,
                                                    chosen_CVs_all_replicas[replica][i],i+1))
                self.simulation.context.setPositions(frame * unit.nanometers)
                self.metaD.step(self.simulation, replica_seg_steps)

        self.simulation.reporters.clear()

        self.update_parmed()

        if self.total_production_time==0* unit.nanosecond:
            self._write_coordinates_to_h5(os.path.join(self.cwd, self.traj_out))
            print("Warning: DID NOT RUN ANY PRODUCTION")

        return self.parmed_structure
