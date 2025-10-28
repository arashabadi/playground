#!/bin/bash
#SBATCH --job-name=scanvi
#SBATCH --partition=pascalnodes 
#SBATCH --gres=gpu:4
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=120G
#SBATCH --time=12:00:00
#SBATCH --output=/home/BLAZERID/github/repo/analysis/03_annotation/scANVI/job/logs/%x-%j.out

# Load conda from cluster modules
module purge

#module load Anaconda3
module spider Anaconda3
conda activate env_hpc

# Debug info
which python
python --version
nvidia-smi

# Run script
python /home/BLAZERID/github/repo/analysis/03_annotation/scANVI/job/scripts/run_scanvi.py
