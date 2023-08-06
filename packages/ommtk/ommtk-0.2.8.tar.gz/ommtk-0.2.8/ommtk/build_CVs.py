
import simtk.openmm as mm

from .utils import *


def build_CVs(CV_list, parmed_structure, system):
    CVs = []
    bin_lengths = []
    # cv list format will be:
    #       cv[0] = cv name
    #       cv[1] = atom_selection1 (should be ligand if using both) or list of atom indeces
    #       cv[2] = atom_selection2 (should be protein if possible) or list of atom indeces
    #       cv[3] = cv min value
    #       cv[4] = cv max value
    #       cv[5] = cv bin width
    #       cv[6] = list of group weights (CN and WD only)
    #       cv[7] = list of decay lengths (CN only)

    print('Building collective variables with the following specifications: {}'.format(CV_list))

    for cv in CV_list:

        if cv[0] == 'Weighted Distances':
            if not isinstance(cv[1], list):
                raise ValueError("""Weighted Distances only accepts a list of lists where the CV will depend on a combination of 
            distances specified pairwise by the atoms in the two lists. So first cv[1] is a list of atom groups
            specifying the receptor groups and the cv[2] is a list of donor groups""")

            if not isinstance(cv[2], list):
                raise ValueError("""Weighted Distances only accepts a list of lists where the CV will depend on a combination of 
            distances specified pairwise by the atoms in the two lists. So first cv[1] is a list of atom groups
            specifying the receptor groups and the cv[2] is a list of donor groups""")

            if len(cv[1]) != len(cv[2]):
                raise ValueError('Donor and Acceptor lists must be the same length')

            if len(cv[1]) != len(cv[6]):
                raise ValueError('number of weights must be the same as the number of groups of atoms')

            k = 1
            for i in range(len(cv[1])):
                if i == 0:
                    lepton_str = 'w{} * (distance(g{},g{}))'.format(i, k, k + 1)
                else:
                    lepton_str += ' + w{} * (distance(g{},g{}))'.format(i, k, k + 1)
                k += 2

            # instantiate the force with the correct number of groups
            wd_force = mm.CustomCentroidBondForce(len(cv[1]) * 2, lepton_str)
            wd_force.setUsesPeriodicBoundaryConditions(True)

            # add the atoms or groups to the force
            group_list = []
            for receiver_group in cv[1]:
                group_list.append(wd_force.addGroup([receiver_group]))
            for donor_group in cv[2]:
                group_list.append(wd_force.addGroup([donor_group]))

            # add the params weight and initial distance holders
            for i in range(len(cv[1])):
                wd_force.addPerBondParameter('w{}'.format(i))
                wd_force.addPerBondParameter('r{}'.format(i))

            # find param values
            masses = []
            for atom_index in range(len(parmed_structure.positions)):
                masses.append(system.getParticleMass(atom_index) / unit.dalton)

            weights = cv[6]
            param_list = []
            for i in range(len(cv[1])):
                param_list.append(weights[i])
                param_list.append(
                    dist(parmed_structure.coordinates[cv[1][i]] / 10,
                         parmed_structure.coordinates[cv[2][i]] / 10))

            # add the bond to the force with params
            wd_force.addBond(group_list, param_list)

            wd_bias = mm.app.BiasVariable(wd_force,
                                          minValue=cv[3],
                                          maxValue=cv[4],
                                          biasWidth=cv[5])
            CVs.append(wd_bias)

        if cv[0] == 'Coordination Number':
            # NOTE coordination number only accepts a list of lists where the CN will depend on a combination of
            # distances specified pairwise by the atoms in the two lists. So first cv[1] is a list of atom groups
            # specifying the receptor groups and the cv[2] is a list of donor groups

            if not isinstance(cv[1], list):
                raise ValueError("""coordination number only accepts a list of lists where the CN will depend on a combination of 
            distances specified pairwise by the atoms in the two lists. So first cv[1] is a list of atom groups
            specifying the receptor groups and the cv[2] is a list of donor groups""")

            if not isinstance(cv[2], list):
                raise ValueError("""coordination number only accepts a list of lists where the CN will depend on a combination of 
            distances specified pairwise by the atoms in the two lists. So first cv[1] is a list of atom groups
            specifying the receptor groups and the cv[2] is a list of donor groups""")

            if len(cv[1]) != len(cv[2]):
                raise ValueError('Donor and Acceptor lists must be the same length')

            if len(cv[1]) != len(cv[6]):
                raise ValueError('number of weights must be the same as the number of groups of atoms')

            # build CV force string in lepton syntax
            k = 1
            for i in range(len(cv[1])):
                if i == 0:
                    lepton_str = 'w{} * ((1-(distance(g{},g{})-r{})^6/d{}) / ' \
                                 '(1-(distance(g{},g{})-r{})^12/d{}))'.format(i, k, k + 1, i, i, k, k + 1, i, i)
                else:
                    lepton_str += '+ w{} * ((1-(distance(g{},g{})-r{})^6/d{}) / ' \
                                  '(1-(distance(g{},g{})-r{})^12/d{}))'.format(i, k, k + 1, i, i, k, k + 1, i, i)
                k += 2

            # instantiate the force with the correct number of groups
            cn_force = mm.CustomCentroidBondForce(len(cv[1]) * 2, lepton_str)
            cn_force.setUsesPeriodicBoundaryConditions(True)

            # add the atoms or groups to the force
            group_list = []
            for receiver_group in cv[1]:
                group_list.append(cn_force.addGroup([receiver_group]))
            for donor_group in cv[2]:
                group_list.append(cn_force.addGroup([donor_group]))

            # add the params weight and initial distance holders
            for i in range(len(cv[1])):
                cn_force.addPerBondParameter('w{}'.format(i))
                cn_force.addPerBondParameter('r{}'.format(i))
                cn_force.addPerBondParameter('d{}'.format(i))

            weights = cv[6]
            decay_lengths = cv[7]
            param_list = []
            for i in range(len(cv[1])):
                param_list.append(weights[i])
                # coordinates are stored in Angstroms, everything else in nm
                r0 = dist(parmed_structure.coordinates[cv[1][i]],
                          parmed_structure.coordinates[cv[2][i]]) / 10
                print('r0', r0)
                param_list.append(r0)
                param_list.append(decay_lengths[i])
            print(param_list)

            # add the bond to the force with params
            cn_force.addBond(group_list, param_list)

            # if cv[3] != 0 or cv[4] != 1:
            #     raise ValueError('Coordination Number must be biased from 0 to 1')

            cn_bias = mm.app.BiasVariable(cn_force,
                                          minValue=cv[3],
                                          maxValue=cv[4],
                                          biasWidth=cv[5])
            bin_lengths.append((cv[4] - cv[3]) / cv[5])
            CVs.append(cn_bias)

        if cv[0] == 'RMSD':

            if isinstance(cv[1], list):
                atom_set = cv[1]
            elif cv[1].startswith('resid'):
                resid_list = cv[1][6:]
                atom_set = select_atoms(parmed_structure, resid_selection=resid_list)
            else:
                atom_set = select_atoms(parmed_structure, keyword_selection=cv[1])

            if len(atom_set) == 0:
                raise ValueError('RMSD atom selection found no atoms')
            print('Number of atoms to be used for RMSD Bias: {}'.format(len(atom_set)))
            rmsd_force = mm.RMSDForce(parmed_structure.positions, atom_set)
            rmsd_bias = mm.app.BiasVariable(rmsd_force,
                                            minValue=cv[3],
                                            maxValue=cv[4],
                                            biasWidth=cv[5])
            bin_lengths.append((cv[4] - cv[3]) / cv[5])
            CVs.append(rmsd_bias)

        if cv[0] == 'Distance':
            com_force = mm.CustomCentroidBondForce(2, 'distance(g1,g2)')
            com_force.setUsesPeriodicBoundaryConditions(True)

            # find first group
            if isinstance(cv[1], list):
                atom_group1 = cv[1]
            elif cv[1].startswith('resid'):
                resid_list = cv[1][6:]
                atom_group1 = select_atoms(parmed_structure, resid_selection=resid_list)
            else:
                atom_group1 = select_atoms(parmed_structure, keyword_selection=cv[1])

            # find second group
            if isinstance(cv[2], list):
                atom_group2 = cv[2]
            elif cv[2].startswith('resid'):
                resid_list = cv[2][6:]
                atom_group2 = select_atoms(parmed_structure, resid_selection=resid_list)
            else:
                atom_group2 = select_atoms(parmed_structure, keyword_selection=cv[2])

            if len(atom_group1) == 0 or len(atom_group2) == 0:
                raise ValueError('One of the atom selection sets has no atoms')

            print('num atoms being used in 1st moeity: {}'.format(len(atom_group1)))
            print('num atoms being used in 2nd moeity: {}'.format(len(atom_group2)))
            com_force.addGroup(atom_group1)
            com_force.addGroup(atom_group2)
            com_force.addBond([0, 1])
            com_bias = mm.app.BiasVariable(com_force,
                                           minValue=cv[3],
                                           maxValue=cv[4],
                                           biasWidth=cv[5])
            CVs.append(com_bias)

            bin_lengths.append((cv[4] - cv[3]) / cv[5])

        if cv[0] == 'Z-Proj':
            # z-proj is just a distance force using only the z components
            zproj_force = mm.CustomCentroidBondForce(2, 'abs(z1-z2)')
            zproj_force.setUsesPeriodicBoundaryConditions(True)

            # find first group
            if isinstance(cv[1], list):
                atom_group1 = cv[1]
            elif cv[1].startswith('resid'):
                resid_list = cv[1][6:]
                atom_group1 = select_atoms(parmed_structure, resid_selection=resid_list)
            else:
                atom_group1 = select_atoms(parmed_structure, keyword_selection=cv[1])

            # find second group
            if isinstance(cv[2], list):
                atom_group2 = cv[2]
            elif cv[2].startswith('resid'):
                resid_list = cv[2][6:]
                atom_group2 = select_atoms(parmed_structure, resid_selection=resid_list)
            else:
                atom_group2 = select_atoms(parmed_structure, keyword_selection=cv[2])

            if len(atom_group1) == 0 or len(atom_group2) == 0:
                raise ValueError('One of the atom selection sets has no atoms')

            zproj_force.addGroup(atom_group1)
            zproj_force.addGroup(atom_group2)
            zproj_force.addBond([0, 1])
            z_bias = mm.app.BiasVariable(zproj_force,
                                         minValue=cv[3],
                                         maxValue=cv[4],
                                         biasWidth=cv[5])
            bin_lengths.append((cv[4] - cv[3]) / cv[5])
            CVs.append(z_bias)

        if cv[0] == 'Angle':
            # angle force can only be applied to three atoms, but they don't need to be bound
            # if we want to support angles between groups we can use CustomCentroidBondForce
            angle_force = mm.CustomAngleForce('theta')

            lig_atom_index = select_atoms(parmed_structure, keyword_selection='ligand')
            prot_atom_index = select_atoms(parmed_structure, keyword_selection='protein')
            lig_positions = np.array(parmed_structure.positions.value_in_unit(unit.nanometer))[lig_atom_index]
            prot_positions = np.array(parmed_structure.positions.value_in_unit(unit.nanometer))[prot_atom_index]
            three_coords, indeces = get_angle_particle_coords(lig_positions, prot_positions)
            print('Using atoms {}, {}, {} for angle bias'.format(indeces[0], indeces[1], indeces[2]))
            angle_force.addAngle(indeces[0], indeces[1], indeces[2])
            angle_bias = mm.app.BiasVariable(angle_force,
                                             minValue=cv[3],
                                             maxValue=cv[4],
                                             biasWidth=cv[5],
                                             periodic=True)
            bin_lengths.append((cv[4] - cv[3]) / cv[5])
            CVs.append(angle_bias)

    # # all bins must be the same shape
    if not bin_lengths[1:] == bin_lengths[:-1]:
        print("""{}
            Warning: Bias dimensions should be equal for all CVs specified. Please adjust the max, min, and binwidths',
            such that max-min/width are equal for all CVs""".format(bin_lengths))


    return CVs