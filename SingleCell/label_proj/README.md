
# scANVI Tutorials and Pipelines

1. Basic Integration & Label Transfer
	•	Goal: Train scANVI from scratch with a labeled reference and an unlabeled query, then transfer labels.
	•	Best for: Standard label transfer workflows (e.g., cross-study or cross-tech).
	•	Tutorial link: Integration and label transfer with Tabula Muris
https://docs.scvi-tools.org/en/1.3.2/tutorials/notebooks/scrna/tabula_muris.html
⸻

2. Seed Labeling (Partial Labels)
	•	Goal: Start with a small set of seed labels and propagate them across unlabeled cells using scANVI.
	•	Best for: When you have very few annotated cells.
	•	Tutorial link: Seed labeling with scANVI
https://docs.scvi-tools.org/en/1.3.2/tutorials/notebooks/scrna/seed_labeling.html
⸻

3. scArches “Surgery” with scANVI
	•	Goal: Train a reference model once, then update (“surgery”) with new query data without full retraining.
	•	Best for: Mapping multiple new datasets efficiently into the same reference space.
	•	Tutorial link: Semi-supervised scANVI surgery pipeline (scArches)
https://docs.scarches.org/en/latest/scanvi_surgery_pipeline.html
⸻

4. Reference Mapping with scArches (SCVI/SCANVI/TOTALVI)
	•	Goal: Map new query data onto an existing pretrained model (SCVI, SCANVI, or TOTALVI) using scArches.
	•	Best for: Large-scale projects, multimodal data (e.g., CITE-seq), or when you need consistent embeddings across many queries.
	•	Tutorial link: Reference mapping with SCVI-Tools (multimodal)
https://docs.scvi-tools.org/en/1.3.2/tutorials/notebooks/multimodal/scarches_scvi_tools.html
⸻

5. API Reference (for custom pipelines)
	•	Goal: Learn available functions, parameters, and usage for scANVI in scvi-tools.
	•	Best for: Building your own pipeline, tuning hyperparameters, or integrating with custom preprocessing.
	•	Docs link: scANVI API — scvi-tools
https://docs.scvi-tools.org/en/stable/api/reference/scANVI.html

-----

# scANVI label transfer on AnnData

This README documents a robust recipe to transfer cell type labels from a labeled reference AnnData to an unlabeled query AnnData using scvi-tools scANVI on GPU nodes.

> You need to first install `env_hpc.yml` which will make your conda environment on cheaha (try installing through running `./scripts/install_env_hpc.sbatch`).
> After optimizing your code for the ref and query datasets, run scANVI through `./scripts/run_scanvi.sbatch`. Make sure you are having existing empty directories of `./logs/` and `./outputs/`.


Tested with: 
- Python 3.12.11
- scvi-tools 1.3.3, Scanpy 1.11.3
- PyTorch 2.5.1 + Lightning 2.x
- GPUs: NVIDIA A100 and P100 on UAB Cheaha HPC


## What you get
- A single output H5AD: `scanvi_label_transfer.h5ad` that contains
  - `obs['dataset']` = ref or qry
  - `obs['pred_label']`, `obs['pred_conf']`
  - `obsm['X_scANVI']` latent embedding
- Saved model directories: `model_scvi/`, `model_scanvi/`


## Input requirements for reference vs query AnnData

| Aspect | Reference AnnData (ref) | Query AnnData (qry) | Why it matters |
|---|---|---|---|
| Raw counts availability | Must have raw counts in `ref.raw.X` | Must have raw counts in `qry.layers['counts']` | scVI/scANVI are trained on counts. |
| Counts layer | Exposed as `ref.layers['counts']` from `ref.raw.X` by the script | Already present as `qry.layers['counts']` | Keeps memory efficient sparse CSR float32. |
| Gene identifiers | Prefer gene symbols in `.var_names` or provide a column `symbol` or `gene_name` to normalize | Same | Ensures proper intersection across ref and qry. |
| Species | Same species across ref and qry | Same | Mixed species requires ortholog mapping first. |
| Labels column | Must have `ref.obs['author_cell_type']` (or adapt the script) | Not required | scANVI needs supervision only on ref. |
| QC status | Already QC-filtered cells and genes preferred | Same | Cleaner HVGs and more reliable mapping. |
| Batch tags | Optional | Optional | The script uses a synthetic `dataset` batch so batch tags are not required. |
| Size balance | Reasonable numbers per class. Rare classes can be merged to an Other bucket | N/A | Avoids degenerate classes and improves transfer. |

Notes
- `.var_names` will be made unique and intersected. Ref-only zero columns are pruned before intersection.
- If you renamed the reference labels column, update `LABEL_COL_IN_REF` in the script.


## Directory layout and paths
The script expects:
```
DATA_DIR/                       # input data
  c2_2_adata_raw_qc_doublet.h5ad   # query
  anndata_ibalt_xenium.h5ad        # reference
analysis/03_annotation/scANVI/job/
  scripts/run_scanvi.py            # this script
  outputs/                         # models and final h5ad will land here
  logs/                            # sbatch logs
```
Edit the `DATA_DIR`, `QRY_PATH`, and `REF_PATH` variables if your layout is different.


## Environment setup
Use the supplied environment YAML or create one manually. Example with mamba on HPC:
```bash
module load Mamba
mamba env create -f /path/to/environment-cheaha-gpu.yml
# or, if creating manually with PyTorch channel builds:
# mamba create -n scanvi python=3.12 scvi-tools=1.3.3 scanpy=1.11.3 pytorch=2.5.1 torchvision=0.20.1 torchaudio=2.5.1 pytorch-cuda=12.4 -c pytorch -c nvidia -c conda-forge
```
Activation in batch jobs must initialize the shell, for example:
```bash
# inside your sbatch script, before conda activate
source "$HOME/miniconda3/etc/profile.d/conda.sh" || eval "$(conda shell.bash hook)"
conda activate memory_rechallenge_v2_hpc
```
Tip
- Prefer `pytorch-cuda=<match>` meta package instead of pinning `cudatoolkit` when using PyTorch channel binaries.


## How to run
Interactive
```bash
python analysis/03_annotation/scANVI/job/scripts/run_scanvi.py
```
Example sbatch
```bash
#!/bin/bash
#SBATCH --job-name=scanvi
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --output=analysis/03_annotation/scANVI/job/logs/%x-%j.out

module purge
module load Mamba
source "$HOME/miniconda3/etc/profile.d/conda.sh" || eval "$(conda shell.bash hook)"
conda activate memory_rechallenge_v2_hpc

python analysis/03_annotation/scANVI/job/scripts/run_scanvi.py
```
Adjust partition, GPU resource, and memory according to your scheduler.


## The script at a glance
- Normalizes gene identifiers to symbols when available.
- Intersects genes between ref and qry, selects 2000 HVGs on counts with `seurat_v3` flavor.
- Builds `obs['celltype_scanvi']` from the reference labels and sets query to `Unknown`.
- Trains SCVI for 60 epochs then initializes SCANVI with `from_scvi_model` and trains for 20 epochs.
- Autoselects precision: `bf16-mixed` on Ampere or newer else `16-mixed`.
- Autotunes batch size by VRAM (80G, 32G, 16G tiers).
- Writes `scanvi_label_transfer.h5ad` with `X_scANVI`, `pred_label`, `pred_conf`.

Tunables in the script
- `n_top_genes` in HVGs: 1500 to 3000
- `n_latent` and `n_layers` in SCVI
- `n_samples_per_label` in SCANVI for rare classes
- `batch_size`, `precision`, `max_epochs`
- Learning rate via `plan_kwargs` (default 1e-3)


## Output structure
`scanvi_label_transfer.h5ad` is a standard AnnData with key fields:
- `obs['dataset']`: ref or qry
- `obs['pred_label']`: predicted label per cell in query. Low confidence cells can be re-marked by you as Unassigned based on thresholds.
- `obs['pred_conf']`: max posterior probability per cell
- `obsm['X_scANVI']`: latent embedding
- `layers['counts']`: raw counts used for modeling

Models on disk
- `outputs/model_scvi` and `outputs/model_scanvi` for reloading.


## Quick quality checks
Bar plot of counts per predicted label on the query:
```python
import scanpy as sc, pandas as pd
import matplotlib.pyplot as plt
adata = sc.read_h5ad("analysis/03_annotation/scANVI/job/outputs/scanvi_label_transfer.h5ad")
aq = adata[adata.obs["dataset"] == "qry"].copy()
vc = aq.obs["pred_label"].value_counts()
plt.figure(figsize=(9, 5))
vc.plot(kind="bar")
plt.ylabel("Number of cells"); plt.xlabel("predicted label"); plt.title("Query cell counts per label")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("analysis/03_annotation/scANVI/job/outputs/plots/qry_label_counts.png", dpi=200)
```
UMAP on scANVI embedding:
```python
sc.pp.neighbors(aq, use_rep="X_scANVI", n_neighbors=30)
sc.tl.umap(aq)
sc.pl.umap(aq, color=["pred_label"], frameon=False)
sc.pl.umap(aq, color=["pred_conf"], frameon=False)
```
Optional gating to avoid forced assignment:
```python
proba = m_scanvi.predict(soft=True, use_posterior_mean=True)
maxp = proba.max(1)
pred = proba.idxmax(1).astype(str)
pred[maxp < 0.75] = "Unassigned"  # adjust threshold to taste
adata.obs["pred_label"] = pred
adata.obs["pred_conf"] = maxp
```


## Troubleshooting
- `Trainer.__init__() got an unexpected keyword argument 'data_loader_kwargs'`
  - Do not pass `data_loader_kwargs` to `train`. Use `scvi.settings.dl_num_workers` and `dl_pin_memory` instead.
- `Trainer.__init__() got an unexpected keyword argument 'load_sparse_tensor'` or `DataLoader.__init__() got an unexpected keyword argument 'load_sparse_tensor'`
  - Do not pass `load_sparse_tensor` anywhere. scvi-tools handles sparsity internally.
- `author_cell_type not found in ref.obs`
  - Update `LABEL_COL_IN_REF` or add the column to the reference.
- Species mismatch or too few common genes
  - Map orthologs first or unify gene naming. At least 2k intersecting genes is recommended.
- AMP or bf16 messages on older GPUs
  - The script picks `16-mixed` automatically on pre-Ampere GPUs like P100.
- Dataloader worker warning
  - Increase `scvi.settings.dl_num_workers` to 7 or 8.
- Out of memory
  - Reduce `BATCH_SIZE` tiers or use `n_top_genes=1500`.


## Reproducibility
- Seed is fixed via `scvi.settings.seed = 0`.
- Archive the environment YAML. You can export a lockfile for exact versions:
```bash
mamba env export -n memory_rechallenge_v2_hpc > env_export_locked.yml
```


