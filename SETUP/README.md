# My Protocols For HPC & Local Workspace Setup 
> A cloudy afternoon in Shelby building, May 2025. A week after joining the lab. Quite frankly, I don't know where to start... Anaconda, Jupyter, [VSCode PETS](https://marketplace.visualstudio.com/items?itemName=tonybaloney.vscode-pets), Singularity, Docker, Nextflow, Slurm, Login node, Compute node, Seurat, Scanpy, Bash, R, Python, Julia, Rust, Biostatistics, Linear Algebra, Differential Equations, Pytorch, Tensorflow, Machine Learning, Deep Learning, Neural Networks, GNN, CNN, VAE, GAN, diffusion models, etc. For god's sake! I am a biologist, not an engineer!!


> I'm sure I'll figure it out as I go along, but I'm also sure I'll forget everything and have to start over again!


## Table of Contents
- [HPC](#hpc)
- [Local_MacOS](#local_macos)
- [Local_Windows](#local_windows)

## HPC
### UAB Cheaha Supercomputer
- where Alabama's natural beauty meets computational chaos, because nothing says "high-performance computing" like a server room that occasionally gets visited by curious raccoons!


- [Cheaha User Guide](https://docs.rc.uab.edu/)
-----
### Running interactive RStudio session on top of created anaconda environment
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


Note: in an R Markdown (.Rmd) document, a code chunk like this:
    ```{python}
    print("Hello from Python!")
    ```
**does run using `reticulate`** under the hood, as long as:
- The `reticulate` package is installed (available in the conda environment) and loaded.
- The Python environment is correctly configured via `reticulate::use_condaenv()`



🛠️ How to control the Python environment
If you want to explicitly specify the Python or conda environment used, include this in a setup chunk before any Python code:

```r
```{r setup, include=FALSE}
library(reticulate)
use_condaenv("myenv", required = TRUE)
```

Or if you're using virtualenv:
```r
use_virtualenv("myenv", required = TRUE)
```


### Connect conda environment and Kernel in JupyterLab

```{bash}
module load Anaconda3
conda activate myenv
python -m ipykernel install --user --name jlenv --disply-name "jlenv"
```


## Local_MacOS

will be completed soon!



## Local_Windows

#### Run Conda in Git Bash
> As I have been struggling to run any bash commnads in windows cmd or powershell, it's been a while I'm using Git Bash. It's super clean, fast and compatible with almost all unix commands. Git Bash can be more than version control or pushing to github. Here I show how to run conda commands in Git Bash:

0. Install Miniconda for Windows from [Link](https://docs.conda.io/en/latest/miniconda.html)

1. Find `conda.sh` from Anaconda PowerShell: Open **Anaconda PowerShell Prompt** (the one that works with `conda` command).

2. Run the following command to locate the Conda base path:

   ```powershell
   echo $env:CONDA_PREFIX
   ```

   This will give you something like:

   ```
   C:\Users\<username>\Miniconda3
   ```

3. Now check if the `conda.sh` script exists by navigating to:

   ```powershell
   Get-ChildItem "$env:CONDA_PREFIX\etc\profile.d"
   ```
   You're looking for a file named **`conda.sh`** and copy Directory path.

4. Once you confirm the full path to `conda.sh`, switch back to Git Bash & run this to enable Conda temporarily:

    ```bash
    source /c/ProgramData/miniconda3/etc/profile.d/conda.sh
    ```

    Then verify:

    ```bash
    conda --version
    conda activate base
    ```

    You should see `(base)` appear in your prompt.

5. Now Make Conda available every time

    Add this line to your Git Bash startup file (`~/.bashrc`):

    ```bash
    echo 'source /c/ProgramData/miniconda3/etc/profile.d/conda.sh' >> ~/.bashrc
    ```
    Then reload:

    ```bash
    source ~/.bashrc
    ```
* Next time running Git Bash, you may see a warning of  incorrect setup. You can ignore it cause the next time:

    - ~/.bash_profile will run automatically
    - It will source ~/.bashrc
    - And that will source the conda.sh script
    - So conda will be available from the start 🎉


-----

#### Setup SSH into Cheaha through Git Bash








#### The problem of Remote-SSH in VSCode and login node access in Cheaha!

> Nothing should be run on the login node, especially IDE SSH sessions. Any processes run in or by these IDEs are run using login node resources. Even if you request an interactive job within the IDE, only the processes run within that terminal session are on the compute node, everything else is still run on the login node. We automatically kill any IDE server process on the login node. If you want to use an IDE to access Cheaha, we have documentation on how to use VSCode to access a compute node directly on our documentation at [Link](https://docs.rc.uab.edu/cheaha/open_ondemand/hpc_desktop/#downloading-and-installing-vscode-and-vscode-server).

