# My Protocols For HPC & Local Workspace Setup 
- A cloudy afternoon in Shelby building, May 2025. A week after joining a lab in immunology. Quite frankly, I don't know where to start... Man! I am a biologist, not an engineer! 
- Anaconda, Jupyter, [VSCode PETS](https://marketplace.visualstudio.com/items?itemName=tonybaloney.vscode-pets), Singularity, Docker, Nextflow, Slurm, Login node, Compute node, Seurat, Scanpy, Bash, R, Python, Julia, Biostatistics, Linear Algebra, Differential Equations, Pytorch, Tensorflow, Machine Learning, Deep Learning, Neural Networks, GNN, CNN, VAE, GAN, diffusion models, etc. 

- I'm sure I'll figure it out as I go along, but I'm also sure I'll forget everything and have to start over again!

## HPC
### UAB Cheaha Supercomputer
- where Alabama's natural beauty meets computational chaos, because nothing says "high-performance computing" like a server room that occasionally gets visited by curious raccoons!


- [Cheaha User Guide](https://docs.rc.uab.edu/)

#### Running interactive RStudio session on top of created anaconda environment
- There is a documentation for this in [Link](https://docs.rc.uab.edu/cheaha/open_ondemand/ood_rstudio/). I have added a few more steps to make it work.
```{bash}
# Environment Setup window (brfore running interactive RStudio):
module load Anaconda3
conda activate myenv
```
```{r, include=FALSE} 
# libraries to load
Sys.which("R") # to check env address 
reticulate::use_condaenv('myenv')
.libPaths() # to check lib address
.libPaths(c("/data/user/home/BlazerID/.conda/envs/combined/lib/R/library"))

suppressPackageStartupMessages({
  library(Seurat)        # core single‑cell toolkit
  library(dplyr)         # tidy utilities
  library(ggplot2)       # plotting
})
```

## Local (Windows)

- The problem of Remote-SSH in VSCode and login node access in Cheaha!

> Nothing should be run on the login node, especially IDE SSH sessions. Any processes run in or by these IDEs are run using login node resources. Even if you request an interactive job within the IDE, only the processes run within that terminal session are on the compute node, everything else is still run on the login node. We automatically kill any IDE server process on the login node. If you want to use an IDE to access Cheaha, we have documentation on how to use VSCode to access a compute node directly on our documentation at [Link](https://docs.rc.uab.edu/cheaha/open_ondemand/hpc_desktop/#downloading-and-installing-vscode-and-vscode-server).


## Local (MacOS)

