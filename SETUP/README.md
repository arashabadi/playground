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

First create an environment with specific YAML file:
```{bash}
conda env create -f myenv.yaml
conda env list # to check if the environment is created
```

Then activate the environment:
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
-----

#### Export conda environment

I wanted to clarify an important detail regarding the use of `conda env export` when sharing or recreating environments across different systems.

By default, `conda env export` includes **OS-specific details** such as build strings and dependency variations that may differ between macOS, Linux, and Windows. This means that an environment file exported on one system might not work seamlessly on another due to these platform-dependent elements.

To make the environment file more portable and cross-platform compatible, it's recommended to use the `--no-builds` flag, like so:

```bash
conda env export --no-builds > env_no_builds.yml
```

This omits build-specific metadata. Additionally, to ensure no system-specific file paths are included (e.g., the local environment `prefix`), you can run:

```bash
conda env export --no-builds | grep -v "prefix:" > env_no_builds.yml
```

This approach helps create cleaner, more reproducible environment files that can be used reliably across different operating systems.


It depends on how “complete” you need your spec to be versus how much you want Conda to re-solve dependencies per OS:

---

## 1. `--no-builds`

* **What it does**
  Exports the *entire* dependency tree (all direct + transitive deps) with exact versions but strips out platform-specific build hashes.
* **Resulting file**

  ```yaml
  dependencies:
    - python=3.10.4
    - numpy=1.24.3
    - pandas=2.0.1
    - scipy=1.11.0
    …  
  ```
* **Pros**

  * You get *every* package you had, so reproduction is closer to the original.
  * No build strings → Conda picks the latest compatible build on each OS.
* **Cons**

  * You’ll also pull in Linux-only libraries (e.g. `libgcc-ng`) that may fail on macOS/Windows unless you manually prune them.

---

## 2. `--from-history`

* **What it does**
  Exports *only* the packages you explicitly installed (`conda install X Y Z`), without any build strings or transitive deps.
* **Resulting file**

  ```yaml
  dependencies:
    - python=3.10
    - numpy
    - pandas
    - pip
    - pip:
        - fastapi>=0.95.0
        - torch
  ```
* **Pros**

  * Minimal: Conda re-solves the full dependency graph on the target OS, automatically choosing the right platform variants.
  * Very portable across Linux, macOS, Windows.
* **Cons**

  * You may need to add back in any low-level package you specifically need (e.g. a special C library) if it doesn’t get pulled in.

---

## 3. Which to pick for Linux → Windows/macOS?

* **For maximum portability:**
  Use **`--from-history`**. It hands off all the dependency solving to the target OS, avoiding leftover Linux-only bits.

  ```bash
  conda env export --from-history \
    | grep -v '^[[:space:]]*prefix:' \
    > environment-minimal.yml
  ```
* **If you really need the full tree** (e.g. you know every transitive dep is cross-platform), use **`--no-builds`**, then manually remove any errant Linux-only packages:

  ```bash
  conda env export --no-builds \
    | grep -v '^[[:space:]]*prefix:' \
    > environment-full-portable.yml
  ```



1. Try **`--from-history`** first—most cross-platform workflows are covered by rescanning your top-level specs.
2. If you hit “missing dependency” errors, generate a **`--no-builds`** export and cherry-pick or prune Linux-only entries.

This two-step approach gives you both portability and completeness.


-----

### Connect conda environment and Kernel in JupyterLab

```{bash}
module load Anaconda3
conda activate myenv
python -m ipykernel install --user --name myenv --disply-name "myenv"
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

* Channel configuration for conda:
```{bash}
conda config --show channels
```
add channels
```{bash}
conda config --add channels conda-forge && conda config --add channels bioconda && conda config --add channels r
```
remove channels
```{bash}
conda config --remove channels conda-forge && conda config --remove channels bioconda && conda config --remove channels r
```

- Note: Installing bioconductor packages on windows via conda is headache!! Try tostick to linux for 100% reproducibility!

-----

#### Setup SSH into Cheaha through Git Bash








#### The problem of Remote-SSH in VSCode and login node access in Cheaha!

> Nothing should be run on the login node, especially IDE SSH sessions. Any processes run in or by these IDEs are run using login node resources. Even if you request an interactive job within the IDE, only the processes run within that terminal session are on the compute node, everything else is still run on the login node. We automatically kill any IDE server process on the login node. If you want to use an IDE to access Cheaha, we have documentation on how to use VSCode to access a compute node directly on our documentation at [Link](https://docs.rc.uab.edu/cheaha/open_ondemand/hpc_desktop/#downloading-and-installing-vscode-and-vscode-server).

