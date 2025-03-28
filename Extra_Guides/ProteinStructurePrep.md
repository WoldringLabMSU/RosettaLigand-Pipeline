The main source for protein PDB files is the Protein Data Bank. However, most protein files sourced from here are not “clean” and therefore not immediately suitable for protein-ligand docking. To clean these proteins, you can use PyMOL. Instructions for cleaning protein files with PyMOL are provided next in steps 6-10.
1. Once you download the protein file from the PDB, open it in PyMOL.
2. Next to the protein name, click on ‘A’ and then click on ‘remove waters’ to get rid of any water molecules present.
![image](https://github.com/user-attachments/assets/bd01aa6f-d759-40b2-97c3-3203115e5c62)

3. Select Display > Sequence
![image](https://github.com/user-attachments/assets/a5d66579-9856-4780-8a64-ccbfac89de3b)

4. Highlight ligands, ions, and/or other non-protein entities in the sequence for deletion (if you want to dock only a certain part of the protein, you can highlight parts of the protein for deletion as well). Next to the (sele) menu, click on A and then click on ‘remove atoms’.
![image](https://github.com/user-attachments/assets/a528a973-1af5-4f36-b115-e3201fe6a25d)

5. Now you need to save the file. Go to File > Export Molecule > Save. On Mac, the file saves as a .cif by default, so you should select the option to save it as a .pdb file.
