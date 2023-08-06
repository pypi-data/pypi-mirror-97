import os
import pickle


class FESReporter(object):
    """
    Custom reporter for saving the FES and CV values to files as output from metadynamics simulation
    """
    def __init__(self,file,reportInterval,metaD_wrapper,CV_list,
                 potentialEnergy=False, kineticEnergy=False,
                 totalEnergy=False, temperature=False):

        self._reportInterval = reportInterval
        self.metaD_wrapper = metaD_wrapper
        self.CV_list = CV_list
        self._out = file
        self._hasInitialized = False
        self._needsPositions = True
        self._needsVelocities = False
        self._needsForces = False
        self._needEnergy = potentialEnergy or kineticEnergy or totalEnergy or temperature

    def _initialize(self, simulation):
        """Deferred initialization of the reporter, which happens before
        processing the first report."""

        self.CV_values = []
        self.free_energy = []

        self._hasInitialized = True

    def report(self, simulation, state):
        """Generate a report.

        Parameters
        ----------
        simulation : simtk.openmm.app.Simulation
            The Simulation to generate a report for

        """
        if not self._hasInitialized:
            self._initialize(simulation)
            self._hasInitialized = True

        self.CV_values.append(self.metaD_wrapper.getCollectiveVariables(simulation))
        self.free_energy.append(self.metaD_wrapper.getFreeEnergy())

        # Save free energy and CV files periodically
        with open(os.path.join(self._out,'CV_values.pickle'), 'wb') as cv_pickle:
            pickle.dump(self.CV_values, cv_pickle)

        with open(os.path.join(self._out,'fes.pickle'), 'wb') as fes_pickle:
            pickle.dump(self.free_energy, fes_pickle)

    def describeNextReport(self, simulation):
        """Get information about the next report this object will generate.

        Parameters
        ----------
        simulation : simtk.openmm.app.Simulation
            The Simulation to generate a report for

        Returns
        -------
        report_description : tuple
            A five element tuple.  The first element is the number of steps
            until the next report.  The remaining elements specify whether
            that report will require positions, velocities, forces, and
            energies respectively.
        """
        steps = self._reportInterval - simulation.currentStep % self._reportInterval
        return (steps, self._needsPositions, self._needsVelocities, self._needsForces, self._needEnergy)
