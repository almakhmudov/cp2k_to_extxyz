import os
import sys
from ase.io import read

# The conversion factors were taken from https://physics.nist.gov/cuu/Constants/ 
CONVERSION_FACTORS = {
    "au2eV": 27.21138625,    # Hartree to eV
    "au2eVA": 51.42206771,   # Hartree/Bohr to eV/A
}

def print_help():
    help_text = """
Usage: python cp2k2extxyz.py path=<path> coordinates=<coordinates_filename> sp_output=<output_filename> lattice=<lattice_params> [from=<start_folder>] [to=<end_folder>] [step=<folder_step>] [convert_energy=<conversion>] [convert_forces=<conversion>]

Arguments:
    path           : Base directory path containing subdirectories with input files. Each subdirectory will be processed.
    coordinates    : Name of the coordinates file (e.g., 'coordinates.xyz') in each subdirectory.
    sp_output      : Name of the output file (e.g., 'output') in each subdirectory, which contains total energy and force data.
    lattice        : Lattice parameters in the form "a b c" (e.g., "15.0 15.0 15.0").
    from           : (Optional) Starting number for the subdirectory loop. If not provided, all folders are processed.
    to             : (Optional) Ending number for the subdirectory loop. If not provided, all folders are processed.
    step           : (Optional) Step size for incrementing through subdirectories. Only used if 'from' and 'to' are provided.
    convert_energy : (Optional) Convert energy values. Supported: 'au2eV'.
    convert_forces : (Optional) Convert force values. Supported: 'au2eVA'.

Example:
    python cp2k2extxyz.py path=/data/simulations coordinates=coordinates.xyz sp_output=output lattice="15.0 15.0 15.0" from=1 to=100 step=5 convert_energy=au2eV convert_forces=au2eVA

If 'from' and 'to' are omitted, all subdirectories under 'path' will be processed.
"""
    print(help_text)
    sys.exit()

# Check for help flag
if '-h' in sys.argv or '--help' in sys.argv:
    print_help()

# Parse command-line arguments
args = {arg.split('=')[0]: arg.split('=')[1] for arg in sys.argv[1:]}
required_args = ['path', 'coordinates', 'sp_output', 'lattice']
if not all(arg in args for arg in required_args):
    print("Error: Missing required arguments.")
    print_help()

path = args.get('path')
coordinates_base = args.get('coordinates')
sp_output_base = args.get('sp_output')
lattice_params = args.get('lattice').split()
convert_energy = args.get('convert_energy')
convert_forces = args.get('convert_forces')

# Convert lattice parameters to a cubic cell format
if len(lattice_params) != 3:
    print("Error: Lattice parameters must be provided as three values (e.g., '15.0 15.0 15.0').")
    sys.exit()
lattice_str = f"{lattice_params[0]} 0.0 0.0 0.0 {lattice_params[1]} 0.0 0.0 0.0 {lattice_params[2]}"

# Extract the subdirectories
subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

# Determine start and end folder
if 'from' in args and 'to' in args:
    start_folder = int(args['from'])
    end_folder = int(args['to'])
    step = int(args.get('step', 1))
    subdirs = [d for d in subdirs if d.isdigit() and start_folder <= int(d) <= end_folder]
    subdirs = subdirs[::step]
else:
    subdirs = [d for d in subdirs]

# Create the output file
combined_filename = os.path.join(path, 'combined_coordinates_forces.xyz')
with open(combined_filename, 'w') as combined_file:
    pass

# Loop through subdirectories and combine the coordinates and forces
for folder_num in subdirs:
    folder_path = os.path.join(path, folder_num)
    coordinates_filename = os.path.join(folder_path, coordinates_base)
    output_filename = os.path.join(folder_path, sp_output_base)
    
    if not os.path.exists(coordinates_filename) or not os.path.exists(output_filename):
        continue

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
                if convert_energy in CONVERSION_FACTORS:
                    total_energy *= CONVERSION_FACTORS[convert_energy]
                break

        for i, line in enumerate(lines):
            if '# Atom   Kind   Element' in line:
                for atom_line in lines[i+1 : i+1+number_of_atoms]:
                    columns = atom_line.split()
                    force = [float(f) for f in columns[-3:]]
                    if convert_forces in CONVERSION_FACTORS:
                        force = [f * CONVERSION_FACTORS[convert_forces] for f in force]
                    forces.append([str(f) for f in force])
                break

    with open(coordinates_filename, 'r') as file:
        lines = file.readlines()
        for line in lines[2:2+number_of_atoms]:
            columns = line.split()
            coordinates.append(columns)

    coordinates_forces = [coord + force for coord, force in zip(coordinates, forces)]

    with open(combined_filename, 'a') as combined_file:
        combined_file.write(f"{number_of_atoms}\n")
        combined_file.write(f'Lattice="{lattice_str}" '
                            f'Properties=species:S:1:pos:R:3:forces:R:3 energy={total_energy} '
                            f'pbc="T T T"\n')
        for line in coordinates_forces:
            combined_file.write('\t'.join(line) + "\n")

# Count frames in the output file using ASE
frames = read(combined_filename, index=':')

print("All data appended to the combined file:", combined_filename)
print("The total number of frames:", len(frames))