#!/bin/bash
#SBATCH --job-name=install_env_hpc
#SBATCH --partition=express
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=/home/BLAZERID/github/repo/envs/%x-%j.out

module purge
#module spider Anaconda3
module load Mamba
mamba env create -f /home/BLAZERID/github/repo/envs/env_hpc.yml