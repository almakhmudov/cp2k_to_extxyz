# Usage
```sh 
python cp2k2extxyz.py path=<path> coordinates=<coordinates_filename> \
                         sp_output=<output_filename> lattice=<a b c>
```

# Arguments
path           : Base directory path containing subdirectories with input files. Each subdirectory will be processed.
coordinates    : Name of the coordinates file (e.g., 'coordinates.xyz') in each subdirectory.
sp_output      : Name of the output file (e.g., 'output') in each subdirectory, which contains total energy and force data.
lattice        : Lattice parameters in the form "a b c" (e.g., "15.0 15.0 15.0").
from           : (Optional) Starting number for the subdirectory loop. If not provided, all folders are processed.
to             : (Optional) Ending number for the subdirectory loop. If not provided, all folders are processed.
step           : (Optional) Step size for incrementing through subdirectories. Only used if 'from' and 'to' are provided.
convert_energy : (Optional) Convert energy values. Supported: 'au2eV'.
convert_forces : (Optional) Convert force values. Supported: 'au2eVA'.

# Example
```sh
python cp2k2extxyz.py path=/data/simulations \
                         coordinates=coordinates.xyz \
                         sp_output=output from=1 to=100 step=5 \
                         lattice="15.0 15.0 15.0" convert_energy=au2eV \
                         convert_forces=au2eVA
```
This example processes folders `/data/simulations/1`, `/data/simulations/6`, `/data/simulations/11`, ..., `/data/simulations/96`. 
Each processed folder's data is appended to a single output file named `combined_coordinates_forces.xyz` created in the base path.
The forces and energies will be converted accordingly. If 'from' and 'to' are omitted, all subdirectories under 'path' will be processed.