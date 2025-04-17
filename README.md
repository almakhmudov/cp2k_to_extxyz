# Usage
```sh 
python cp2k2extxyz.py path=<path> coordinates=<coordinates_filename> \
                         sp_output=<output_filename> lattice=<a b c>
```

# Arguments

- `path` (Required):  
  Base directory containing subdirectories with input files to process.

- `coordinates` (Required):  
  Name of the coordinates file in each subdirectory (e.g., `coordinates.xyz`).

- `sp_output` (Required):  
  Output file name in each subdirectory containing total energy and force data.

- `lattice` (Required):  
  Lattice parameters in the form `"a b c"` (e.g., `"15.0 15.0 15.0"`).

- `from` (Optional):  
  Starting index for subdirectory processing. If omitted, all subdirs are processed.

- `to` (Optional):  
  Ending index for subdirectory processing. If omitted, all subdirs are processed.

- `step` (Optional):  
  Step size between subdirectories. Only used if `from` and `to` are provided.

- `convert_energy` (Optional):  
  Convert energy values. Supported: `au2eV`.

- `convert_forces` (Optional):  
  Convert force values. Supported: `au2eVA`.

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