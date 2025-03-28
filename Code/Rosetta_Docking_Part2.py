import os

def main():
    # Step 1: Confirm if Rosetta_Docking_Part1.py has been run
    part1_status = input("\033[1mHave you run Rosetta_Docking_Part1.py? (yes/no): \033[0m").strip().lower()

    if part1_status == "no":
        print("\033[1mPlease run Rosetta_Docking_Part1.py first, ensuring you have your ligands in the 'ligand_inputs' directory and the cleaned protein structure in the 'protein_inputs' directory.\033[0m")
        print("\033[1mAlso, delete any docking job files in the current directory before proceeding.\033[0m")
        return

    if part1_status != "yes":
        print("\033[1mInvalid response. Please type 'yes' or 'no'.\033[0m")
        return

    # Step 2: Ask for the protein file name
    protein_file = input("\033[1mType the exact name of the protein file you plan on docking (with its extension): \033[0m").strip()
    protein_path = os.path.join("protein_inputs", protein_file)

    if not os.path.exists(protein_path):
        print(f"\033[1mProtein file '{protein_file}' not found in 'protein_inputs'. Please check your spelling and rerun Rosetta_Docking_Part2.py.\033[0m")
        return

    print(f"\033[1mProtein file '{protein_file}' found.\033[0m")

    # Step 3: Identify docking job files
    protein_base = os.path.splitext(protein_file)[0]
    docking_jobs = [f for f in os.listdir('.') if f.startswith(protein_base) and f.endswith(".txt")]

    if not docking_jobs:
        print(f"\033[1mNo docking job files found for protein '{protein_base}'. Please make sure to run Rosetta_Docking_Part1.py once you place your ligand in ligand_inputs and your protein in protein_inputs to ensure that they generate correctly.\033[0m")
        return

    print("\033[1mThe following docking job files were found:\033[0m")
    for job in docking_jobs:
        print(f"- {job}")

    print(f"\033[1mTotal number of docking job files: {len(docking_jobs)}\033[0m")

    # Step 4: Generate batch submission jobs
    template_path = os.path.join("script_templates", "multiple_job_submission_template.txt")

    if not os.path.exists(template_path):
        print(f"\033[1mTemplate file '{template_path}' not found. Ensure it is present in the 'script_templates' directory.\033[0m")
        return

    with open(template_path, 'r') as template_file:
        template_lines = template_file.readlines()

    sbatch_index = next((i for i, line in enumerate(template_lines) if line.startswith("sbatch ")), None)
    if sbatch_index is None:
        print("\033[1mNo 'sbatch' line found in the template file. Please check the template.\033[0m")
        return

    batch_size = 65
    for i in range(0, len(docking_jobs), batch_size):
        batch_jobs = docking_jobs[i:i + batch_size]
        batch_file_name = f"batch_submission_job_{i // batch_size + 1}.txt"

        with open(batch_file_name, 'w') as batch_file:
            for j, line in enumerate(template_lines):
                if j == sbatch_index:
                    batch_file.write(f"sbatch {batch_jobs[0]}\n")
                    for job in batch_jobs[1:]:
                        batch_file.write(f"sbatch {job}\n")
                else:
                    batch_file.write(line)

    print(f"\033[1mBatch submission jobs have been created: {len(docking_jobs) // batch_size + (1 if len(docking_jobs) % batch_size > 0 else 0)} files.\033[0m")
    print("\033[1mSubmit the batch jobs by typing 'sbatch [name of batch docking job file]' (e.g., sbatch batch_submission_job_1.txt). If you have multiple batch jobs, submit just one and wait at least 12 hours. If fewer than 10 jobs remain running after 12 hours (use 'qs' to check), feel free to submit another batch job. Otherwise, continue waiting. Submitting in this manner ensures that the priority of your jobs will remain high and that you will not take up too many resources from others who may need them.\033[0m")
    print("\033[1mWhen you finish running all docking jobs and wish to proceed to analysis, you should run the script titled 'directory_custodian.py' to delete unnecessary files like docking jobs you have finished running, SLURM outputs, options files, and XML files.\033[0m")

if __name__ == "__main__":
    main()
