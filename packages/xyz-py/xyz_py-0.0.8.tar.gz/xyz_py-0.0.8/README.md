# xyz-py

`xyz-py` is a python module for working with and manipulating chemical structures. 

# Installation

For convenience, `xyz-py` is available on [PyPI](https://pypi.org/project/xyz-py/) and so can be installed using `pip`

```
pip install xyz-py
```

# Functionality

To use the functions included in `xyz-py`, first import it into your python file
```
import xyz_py as xyzp
```
and then call them as 
```
xyzp.function_name(arguments)
```

To find information on any of the functions included in `xyz-py`, use the `help` command from within a python environment, e.g.

```
help(xyzp.function_name(arguments))
```

# List of functions

A brief descriptions of functions:

## `load_xyz`

Loads labels and coordinates from xyz file

## `save_xyz`

Save labels and coordinates to xyz file

## `remove_numbers`

Remove indexing numbers from a set of atomic labels

## `add_numbers`

Add indexing numbers to a set of atomic labels

## `count_elements`

Count number of each element in a list of elements

## `formstr_to_formdict`

Converts formula string into dictionary of {atomic label:quantity} pairs

## `formdict_to_formstr`

Converts dictionary of {atomic label:quantity} pairs into a single formula string

## `contains_metal`

Returns 1 if metal found in formula string else returns a 0

## `combine_xyz`

Combines two sets of labels and coordinates

## `get_neighborlist`

Calculate ASE neighbourlist with cutoffs

## `get_adjacency`

Calculate adjacency matrix using ASE neighbourlist

## `get_bonds`

Calculate and save list of atoms between which there is a bond using ASE. Only unique bonds are saved.

## `get_angles`

Calculate and save list of atoms between which there is a angle using ASE. Only unique angles are saved.

## `get_dihedrals`

Calculate and save list of atoms between which there is a dihedral using ASE. Only unique dihedrals are saved.

## `lab_to_num`

Convert atomic label to atomic number

## `num_to_lab`

Convert atomic number to atomic label

## `reflect_coords`

Reflect coordinates through XY plane

## `remove_broken`

Removes structures from coordinates which do not match user provided formulae

## `calculate_rmsd`

Calculates RMSD (root mean square deviation) between two structures

## `rotate_coords`

Rotates coordinates by alpha, beta, gamma using the zyz convention

## `minimise_rmsd`

Minimises RMSD between two structures by rotating one onto the other
