import os

# Function to create updated XML files
def create_updated_xml_file(protein_id, x_coord, y_coord, z_coord, grid_dimension):
    script_template_dir = os.path.join(os.getcwd(), 'script_templates')
    xml_template_file = os.path.join(script_template_dir, '1B3_outward_pre-talaris2013_template.xml')
    xml_output_dir = os.path.join(os.getcwd(), 'xml_inputs')

    if not os.path.isfile(xml_template_file):
        print(f"Template file '{xml_template_file}' does not exist.")
        return

    with open(xml_template_file, 'r') as template_file:
        xml_content = template_file.read()

    updated_content = xml_content.replace(
        '<Coordinates x="-1.396999" y="-9.645000" z="3.289000" /></StartFrom>',
        f'<Coordinates x="{x_coord:.3f}" y="{y_coord:.3f}" z="{z_coord:.3f}" /></StartFrom>'
    )

    updated_content = updated_content.replace(
        'box_size="33"',
        f'box_size="{grid_dimension}"'
    )

    output_file_name = f"{os.path.splitext(protein_id)[0]}_pre-talaris2013.xml"
    output_file_path = os.path.join(xml_output_dir, output_file_name)

    with open(output_file_path, 'w') as output_file:
        output_file.write(updated_content)

    print(f"Updated XML file '{output_file_name}' has been created in '{xml_output_dir}'.")

# Function to create options files
def create_options_files(protein_id, ligand_files):
    script_template_dir = os.path.join(os.getcwd(), 'script_templates')
    options_template_file = os.path.join(script_template_dir, 'In100_1B3_outward_pre-talaris2013_template.txt')
    options_output_dir = os.path.join(os.getcwd(), 'options_inputs')

    if not os.path.isfile(options_template_file):
        print(f"Options template file '{options_template_file}' does not exist.")
        return

    options_files = []  # List to store the names of the generated options files

    for ligand in ligand_files:
        ligand_name = os.path.splitext(ligand)[0]
        output_file_name = f"{ligand_name}_{os.path.splitext(protein_id)[0]}_pre-talaris2013.txt"
        output_file_path = os.path.join(options_output_dir, output_file_name)

        with open(options_template_file, 'r') as template_file:
            options_content = template_file.read()

        updated_content = options_content.replace('In100', ligand_name)
        updated_content = updated_content.replace('1B3_outward', os.path.splitext(protein_id)[0])

        with open(output_file_path, 'w') as output_file:
            output_file.write(updated_content)

        options_files.append(output_file_name)
        print(f"Options file '{output_file_name}' has been created in '{options_output_dir}'.")

    return options_files

# Function to create docking job files based on the options files
def create_docking_job_files(protein_id, options_files):
    script_template_dir = os.path.join(os.getcwd(), 'script_templates')
    docking_job_template_file = os.path.join(script_template_dir, 'Docking_job_template.txt')
    docking_output_dir = os.getcwd()  # Docking job files will be placed in the main directory

    if not os.path.isfile(docking_job_template_file):
        print(f"Docking job template file '{docking_job_template_file}' does not exist.")
        return

    # Ensure the main docking_results directory exists
    docking_results_dir = os.path.join(os.getcwd(), 'docking_results')
    if not os.path.exists(docking_results_dir):
        os.makedirs(docking_results_dir)

    # Ensure the specific raw results directory exists
    protein_name = os.path.splitext(protein_id)[0]
    raw_results_dir = os.path.join(docking_results_dir, f"{protein_name}_raw_results")
    if not os.path.exists(raw_results_dir):
        os.makedirs(raw_results_dir)

    # Create a docking job file for each options file generated
    for idx, options_file in enumerate(options_files, start=1):
        docking_job_file_name = f"{protein_name}_docking_job_{idx}.txt"
        docking_job_file_path = os.path.join(docking_output_dir, docking_job_file_name)

        with open(docking_job_template_file, 'r') as template_file:
            docking_job_content = template_file.read()

        # Replace placeholder with the actual options file name
        docking_job_content = docking_job_content.replace('Non_inhib86_1B1_final_pre-talaris2013.txt', options_file)

        with open(docking_job_file_path, 'w') as output_file:
            output_file.write(docking_job_content)

        print(f"Docking job file '{docking_job_file_name}' has been created in '{docking_output_dir}'.")

# Main function that runs after passing checks
def main(protein_id, ligand_files):
    # Assume that the checks for ligands and protein-ligand complexes have passed
    print("\033[1mAll ligands have corresponding conformer and protein-ligand complex files.\033[0m")

    # Ask the user for the docking type
    docking_type = input("\033[1mDo you want to perform global or local docking? (global/local): \033[0m").strip().lower()

    if docking_type == 'local':
        ready_for_input = input("\033[1mAre you ready to provide starting coordinates and docking grid dimensions? (yes/no): \033[0m").strip().lower()

        if ready_for_input == 'no':
            print("\033[1mPlease look at the 'finding_input_coordinates_and_dimensions_guide' directory.\033[0m")
        elif ready_for_input == 'yes':
            # Get coordinates and grid dimension from user
            coordinates_input = input("\033[1mEnter x, y, z coordinates (e.g., 12.3 45.6 78.9): \033[0m").strip()
            try:
                x_coord, y_coord, z_coord = map(float, coordinates_input.split())
                grid_dimension = int(input("\033[1mEnter the grid dimension (integer): \033[0m").strip())

                # Generate updated XML and options files
                create_updated_xml_file(protein_id, x_coord, y_coord, z_coord, grid_dimension)
                options_files = create_options_files(protein_id, ligand_files)

                # After generating options files, create the docking job files
                create_docking_job_files(protein_id, options_files)
                print("\033[1mXML, options, and docking job files have been created.\033[0m")

            except ValueError:
                print("\033[1mInvalid input for coordinates or grid dimension.\033[0m")
    else:
        print("\033[1mInvalid docking type. Please enter 'local' for local docking.\033[0m")

# Example usage of the main function:
protein_id = input("\033[1mEnter the exact protein file name (including extension) for the simulation: \033[0m").strip()

protein_dir = os.path.join(os.getcwd(), 'protein_inputs')

if not os.path.exists(protein_dir):
    print(f"Directory '{protein_dir}' does not exist.")
else:
    protein_file = os.path.join(protein_dir, protein_id)

    if os.path.isfile(protein_file):
        print(f"Protein file '{protein_file}' found!")
        ligand_dir = os.path.join(os.getcwd(), 'ligand_inputs')
        ligand_check = input("\033[1mHave you placed your ligand files in SDF format in the 'ligand_inputs' directory? (yes/no): \033[0m").strip().lower()

        if ligand_check == 'yes':
            if os.path.exists(ligand_dir):
                ligand_files = [f for f in os.listdir(ligand_dir) if f.endswith('.sdf')]
                if ligand_files:
                    print("\033[1mLigand files in SDF format found in 'ligand_inputs':\033[0m")
                    for file in ligand_files:
                        print(f"  - {file}")

                    conformer_dir = os.path.join(ligand_dir, 'ligand_conformers')
                    if os.path.exists(conformer_dir):
                        missing_conformers = []
                        for ligand_file in ligand_files:
                            ligand_name = os.path.splitext(ligand_file)[0]
                            conformer_file = f"{ligand_name}_conformers.sdf"
                            conformer_path = os.path.join(conformer_dir, conformer_file)

                            if not os.path.isfile(conformer_path):
                                missing_conformers.append(ligand_file)

                        complexes_dir = os.path.join(ligand_dir, 'protein_ligand_complexes')
                        missing_complexes = []
                        if os.path.exists(complexes_dir):
                            for ligand_file in ligand_files:
                                ligand_name = os.path.splitext(ligand_file)[0]
                                complex_file = f"{os.path.splitext(protein_id)[0]}_{ligand_name}.pdb"
                                complex_path = os.path.join(complexes_dir, complex_file)

                                if not os.path.isfile(complex_path):
                                    missing_complexes.append(ligand_file)

                        if missing_conformers or missing_complexes:
                            print("\033[1m\nThe following issues were found:\033[0m")
                            if missing_conformers:
                                print("\033[1mLigands without conformer files:\033[0m")
                                for ligand in missing_conformers:
                                    print(f"  - {ligand}")
                            if missing_complexes:
                                print("\033[1mLigands without protein-ligand complexes:\033[0m")
                                for ligand in missing_complexes:
                                    print(f"  - {ligand}")

                            script_template_dir = os.path.join(os.getcwd(), 'script_templates')
                            conformer_template_file = os.path.join(script_template_dir, 'conformer_generation_template.txt')

                            if os.path.isfile(conformer_template_file):
                                with open(conformer_template_file, 'r') as template_file:
                                    template_content = template_file.readlines()

                                output_file_path = os.path.join(os.getcwd(), 'conformer_params_concatenation_job.txt')
                                with open(output_file_path, 'w') as output_file:
                                    for line in template_content:
                                        if line.startswith("./bcl.exe"):
                                            for ligand in missing_conformers:
                                                ligand_name = os.path.splitext(ligand)[0]
                                                modified_line = line.replace('AGA', ligand_name)
                                                output_file.write(modified_line)
                                        elif line.startswith("python ../../rosetta_package"):
                                            for ligand in missing_conformers:
                                                ligand_name = os.path.splitext(ligand)[0]
                                                modified_line = line.replace('AGA', ligand_name)
                                                output_file.write(modified_line)
                                        elif line.startswith("cat"):
                                            for ligand in missing_complexes:
                                                ligand_name = os.path.splitext(ligand)[0]
                                                modified_line = line.replace('7qgz', os.path.splitext(protein_id)[0]).replace('AGA', ligand_name)
                                                output_file.write(modified_line)
                                        else:
                                            output_file.write(line)

                                print(f"\033[1m\nConformer and params job file 'conformer_params_concatenation_job.txt' has been created at: {output_file_path}\033[0m")
                                print("\033[1mTo run the job, type: sbatch conformer_params_concatenation_job.txt\033[0m")
                                print("\033[1mTo check when your job starts and finishes, use the 'qs' command.\033[0m")
                                print("\033[1mOnce 'conformer_params_concatenation_job.txt' is done running, re-run this script.\033[0m")
                        else:
                            print("\033[1mAll ligands have corresponding conformer and protein-ligand complex files. Do you want to perform global or local docking?\033[0m")
                            docking_type = input("\033[1m(global/local): \033[0m").strip().lower()

                            if docking_type == 'global':
                                print("\033[1mGlobal docking is not yet available.\033[0m")
                            elif docking_type == 'local':
                                ready_for_input = input("\033[1mAre you ready to provide starting coordinates and docking grid dimensions? (yes/no): \033[0m").strip().lower()
                                if ready_for_input == 'no':
                                    print("\033[1mPlease look at the 'finding_input_coordinates_and_dimensions_guide' directory.\033[0m")
                                elif ready_for_input == 'yes':
                                    coordinates_input = input("\033[1mEnter x, y, z coordinates (e.g., 12.3 45.6 78.9): \033[0m").strip()
                                    try:
                                        x_coord, y_coord, z_coord = map(float, coordinates_input.split())
                                        grid_dimension = int(input("\033[1mEnter the grid dimension (integer): \033[0m").strip())
                                        create_updated_xml_file(protein_id, x_coord, y_coord, z_coord, grid_dimension)
                                        options_files = create_options_files(protein_id, ligand_files)
                                        create_docking_job_files(protein_id, options_files)
                                        print("\033[1mXML, options, and docking job files have been created.\033[0m")
                                        print("\033[1mIf you are ready to conduct the docking with all of the ligands currently in the ligand_inputs directory and you have 10 or fewer docking jobs for your protein, simply submit your docking jobs by typing 'sbatch [name of docking job file]' (e.g., sbatch 1B1_docking_job_1.txt) for each of your files and wait until the command prompt allows you to enter another command. If you have more than 10 docking job files, go ahead and execute the script called Rosetta_Docking_Part2.py by typing 'python Rosetta_Docking_Part2.py'. If you do not want to dock all of the ligands that you have in ligand_inputs, you can delete all of the docking job files in this directory for your protein, go into ligand_inputs and delete the SDF files of ligands that you don't want to dock, and then run this script again. Note that this script outputs docking job files for every ligand SDF file you have in ligand_inputs by default.\033[0m")
                                    except ValueError:
                                        print("\033[1mInvalid input for coordinates or grid dimension.\033[0m")
                            else:
                                print("\033[1mInvalid docking type.\033[0m")
                else:
                    print("\033[1mNo ligand files found in 'ligand_inputs'.\033[0m")
            else:
                print(f"\033[1mLigand directory '{ligand_dir}' does not exist.\033[0m")
    else:
        print(f"\033[1mProtein file '{protein_file}' not found. Make sure that you upload the file to protein_inputs and that you spell its name correctly.\033[0m")
