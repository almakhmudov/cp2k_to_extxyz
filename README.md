# Usage
```sh 
python cp2k_to_extxyz.py path=<path> coordinates=<coordinates_filename> sp_output=<output_filename> from=<start_folder> to=<end_folder> step=<folder_step>
```

# Arguments
    path          : Base directory path containing subdirectories with input files. Each subdirectory will be processed.
    coordinates   : Name of the coordinates file (e.g., 'coordinates.xyz') in each subdirectory.
    sp_output     : Name of the output file (e.g., 'output') in each subdirectory, which contains total energy and force data.
    from          : Starting number for the subdirectory loop. For example, 'from=1' starts processing from folder '1'.
    to            : Ending number for the subdirectory loop. For example, 'to=100' processes up to folder '100'.
    step          : Step size for incrementing through subdirectories. For example, 'step=5' processes every 5th folder in the specified range.

# Example
```sh
python cp2k_to_extxyz.py path=/data/simulations coordinates=coordinates.xyz sp_output=output from=1 to=100 step=5
```
This example processes folders /data/simulations/1, /data/simulations/6, /data/simulations/11, ..., /data/simulations/96. 
Each processed folder's data is appended to a single output file named 'combined_coordinates_forces.xyz' created in the base path.