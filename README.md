# QuantumBind-RBFE

## Summary

QuantumBind-RBFE is Acellera's implementation for Relative Binding Free Energy (RBFE) calculations. This approach is based on the Alchemical Transfer Method (ATM) and incorporates Neural Network Potentials (NNP) within a hybrid NNP/MM framework. The data in this repository was used in the accompanying manuscript: [QuantumBind-RBFE: Accurate Relative Binding Free Energy Calculations Using Neural Network Potentials](https://arxiv.org/abs/2501.01811).

## Contents

- **`inputs/`**: Contains input files for binding free energy calculations.
- **`results/`**: Includes ΔΔG and ΔG values from the runs presented in our manuscript.
- **`tutorial/`**: Provides a Jupyter notebook offering a step-by-step tutorial on setting up and running a QuantumBind-RBFE calculation.
- **`scripts/`**: Contains the necessary scripts to execute the production phase using the provided input files.

## Prerequisites

QuantumBind-RBFE can be run via [Acellera-ATM](https://github.com/Acellera/atm) and [HTMD](https://software.acellera.com/htmd/index.html), Acellera's molecular modeling environment. Ensure that you have both repositories installed and properly configured to execute the provided scripts and workflows.

## References

- **AceForce**:  
  If you wish to use the AceForce model, Acellera's own NNP, it can be found on Hugging Face: [AceForce 1.0](https://huggingface.co/Acellera/AceForce-1.0).  
  AceForce 1.0 is available for non-profit use and demonstrations, allowing researchers to explore its potential in their projects.

