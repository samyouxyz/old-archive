# HBond-DPI
A program that predicts H-bond in DNA-Protein complexes.
Detail: https://github.com/samyouxyz/old-archive/blob/master/hbond-dpi/hbond-dpi.pdf

### Overview
HBond-DPI is a program that predicts the possibility of hydrogen bond interactions that occur at DNA-binding site in protein. DNA-protein complexes used in this program were extracted from PDB and NPIDB. The residues are divided into data instances, each has 11 residues and each residue is translated into three features: (1) side chain pKa value, (2) hydrophobicity index, and (3) molecular mass of an amino acid. After standardization, all training data instances is fed into support vector machine model to build an estimator for predicting h-bond interactions in DNA-binding protein. The result of the program appears to be 90.73% accuracy with sensitivity of 65.82% and specificity of 95.10%, while the MCC is 0.62.

#### Requirement
* python 3
* sklearn 0.20
* numpy 1.16

#### Usage
  1.  Run in terminal: `$ python hbonddpi.py`. 
  2.  Wait for several seconds for SVM training.
  3.  Input protein sequence residues. Example: TNPYAMRLYESLCQYRKPDGSGIVSLKIDWIIERYQLPQSYQR
  4.  Output displays '0' for no H-bond and '1' for H-bond.
