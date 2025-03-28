### You will need to know exactly where in the protein you will want the docking simulation to occur. 

1. Open the protein file that you inputted into the docking workflow in PyMOL (this file should already be in the `protein_inputs` directory).  

2. Toggle through the lower right-hand menu by clicking on the word immediately to the right of 'Selecting' until 'Atoms' appears. Now you can select a single starting coordinate of your choice by clicking on the structure. See the image below if unclear.

<p align="center">
  <img src="https://github.com/user-attachments/assets/aad337dc-11d5-4e4c-9877-4ea343b5ba0d" width="200">
</p>

3. Once you've decided on a starting coordinate, click on the structure where you want the starting coordinate to be located. A pink dot should appear.

<p align="center">
  <img src="https://github.com/user-attachments/assets/0be83d5e-10e6-4c80-956f-98054c365796" width="300">
</p>

4. In the PyMOL command line, type the following: iterate_state 1, sele, print(x,y,z). This will give you the starting coordinate of the selected pink dot. Record this somewhere so you can input it when prompted to do so by this script.

<p align="center">
  <img src="https://github.com/user-attachments/assets/a2875a40-5274-49bb-9aeb-4d5615633ff7" width="300">
</p>

5. There is no need to record all decimal points in the coordinates--three should be enough.  

6. To find grid dimensions for docking using PyMOL, imagine a cubic volume where you want your ligand(s) to move during the simulation, centered at the starting coordinate. Your task is simply to find the side dimension of this cube.  

7. Click on the 'M' in the lower right-hand panel in PyMOL. It should be a blue letter right above 'Move'. If you click on the structure now, a white dot should appear. See the image below if unclear.
<p align="center">
  <img src="https://github.com/user-attachments/assets/11d3c71f-8f62-4129-a0df-dcb1bfb5765e" width="300">
</p>

8. Now you can measure distances. Simply click on another part of the protein to measure the distance between the original white dot and the second one which you will now place. The distance in Angstroms will appear, along with a dashed line. You can remove either of the dots (or both) simply by clicking on them again. Use this measuring tool to estimate a reasonable length for the side of the cubic simulation volume. See the image below if unclear.
<p align="center">
  <img src="https://github.com/user-attachments/assets/f7549ffe-ad35-4f56-9508-15e9032ea498" width="300">
</p>

