import os
import sys

# Display help information
def print_help():
    help_text = """
Usage: python cp2k_to_extxyz.py path=<path> coordinates=<coordinates_filename> sp_output=<output_filename> from=<start_folder> to=<end_folder> step=<folder_step>

Arguments:
    path          : Base directory path containing subdirectories with input files. Each subdirectory will be processed.
    coordinates   : Name of the coordinates file (e.g., 'coordinates.xyz') in each subdirectory.
    sp_output     : Name of the output file (e.g., 'output') in each subdirectory, which contains total energy and force data.
    from          : Starting number for the subdirectory loop. For example, 'from=1' starts processing from folder '1'.
    to            : Ending number for the subdirectory loop. For example, 'to=100' processes up to folder '100'.
    step          : Step size for incrementing through subdirectories. For example, 'step=5' processes every 5th folder in the specified range.

Example:
    python cp2k_to_extxyz.py path=/data/simulations coordinates=coordinates.xyz sp_output=output from=1 to=100 step=5

This example processes folders /data/simulations/1, /data/simulations/6, /data/simulations/11, ..., /data/simulations/96. 
Each processed folder's data is appended to a single output file named 'combined_coordinates_forces.xyz' created in the base path.
"""
    print(help_text)
    sys.exit()

# Check for help flag
if '-h' in sys.argv or '--help' in sys.argv:
    print_help()

# Parse command-line arguments
args = {arg.split('=')[0]: arg.split('=')[1] for arg in sys.argv[1:]}
required_args = ['path', 'coordinates', 'sp_output', 'from', 'to', 'step']
if not all(arg in args for arg in required_args):
    print("Error: Missing required arguments.")
    print_help()

path = args.get('path')
coordinates_base = args.get('coordinates')
sp_output_base = args.get('sp_output')
start_folder = int(args.get('from'))
end_folder = int(args.get('to'))
step = int(args.get('step'))

# Create the combined output file
combined_filename = os.path.join(path, 'combined_coordinates_forces.xyz')
with open(combined_filename, 'w') as combined_file:
    pass

# Loop through the range of folders and combine the coordinates and forces
for folder_num in range(start_folder, end_folder + 1, step):
    folder_path = os.path.join(path, str(folder_num))
    coordinates_filename = os.path.join(folder_path, coordinates_base)
    output_filename = os.path.join(folder_path, sp_output_base)

    number_of_atoms = 0
    forces = []
    coordinates = []
    total_energy = None

    with open(output_filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if '- Atoms:' in line:
                number_of_atoms = int(line.split()[-1])
                break

        for line in lines:
            if 'ENERGY| Total FORCE_EVAL ( QS ) energy [a.u.]:' in line:
                total_energy = float(line.split()[-1])
                break

        for i, line in enumerate(lines):
            if '# Atom   Kind   Element' in line:
                for atom_line in lines[i+1 : i+1+number_of_atoms]:
                    columns = atom_line.split()
                    force = columns[-3:]
                    forces.append(force)
                break

    with open(coordinates_filename, 'r') as file:
        lines = file.readlines()
        for line in lines[2:2+number_of_atoms]:
            columns = line.split()
            coordinates.append(columns)

    # Combine 'coordinates' and 'forces' into 'coordinates_forces'
    coordinates_forces = []
    for coord, force in zip(coordinates, forces):
        coordinates_forces.append(coord + force)

    # Write to the combined file
    with open(combined_filename, 'a') as combined_file:
        combined_file.write(f"{number_of_atoms}\n")
        combined_file.write(f'Lattice="15.0 0.0 0.0 0.0 15.0 0.0 0.0 0.0 15.0" '
                            f'Properties=species:S:1:pos:R:3:forces:R:3 energy={total_energy} '
                            f'pbc="T T T"\n')
        for idx, line in enumerate(coordinates_forces):
            combined_file.write('\t'.join(line) + "\n")

print("All data appended to the combined file:", combined_filename)
