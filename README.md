# Simplified Rosetta Docking Workflow Tutorial
### By Theodore Belecciu (@Theodor-ator)
##### Last updated: 1/15/2025

<i>This guide provides step-by-step instructions for using a simplified Rosetta protein-ligand docking workflow. This workflow was developed to be easy to use even for those with only basic knowledge of the Linux shell. PyMOL and access to an MSU HPCC account are the only requirements.</i>

Prior to installing anything in your home directory, please ensure that you have enough memory available. Enter HPCC using a command prompt and type ‘quota’ to see your memory usage. You’ll need at least 36 GB of free space to install Rosetta with this workflow. You’ll also need about 190 MB of space for every ligand you plan on docking (~13 GB for every 65 ligands assuming you generate 1000 outputs for each ligand). The default HPCC storage is 50 GB, but they will begin limiting all home directories to 100 GB on January 20th (you will receive an email from them when your home directory is scheduled for this change). You will also no longer be able to request up to 1 TB of storage space, since they decided to make 100 GB a hard limit, but our lab research directory will now be able to store up to 3 TB. This workflow will be installed there for group use as well. See the [ICER blog](https://blog.icer.msu.edu/announcement/maintenance/2025/01/12/New-Homedir-Transition) for details on the HPCC memory changes.

Example of quota command:
<p align="center">
  <img src="https://github.com/user-attachments/assets/66be4a08-8cb6-4cec-9d05-ee64f879b646" width="500">
</p>

You should also be familiar with the [HPCC OnDemand interface](https://ondemand.hpcc.msu.edu) for file visualization and management on HPCC. Other file management interfaces like FileZilla can be used, but HPCC OnDemand is automatically available to all who have an HPCC account, and it will be used in this guide.


## Installing Rosetta and the Workflow Directory Structure
Once you have an HPCC account, you can copy Rosetta and all the necessary directories and files directly from my home directory (/mnt/home/belecciu). If you already have Rosetta in your home directory and would like to use that installation in the workflow instead, feel free to skip to the next section.

1.	To install Rosetta and all the necessary files in your home directory, you should run the SLURM job file [`cp_job.sb`](https://github.com/WoldringLabMSU/BINDSMART/blob/main/RosettaLigand-Pipeline/Code/cp_job.sb)
2.	&#9888; <b>Important!</b> Before running this SLURM job file, make the following change to it: replace the ‘aljetsal’ with the name of your HPCC home directory (generally your MSU NetID).
3.	Place this SLURM file in your home directory using HPCC OnDemand. Run it by typing `sbatch cp_job.sb`.
4.	This will take take approximately 40 minutes to run, as you are transferring a large directory (~36G). You can check the progress of your job by typing `qs` in the command prompt. If no job ID and time appear, the transfer has completed.
5.	You should now see a directory called streamlined_docking in your home directory if you type `ls`. 

<i>NOTE: If you already had Rosetta installed in your home directory, there is no need to copy it from my directory. You can copy the entire directory structure and workflow without Rosetta by making the changes to the [`cp_job.sb`](https://github.com/WoldringLabMSU/BINDSMART/blob/main/RosettaLigand-Pipeline/Code/cp_job.sb) SLURM job to match the code in the below figure. </i>
<p align="center">
  <img src="https://github.com/user-attachments/assets/9e5470f0-679f-45c8-829b-cea13c549976" width="500">
</p>

<i>NOTE: Within the workflow directory, there is a `bcl_package` subdirectory containing a license that will need to be renewed annually. I’m fairly certain you can still use my license from 2024, but you should check if mine is valid for you simply by going into the bcl_package directory with your command prompt and typing `./bcl.exe`. If you get a wall of text once you do this, your license should be good until March 23rd of 2025. If you do not get this, you will need a license which you can obtain from [here](http://servers.meilerlab.org/index.php/servers/bcl-academic-license). After obtaining a license, upload it to the `bcl_package` directory.</i> 

## File Preparation for Docking
1.	Enter the streamlined_docking directory.
2.	You will need to upload a cleaned PDB file of the protein you want to dock (no cofactors, ions, waters, or other ligands) into the `protein_inputs` directory. A guide for protein structure preparation is provided in [Extra_Guides/ProteinStructurePrep.md](https://github.com/WoldringLabMSU/RosettaLigand-Pipeline/blob/main/Extra_Guides/ProteinStructurePrep.md).
3.	Likewise, you will need to upload 3D ligand files in SDF format into the `ligand_inputs` directory. There are many sites that you can obtain these from, but PubChem has the largest collection. Do not upload your files to these subdirectories seen within. Upload them only to `ligand_inputs`. Other files generated by the docking workflow will populate these subdirectories.
4.	You will need to know exactly where in the protein you want the docking simulation to occur. A guide to do this is provided in [Extra_Guides/DeterminingDockingCoordinates.md](https://github.com/WoldringLabMSU/RosettaLigand-Pipeline/blob/main/Extra_Guides/DeterminingDockingCoordinates.md)

## Docking Workflow Part 1
1.	Now you are ready to execute the docking workflow! Navigate to the `streamlined_docking` directory where the scripts `Rosetta_Docking_Part1.py`, `Rosetta_Docking_Part2.py`, and `directory_custodian.py` are located.
2.	Type `python Rosetta_Docking_Part1.py` into the command prompt.
    * The script will ask you to type the name of the protein file you intend on docking. Refer to your `protein_inputs` directory and make sure you type the name exactly, with its .pdb extension; the script will fail to identify it otherwise.
    * If you misspell the name and the script tells you it cannot find your protein file, simply run the script again. The script will tell you that it found the file if you typed it correctly.
    * Example prompts below:
    <p align="center>
      <img src="https://github.com/user-attachments/assets/dd3dcbc7-522e-4b80-ac4d-822d5f86eae4">
    </p>
3.	Once your protein file has been located, the script will ask you if you have placed your ligand SDF files in the ligand_inputs directory. Type ‘yes’ if you have. If you say ‘no’, the script will simply tell you to upload them there and then run the script again. If you type ‘yes’ but you actually didn’t, the script will tell you that it couldn’t find any. In that case, you’ll also have to run the script again once you put the ligand files in ligand_inputs.
	    * <i>NOTE: As a general rule, if the script does not produce an output, or if it tells you that you made an invalid input, or if it tells you that it couldn’t find something, the script didn’t do anything wrong—you probably did! Check your files and spelling and simply run it again.</i>
<p align="center>
  <img src="https://github.com/user-attachments/assets/03e60292-8bb7-4ca6-b1fb-4ea78b514b5f" width="500">
</p>

4.	If everything is good so far, the script will check to see if you have ligand conformer files and protein-ligand complex files. It will report the ligand files that are not complexed with your protein and those that are lacking conformer files. (if you’re running docking for the first time you definitely won’t have these files, but don’t worry—the script will generate them for you!). Example below:  
<p align="center">
  <img src="https://github.com/user-attachments/assets/c53c3c07-af9e-4725-a99c-a313739a3a9d" width="500">
</p>

5.	If this is the case, simply follow the script’s instructions and type `sbatch conformer_params_concatenation_job.txt` into the command prompt. This will submit a SLURM job that will address all of these missing files. This job may take some time, depending on the number of ligands that are missing conformer files. As the script says, you can check when the job finishes with the `qs` command. Now, you will have conformer and protein-ligand complex files for your ligands. Run the script again, and you should receive the following output after responding with `yes` to the question about placing your ligand files in ligand_inputs:
<p align="center">
  <img src="https://github.com/user-attachments/assets/a70a28e6-d152-410e-894f-d497d65c0d97" width="500">
</p>

6.	The script always checks for missing ligand conformer and protein-ligand complex files when you run it, and if it sees that none are missing it enables you to go to this next step. Global docking is not available as a feature yet, and if you type that in as a response, you’ll simply have to run the script again.
7.	Once you type `local`, you are able to enter the starting coordinates and grid dimensions you determined for your protein earlier. See the image below for an example input:
<p align="center">
  <img src="https://github.com/user-attachments/assets/d7e5fb00-f99b-435a-a448-fd5a4092e83b" width="500">
</p>

8.	Now, the script will make an XML file, options files, and docking job files. In brief, the XML file tells Rosetta what sort of movements and physics to use for your system. The options files tell Rosetta what score function it should use, where it can find the important files it will need, and how many outputs to produce. The docking job files are the commands that you will submit to actually start the docking simulations. The script generates a docking job file and an options file for each ligand you place in ligand_inputs, so if you have many ligands, the script will generate many such files.If you didn’t generate too many docking job files, you should submit the docking jobs now! Do so simply by typing `sbatch [name of docking job file]` for each file (e.g., sbatch 8hnd_test_docking_job_1.txt), waiting until the command prompt tells you that a job was submitted before submitting the next one. If you have many docking job files that you need to run and feel that it would be inconvenient to submit all of them manually, you can instead follow the suggestions of the script and execute [`Rosetta_Docking_Part2.py`](https://github.com/WoldringLabMSU/RosettaLigand-Pipeline/blob/main/Code/Rosetta_Docking_Part2.py) (see example output below)

 <p align="center">
   <img src="https://github.com/user-attachments/assets/9215a7cf-0ecd-41cd-ab95-20b14ca26287" width="500">
 </p>

<i>NOTE: All submitted docking jobs, once running, will begin producing results in the form of zipped protein-ligand complexes and a score file. These will go into a folder named after your protein in the docking_results directory within streamlined_docking.</i>

## Docking Workflow Part 2

1.	If you have a large number of docking job files, you should execute [`Rosetta_Docking_Part2.py`](https://github.com/WoldringLabMSU/RosettaLigand-Pipeline/blob/main/Code/Rosetta_Docking_Part2.py) by typing `python Rosetta_Docking_Part2.py` (the number 10 is given by the first script in the command prompt as a quantity that may not be convenient to submit manually, but there is no upper or lower limit to using Rosetta_Docking_Part2.py). This script will not do anything if you did not obtain docking job files by using Rosetta_Docking_Part1.py first, so you cannot run it before Rosetta_Docking_Part1.py. Regardless, it will still ask you if you ran `Rosetta_Docking_Part1.py`. It will also ask you for the exact protein file name that you are interested in docking. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/2d9f7006-b231-4f54-9e74-ac21b5070ec0" width="500">
</p>

2.	Rosetta_Docking_Part2.py will then count the number of docking job files you have and it will generate batch submission jobs. These batch submission jobs can submit a maximum of 65 docking jobs simultaneously (and a minimum of 1 job). If you have more than 65 docking jobs, multiple batch submission jobs will be created to house all the docking jobs. For instance, if you have 175 docking jobs, three batch submission jobs will be created and they will be named batch_submission_job_1.txt, batch_submission_job_2.txt, and batch_submission_job_3.txt. You can submit these batch jobs by typing ‘sbatch [name of batch submission job]’ (e.g., sbatch batch_submission_job_1.txt). Note: you should never submit more than one batch submission job at a time. If you do so, the SLURM system will put many of those jobs on very low priority, and they’ll actually take longer to submit than if you submit just one batch submission job and wait. This is also a useful precaution against hitting your memory cap. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/08f1c672-2a0d-49f4-a59f-c8ec70bd6e2a" width="500">
</p>

3.	This batch job may take some time to submit, but once it does, it will begin submitting the docking jobs one by one automatically. If you type `qs` during this phase, you will see a growing list of submitted jobs. This is normal. A batch job containing 65 ligand files usually takes about a full day to run.

<i>NOTE: when you submit jobs and run `qs`, you might see N/A in the ‘Start_Time’ field. This is also normal and simply means that the SLURM system hasn’t scheduled your job yet. If you want to cancel a job for whatever reason, type `scancel [number in JobID field]` (e.g., scancel 48466347).</i>

4.	The output of the command prompt shown in the above figure mentions a script called [`directory_custodian.py`](https://github.com/WoldringLabMSU/RosettaLigand-Pipeline/blob/main/Code/directory_custodian.py) that should be run after the batch submission jobs have finished running. That script will delete all docking job files, all batch submission jobs, all SLURM outputs, all options files, and all XML files. It is highly recommended that you run this script after you finish running all docking job files (or all batch submission jobs) for a given protein. See example output below:

<p align="center">
  <img src="https://github.com/user-attachments/assets/83f55cb2-16bf-4ec6-bc9c-e8dbd5690f15" width="500">
</p>

5.	These are not necessarily the only files you should delete. If you want to dock different ligands in the future, you should delete all ligands that you no longer want to dock from the `ligand_inputs` directory.






