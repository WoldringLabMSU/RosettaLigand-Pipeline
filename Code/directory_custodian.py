import os
import glob

def main():
    # Ask the user if they have finished running all docking jobs
    response = input("\033[1mHave you finished running all the docking jobs you wanted to run? (yes/no): \033[0m").strip().lower()

    if response != "yes":
        print("\033[1mPlease wait until all your jobs have finished running before using this script.\033[0m")
        return

    # Delete .txt and .out files in the current directory
    print("\033[1mDeleting .txt and .out files in the current directory...\033[0m")
    for extension in ["*.txt", "*.out"]:
        for file in glob.glob(extension):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")

    # Delete .txt files in the options_inputs directory
    options_inputs_path = os.path.join(os.getcwd(), "options_inputs")
    if os.path.exists(options_inputs_path):
        print("\033[1mDeleting .txt files in the options_inputs directory...\033[0m")
        for file in glob.glob(os.path.join(options_inputs_path, "*.txt")):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")

    # Delete .xml files in the xml_inputs directory
    xml_inputs_path = os.path.join(os.getcwd(), "xml_inputs")
    if os.path.exists(xml_inputs_path):
        print("\033[1mDeleting .xml files in the xml_inputs directory...\033[0m")
        for file in glob.glob(os.path.join(xml_inputs_path, "*.xml")):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")

    print("\033[1mFile cleanup completed.\033[0m")
    print("\033[1mNote that this script did not delete ligand SDF files in ligand_inputs, ligand conformer files in ligand_inputs/ligand_conformers, protein-ligand complex files in ligand_inputs/protein_ligand_complexes or any files in ligand_inputs/molfile_to_params_outputs. This is to make the docking setup faster if you want to perform docking simulations with the same ligands in the future. If you do not want to use the same ligands in the future, you should eventually delete these files since they will accumulate as you dock more and more ligands \033[0m")

if __name__ == "__main__":
    main()
