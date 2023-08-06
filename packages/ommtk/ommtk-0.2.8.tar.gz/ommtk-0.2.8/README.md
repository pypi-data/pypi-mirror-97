# OMMTK
## OpenMM Wrappers for General and Enhanced MDSimulations

This repo contains several simulation classes wrapped around openMM infrastructure that allow for rapid devlopment and usage of various MD Simulations.

Currently Supported are the following simulations: Minimization, Standard MD (base class); Heating and Equil MD simulations (NVT and NPT respectively), Gentle Heat Sims (heat/release restraints over a range of stages), simulated tempering, metadynamics and metadynamics with focused sampling on ligand unbinding (Segment Walker Sims). The simulations support a full API with a range of functions and easily adapted run statements for specialized protocols.  

# Installation

Dependencies:

OMMTK requires very few dependencies. Below is a list you can install with conda or pip:

    python 3.6 or higher
    simtk.openmm
    numpy
    mdtraj
    
To install the latest stable version we recommend using pip with the following command (this is the only method guaranteed to provide a stable version).

    pip install ommtk
  
# Documentation

The most recent documentation: https://redesignscience.github.io/OMMTK/

## Quickstart run

        # Load packages
        import parmed
        from ommtk import MDSimulation, select_atoms, unit
        
        # Note: Requires parameterized parmed in memory named parmed_structure!

        #instantiate sim from parmed alone, minimize (save h5 file) and run
        mdsim = MDSimulation(parmed_structure=parmed_structure)
        mdsim.minimize()
        minimized_parmed = mdsim.run(2 * unit.nanosecond)

        #build sim using a previous trajectory or h5 file
        mdsim = MDSimulation(parmed_structure=parmed_structure, coordinates=trajectory.h5)

        #build sim with positional restraints, run some equilibration and remove them for longer run
        protein_atoms = select_atoms(parmed_structure=parmed_structure, keyword_selection='protein')
        mdsim = MDSimulation(parmed_structure=parmed_structure, atoms_to_restrain=protein_atoms, restraint_weight=4)
        mdsim.run(1*unit.nanosecond)
        mdsim.update_restraint_weight(2)
        mdsim.run(1*unit.nanosecond)
        mdsim.remove_positional_restraints()
        end_parmed = mdsim.run(4 * unit.nanosecond)
