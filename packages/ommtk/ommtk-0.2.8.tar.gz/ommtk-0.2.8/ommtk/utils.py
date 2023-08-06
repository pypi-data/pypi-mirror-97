
import numpy as np
from scipy import signal
from simtk.openmm import unit


aa_residues = ["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS",
               "LEU", "MET", "ASN", "PRO", "GLN", "ARG", "SER", "THR", "VAL", "TRP", "TYR", "ACE", "NME"]

water_residues = ['HOH', 'TIP3', 'TIP3P', 'SPCE', 'SPC', 'TIP4PEW', 'WAT', 'OH2', 'TIP']

lipid_residues = ['AR', 'CHL', 'DHA', 'LA', 'MY', 'OL', 'PA', 'PC', 'PE', 'PGR', 'PH-', 'PS', 'SA', 'SM', 'ST']


def select_atoms(parmed_structure, keyword_selection=None, ligand_resname=None, resid_selection=None):
    """
    Select atoms is the main selection mechanism for ommtk functionality. It requires as input a parmed structure
    (does not need parameters) and a set of keywords. It returns a list of atoms that can be used to slice parmed
    objects, set restraints, or specify CVs.

    Keyword selection argument accepts (in any order) any number of the following: ligand, protein, water, lipids
    with the optional modifiers 'noh' and 'not' where 'noh' will exclude hydrogens and 'not' will invert the selection.
    If more than one keyword is specified, it is assumed they are joined with
    "or" operation (i.e. 'ligand protein' will return both ligand and protein atom indeces).

    Resid selection accepts the format "A 11 12 13 14" where the first is the chain identifier and the following
    residues are also assumed to be joined by 'or' operator such that the above selection will return all atoms in
    residues 11, 12, 13 and 14 on chain A.

    If both keyword and resid selection are applied both are returned (i.e. 'or' combining is assumed).
    If 'not' or 'noh' are selected the modifier will be applied to all selections (keyword or resid). As such
    >>> sel = select_atoms(pmd, keyword_selection='noh', resid_selection='A 11')
    will return non-hydrogen atoms in residue 11 on chain A.

    Ligand selection is performed by residue name, where 'LIG' and 'UNL' are assumed to be ligands resnames.
    If your ligand has a different residue name you can specify it with ligand_resname. Otherwise Amber style
    residue naming is assumed.




    :param parmed_structure: parmed_structre
    :param keyword_selection: string
    :param ligand_resname: string
    :param resid_selection: string
    :return: list of integers
    """

    lig_residues = ['LIG', 'UNL']

    if ligand_resname:
        lig_residues.append(ligand_resname)

    if keyword_selection == None and resid_selection == None:
        raise ValueError('Must specify either keyword selection or resid_selection')

    final_list = []

    if resid_selection:
        # split up the selection syntax
        resid_list = resid_selection.split()
        chain_selection = resid_list[0]
        resid_list = resid_list[1:]
        # convert the resids to integers
        resid_list = [int(i) for i in resid_list]
        # TODO check the order of chains in multichain proteins
        # TODO Currently assuming alphabet designation matches parmed order
        protein_chains = [i for i in parmed_structure.topology.chains() if next(i.residues()).name in aa_residues]
        for k, chain in enumerate(protein_chains):
            # convert letter rep of chain to ordinal number rep
            if ord(chain_selection.lower()) - 96 == k + 1:
                residues = [i for i in chain.residues()]
                res0 = residues[0]
                start_index = res0.index
                selected_residues = [i for i in residues if i.index - start_index in resid_list]

                if len(selected_residues) == 0:
                    raise ValueError('Could not find one of the residues {} on protein chain.'.format(resid_list))

                for i in selected_residues:
                    for k in i.atoms():
                        final_list.append(k.index)
    if keyword_selection:
        selection_keywords = keyword_selection.split()

        # if selection keywords contain noh or not make sure they're at the end of the list
        if 'noh' in selection_keywords:
            selection_keywords.remove('noh')
            selection_keywords.append('noh')
        if 'not' in selection_keywords:
            selection_keywords.remove('not')
            selection_keywords.append('not')

        for keyword in selection_keywords:

            if keyword not in ['ligand', 'protein', 'lipids', 'water', 'noh', 'not']:
                raise ValueError("""Keyword {} could not be parsed. 
                Options are noh; not; protein; ligand; lipids; water.""".format(keyword))

            if keyword == 'protein':
                protein_list = [i.idx for i in parmed_structure.atoms if i.residue.name in aa_residues]
                for i in protein_list:
                    final_list.append(i)

            if keyword == 'water':
                water_list = [i.idx for i in parmed_structure.atoms if i.residue.name in water_residues]
                for i in water_list:
                    final_list.append(i)

            if keyword == 'ligand':
                ligand_list = [i.idx for i in parmed_structure.atoms if i.residue.name in lig_residues]
                for i in ligand_list:
                    final_list.append(i)


            if keyword == 'lipid':
                lipid_list=[i.idx for i in parmed_structure.atoms if i.residue.name in lipid_residues]
                for i in lipid_list:
                    final_list.append(i)

            if keyword == 'noh':
                remove_list = []
                for i in final_list:
                    if 'H' in parmed_structure[i].name:
                        remove_list.append(i)
                final_list = list(set(final_list) - set(remove_list))

            if keyword == 'not':
                all_atoms = [i for i in parmed_structure.topology.atoms()]
                all_atoms_indeces_set = set([i.index for i in all_atoms])
                inverted_set = all_atoms_indeces_set - set(final_list)
                final_list = list(inverted_set)

    if len(final_list) == 0:
        print('warning, failed to select any atoms')
    return final_list

def find_center_of_mass(coord, masses):
    """
    given a set of masses and coordinates (index is assumed to match) find the center of mass
    :param coord: numpy.array of cartesian coordinates
    :param masses: numpy.array
    :return: numpy.array
    """
    masses = np.array(masses)
    weights = masses/masses.sum()
    com = np.average(np.array(coord/unit.nanometer), weights = weights, axis=0)
    return com

def find_z_cone_apex(prot_positions, lig_positions, z_padding = 1):
    """
    Find the apex maximal or minimal z coordinate in relation to ligand protein complex
    and pad it. Meant to be used for finding funnel placement in a z-aligned systems.

    If average ligand z-coordinates are larger than average protein z-coordinates, maximal z is returned,
    else minimal z-coordinate is returned.

    COORDINATES ARE IN NANOMETERS

    :param prot_positions: numpy.array
    :param lig_positions: numpy.array
    :param z_padding: float
    :return:
    """



    #first find z-coordinate of ligand and z_coordinate of protein
    lig_z_pos = np.mean([i[2] for i in lig_positions])
    prot_z_pos = np.mean([i[2] for i in prot_positions])

    #next find the max z coordinate of the protein on the side it's been oriented

    if lig_z_pos>prot_z_pos:
        max_z_pos = np.max([i[2] for i in prot_positions])
        z_coord = max_z_pos + z_padding
    else:
        min_z_pos = np.min([i[2] for i in prot_positions])
        z_coord = min_z_pos - z_padding

    if np.isnan(z_coord):
        raise ValueError('Could not find z_coord for funnel apex')

    return z_coord

def find_radius_and_center(ligand_pos, radius_scale_factor):
    """

    given a set of coordinates, find the maximal separation in those coordinates and
    scale it by radius_scale_factor.

    :param ligand_pos: numpy.array
    :param radius_scale_factor:
    :return: tuple of raidus (float) and  geometric center(coordinates)
    """

    cog = np.mean(ligand_pos, axis=0)

    distances = []
    #choose the two ligand atoms that are the furthest apart and use as estimate for cone mouth
    for k,i in enumerate(ligand_pos):
        for l,j in enumerate(ligand_pos):
            if k != l:
                distances.append(dist(i,j))

    rcyl = radius_scale_factor * np.max(distances)

    return rcyl,cog

def find_flat_bottom_radius(ligand_pos, prot_pos, scale_factor=.8):
    """
    Find the point on the protein furthest from the ligand coordinates specified and return the distance between those
    two points.

    :param ligand_pos: np.array
    :param prot_pos: np.array
    :param scale_factor: float
    :return: float
    """

    cog = np.mean(ligand_pos, axis=0)

    distances = []
    #find the furthest protein atom from the ligand and use that
    for pos in prot_pos:
        distances.append(dist(cog,pos))

    rcyl = scale_factor * np.max(distances)

    return rcyl

def find_center_atom(center, array_pos):
    """
    find the atom closest to a given point (center)

    :param center: numpy.array
    :param array_pos: numpy.array
    :return: tuple (index, positions of the chosen atom)
    """

    distances = []
    for i in array_pos:
        distances.append(dist(i,center))

    chosen = np.argmin(distances)

    return chosen, array_pos[chosen]

def get_angle_particle_coords(ligand_pos, prot_pos):
    """
    Given ligand positions and protein positions, estimate three cartesian positions that define an
    angle between protein and ligand. It takes two points on the ligand that are maximally separate, and
    assigns a point closest to one of those poinst that is on the protein.

    :param ligand_pos: numpy.array
    :param prot_pos: numpy.array
    :return: tuple of three angle coordinates and their indeces
    """

    distances = []
    indeces= []
    #choose the two ligand atoms that are the furthest apart
    for k,i in enumerate(ligand_pos):
        for l,j in enumerate(ligand_pos):
            if k != l:
                indeces.append([k,l])
                distances.append(dist(i,j))
    chosen_k = indeces[np.argmax(distances)][0]
    chosen_l = indeces[np.argmax(distances)][1]

    #choose the protein atom that is the closest to the chosen_k'th ligand atom
    distances = []
    for z in prot_pos:
        distances.append(dist(ligand_pos[chosen_k],z))
    chosen_z = np.argmin(distances)

    #load the coords and indeces in separate arrays
    three_coords = [ligand_pos[chosen_k],ligand_pos[chosen_l],prot_pos[chosen_z]]
    indeces = [int(chosen_k),int(chosen_l),int(chosen_z)]

    return three_coords, indeces

def dist(a,b):
    """
    cartesian distance between two coordinates.

    :param a: numpy array
    :param b: numpy array
    :return: float
    """
    return np.linalg.norm(a-b)

def find_contacts(positions1, positions2, cutoff):
    """
    find contacts between two sets of coordinates based on cartesian distance

    :param positions1: numpy.array
    :param positions2: nuympy.array
    :param cutoff: float
    :return: tuple of coordinate indeces
    """

    contacts_i = []
    contacts_j = []
    for k,i in enumerate(positions1):
        for l,j in enumerate(positions2):
            if dist(i,j)<=cutoff:
                contacts_i.append(k)
                contacts_j.append(l)

    return contacts_i,contacts_j


def find_com_distance_between_atom_groups(parmed, masses, group1, group2):
    """
    given two groups of atom indeces and a parmed.structure object and the masses,
    return the distance between the center of masses of the atom groups
    :param parmed: Parmed.structure.Structure()
    :param masses: list of integers or floats
    :param group1: list of integers
    :param group2: list integers
    :return: float
    """
    g1_coords = np.array(parmed.positions.value_in_unit(unit.nanometer))[group1]
    g2_coords = np.array(parmed.positions.value_in_unit(unit.nanometer))[group2]
    g1_masses = np.array(masses)[group1]
    g2_masses = np.array(masses)[group2]
    g1_com = find_center_of_mass(g1_coords, g1_masses)
    g2_com = find_center_of_mass(g2_coords, g2_masses)
    distance = dist(g1_com, g2_com)
    return distance


def get_bound_site_cog(parmed, cutoff_in_angstroms):
    """

    :param parmed: parmed.structure
    :param cutoff_in_angstroms: float
        cutoff used for finding center of binding site. Cutoff is in distance from ligand
    :return: np.array
        cartesian coordinates of center of geometry of the binding site defined by distance
    """
    prot_sel = select_atoms(parmed, keyword_selection='protein')
    lig_sel = select_atoms(parmed, keyword_selection='ligand')
    coords = parmed.coordinates
    prot_coords=coords[prot_sel]
    lig_coords=coords[lig_sel]
    lig_contacts, prot_contacts = find_contacts(lig_coords,prot_coords,cutoff_in_angstroms)
    prot_contact_coords = prot_coords[np.unique(prot_contacts)]
    return np.mean(prot_contact_coords,axis=0)




def get_rotation_matrix(i_v, unit):
    """
    compute rotation matrix for a set of coordinates to align vector i_v with one of the
    cartesian axes unit.

    :param i_v: numpy.array
        two coordinates defining vector.
    :param unit: numpy.array
        coordinates defining the unit vector, i.e. positive z-axis = np.array([0,0,1])
    :return:
    """

    # From http://www.j3d.org/matrix_faq/matrfaq_latest.html#Q38
    i_v /= np.linalg.norm(i_v)
    uvw = np.cross(i_v, unit)
    rcos = np.dot(i_v, unit)
    rsin = np.linalg.norm(uvw)

    if not np.isclose(rsin, 0):
        uvw /= rsin
    u, v, w = uvw

    # Compute rotation matrix
    rot_matrix =  (
        rcos * np.eye(3) +
        rsin * np.array([
            [ 0, -w,  v],
            [ w,  0, -u],
            [-v,  u,  0]
        ]) +
        (1.0 - rcos) * uvw[:,None] * uvw[None,:]
    )

    return rot_matrix


def align_structure(pmd, sel1, sel2, axis):
    """
    Rotate the structure such that a vector originating from cog of sel1 and terminating in the cog of sel2
    is aligned along the z-axis.

    :param pmd: parmed.structure
    :param sel1: string
        ommtk selection mask. If starts with resid resid selection is assumed else keyword selection is assumed
    :param sel2: string
        ommtk selection mask. If starts with resid resid selection is assumed else keyword selection is assumed
    :return: parmed.structure
        new pmd with rotated coordinates
    """

    coordinates = pmd.coordiantes

    if sel1 == 'active_site':
        sel1_cog = get_bound_site_cog(pmd, 4)
    elif sel1.startswith('resid'):
        sel1_atoms = select_atoms(parmed_structure=pmd, resid_selection=sel1[6:])
        sel1_coords = coordinates[sel1_atoms]
        sel1_cog = np.mean(sel1_coords, axis=0)
    else:
        sel1_atoms = select_atoms(parmed_structure=pmd, keyword_selection=sel1)
        sel1_coords = coordinates[sel1_atoms]
        sel1_cog = np.mean(sel1_coords, axis=0)

    coordinates -= sel1_cog

    if sel2 == 'active_site':
        sel2_cog = get_bound_site_cog(pmd, 4)
    elif sel2.startswith('resid'):
        sel2_atoms = select_atoms(parmed_structure=pmd, resid_selection=sel2[6:])
        sel2_coords = coordinates[sel2_atoms]
        sel2_cog = np.mean(sel2_coords, axis=0)
    else:
        sel2_atoms = select_atoms(parmed_structure=pmd, keyword_selection=sel2)
        sel2_coords = coordinates[sel2_atoms]
        sel2_cog = np.mean(sel2_coords, axis=0)

    # specify axis
    if axis == '-z':
        unit_axis = [0., 0., -1.]
    elif axis == '+z':
        unit_axis = [0., 0., 1.]
    elif axis == '+y':
        unit_axis = [0., 1., 0.]
    elif axis == '-y':
        unit_axis = [0., -1., 0.]
    elif axis == '+x':
        unit_axis = [1., 0., 0.]
    elif axis == '-x':
        unit_axis = [-1., 0., 0.]

    rot_matrix = get_rotation_matrix(sel2_cog, unit=unit_axis)

    rotated_coordinates = []
    for i in coordinates:
        rotated_coordinates.append(list(np.dot(i.T, rot_matrix.T)))

    rotated_coordinates = np.array(rotated_coordinates)

    rotated_coordinates += sel1_cog


    # set coordinates on parmed
    pmd.coordinates = rotated_coordinates
    pmd.positions = rotated_coordinates * unit.angstrom

    return pmd

def calc_dG(fes,well_combining_method):
    """
    Input a free energy surface and calculate energy difference between wells. It is agnostic to units

    :param fes: 2D matrix in format given by FESResporter
    :param well_combining_method: string ['mean','max']
    :return: dG estimate (float)
    """
    fes = np.array(fes)
    minimax = signal.argrelextrema(fes, np.less)
    minimay = signal.argrelextrema(fes, np.less, axis=1)

    y_direction = set()
    for i in range(len(minimay[0])):
        y_direction.add((minimay[0][i], minimay[1][i]))
    x_direction = set()
    for i in range(len(minimax[0])):
        x_direction.add((minimax[0][i], minimax[1][i]))

    min_set = x_direction.intersection(y_direction)
    min_set = list(min_set)
    x_mins = [min_set[i][0] for i in range(len(min_set))]
    y_mins = [min_set[i][1] for i in range(len(min_set))]

    dG_list = []
    try:
        min_index = np.argmin([fes[x_mins[i], y_mins[i]] for i in range(len(x_mins))])
    except ValueError:
        print('did not find any wells')
        return 0

    for i in range(len(x_mins)):
        if i != min_index and y_mins[i] - y_mins[min_index] > 10:
            dG_val = fes[x_mins[min_index], y_mins[min_index]] - fes[x_mins[i], y_mins[i]]
            dG_list.append(dG_val)

    if len(dG_list) == 0:
        print('dG_list empty')
        dG = 0
    else:
        if well_combining_method=='mean':
            dG = np.mean(dG_list)
        if well_combining_method=='max':
            dG = np.max(dG_list)

    return dG
