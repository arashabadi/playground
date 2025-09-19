#!/usr/bin/env python3
"""
scANVI label transfer (scvi-tools >=1.3.x, Lightning 2.x, PyTorch 2.x)
- Reference labels from ref.obs['author_cell_type']
- Query unlabeled -> "Unknown"
- HVGs on counts
- SCVI pretrain -> SCANVI fine-tune
- No load_sparse_tensor anywhere (avoids DataLoader kwarg errors)
- Batch size auto-tuned for GPU VRAM; P100 gets smaller batches
"""

from pathlib import Path
import gc
import numpy as np
import pandas as pd
import scanpy as sc
import scvi
import anndata as ad
from scipy import sparse as sp
import torch

# ---------- paths ----------
DATA_DIR = Path("/home/BLAZERID/github/repo/data")
JOB_DIR  = Path("/home/BLAZERID/github/repo/analysis/03_annotation/scANVI/job")
OUT_DIR  = JOB_DIR / "outputs"
LOG_DIR  = JOB_DIR / "logs"

QRY_PATH = DATA_DIR / "c2_adata_raw_qc_doublet.h5ad"
REF_PATH = DATA_DIR / "anndata_ref.h5ad"

OUT_H5AD   = OUT_DIR / "scanvi_label_transfer.h5ad"
SCVI_DIR   = OUT_DIR / "model_scvi"
SCANVI_DIR = OUT_DIR / "model_scanvi"

LABEL_COL_IN_REF = "author_cell_type"
UNLABELED_TOKEN  = "Unknown"

# ---------- setup ----------
OUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
SCVI_DIR.mkdir(parents=True, exist_ok=True)
SCANVI_DIR.mkdir(parents=True, exist_ok=True)

sc.settings.verbosity = 3
sc.set_figure_params(dpi=100, facecolor="white")
scvi.settings.seed = 0

# Global dataloader hints only (let scvi handle wiring)
scvi.settings.dl_num_workers = 8
scvi.settings.dl_pin_memory = True

# Optional matmul perf tweak
try:
    torch.set_float32_matmul_precision("high")
except Exception:
    pass

print("torch:", torch.__version__)
print("cuda build:", torch.version.cuda)
print("cuda available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
print("scvi-tools:", scvi.__version__)
print("scanpy:", sc.__version__)

# Precision: bfloat16 only on Ampere+; otherwise use 16-mixed
def pick_precision():
    if not torch.cuda.is_available():
        return "32-true"
    major, minor = torch.cuda.get_device_capability(0)
    if major >= 8:  # Ampere or newer
        try:
            if torch.cuda.is_bf16_supported():  # PyTorch check
                return "bf16-mixed"
        except Exception:
            pass
    return "16-mixed"

precision_arg = pick_precision()
print("Selected precision:", precision_arg)

# Batch size by VRAM
def pick_batch_size(default_bs=4096):
    if not torch.cuda.is_available():
        return 512
    props = torch.cuda.get_device_properties(0)
    vram = getattr(props, "total_memory", 0)
    if vram >= 70 * 2**30:
        return default_bs        # 80G
    if vram >= 31 * 2**30:
        return 2048              # 32G
    if vram >= 15 * 2**30:
        return 1024              # 16G (P100)
    return 512

BATCH_SIZE = pick_batch_size()
print("Selected batch_size:", BATCH_SIZE)

print("DATA_DIR:", DATA_DIR)
print("JOB_DIR:", JOB_DIR)
print("OUT_DIR:", OUT_DIR)
print("QRY exists:", QRY_PATH.exists(), "REF exists:", REF_PATH.exists(), flush=True)

# ---------- load ----------
qry = sc.read_h5ad(QRY_PATH)
ref = sc.read_h5ad(REF_PATH)
print("Loaded qry:", qry.shape, "layers:", list(qry.layers.keys()))
print("Loaded ref:", ref.shape, "layers:", list(ref.layers.keys()), "has .raw:", ref.raw is not None, flush=True)

# ---------- counts layers ----------
assert "counts" in qry.layers, "Query must have raw counts in .layers['counts']"
if ref.raw is None:
    raise ValueError("Reference must carry raw counts in ref.raw.X")

ref = ref[:, ref.raw.var_names].copy()
Xraw = ref.raw.X
ref.layers["counts"] = Xraw.tocsr().astype(np.float32) if sp.issparse(Xraw) else np.asarray(Xraw, dtype=np.float32)

qry.layers["counts"] = (
    qry.layers["counts"].tocsr().astype(np.float32)
    if sp.issparse(qry.layers["counts"])
    else np.asarray(qry.layers["counts"], dtype=np.float32)
)

# ---------- normalize gene ids to symbols if available ----------
def ensure_symbols_from_column(adata: ad.AnnData, col: str) -> ad.AnnData:
    if col not in adata.var.columns:
        return adata
    sym = adata.var[col].astype(str)
    keep = sym.notna() & (sym != "")
    adata = adata[:, keep].copy()
    adata.var[col] = sym[keep].values
    adata.var_names = adata.var[col].values
    adata.var_names_make_unique()
    return adata

if "symbol" in ref.var.columns:
    ref = ensure_symbols_from_column(ref, "symbol")
elif "gene_name" in ref.var.columns:
    ref = ensure_symbols_from_column(ref, "gene_name")

if "symbol" in qry.var.columns:
    qry = ensure_symbols_from_column(qry, "symbol")
elif "gene_name" in qry.var.columns:
    qry = ensure_symbols_from_column(qry, "gene_name")
else:
    qry.var_names_make_unique()

# ---------- prune zero-count genes in ref (optional) ----------
if sp.issparse(ref.layers["counts"]):
    nz_cols = np.unique(ref.layers["counts"].indices)
    if len(nz_cols) < ref.n_vars:
        ref = ref[:, ref.var_names[nz_cols]].copy()
        print("Pruned zero-count genes in ref. New shape:", ref.shape, flush=True)

# ---------- gene intersection ----------
common = ref.var_names.intersection(qry.var_names)
print("Common genes after harmonization:", len(common), flush=True)
if len(common) < 2000:
    raise ValueError("Too few common genes after harmonization. Check gene IDs or species mapping.")

ref = ref[:, common].copy()
qry = qry[:, common].copy()

# ---------- build labels on ref; Unknown on qry ----------
if LABEL_COL_IN_REF not in ref.obs.columns:
    raise KeyError(f"{LABEL_COL_IN_REF} not in ref.obs. Available: {list(ref.obs.columns)[:30]}")

tmp_label_col = "__label_from_ref"
ref.obs[tmp_label_col] = ref.obs[LABEL_COL_IN_REF].astype(str)
qry.obs[tmp_label_col] = pd.Series(index=qry.obs_names, data=np.nan, dtype="object")

# ---------- concat and HVGs ----------
adata = ad.concat([ref, qry], join="inner", label="dataset", keys=["ref", "qry"])
print("Concatenated:", adata.shape, flush=True)

sc.pp.highly_variable_genes(
    adata,
    flavor="seurat_v3",
    n_top_genes=2000,
    layer="counts",
    batch_key="dataset",
    subset=True,
)
print("After HVG selection:", adata.shape, flush=True)

# final label key
label_key = "celltype_scanvi"
adata.obs[label_key] = adata.obs[tmp_label_col].astype("object").fillna(UNLABELED_TOKEN).astype(str)
adata.obs[label_key] = adata.obs[label_key].astype("category")
del adata.obs[tmp_label_col]

# ---------- SCVI pretrain ----------
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="dataset",
    labels_key=label_key,
)
m_scvi = scvi.model.SCVI(adata, n_layers=2, n_latent=30)
m_scvi.train(
    max_epochs=60,
    batch_size=BATCH_SIZE,
    accelerator="gpu",
    devices=1,
    precision=precision_arg,
    plan_kwargs={"lr": 1e-3},
)
m_scvi.save(str(SCVI_DIR), overwrite=True)
print("Saved SCVI model to", SCVI_DIR, flush=True)

# ---------- SCANVI fine-tune ----------
m_scanvi = scvi.model.SCANVI.from_scvi_model(
    m_scvi,
    unlabeled_category=UNLABELED_TOKEN,
    labels_key=label_key,
    adata=adata,
)
m_scanvi.train(
    max_epochs=20,
    n_samples_per_label=100,
    batch_size=BATCH_SIZE,
    accelerator="gpu",
    devices=1,
    precision=precision_arg,
)
m_scanvi.save(str(SCANVI_DIR), overwrite=True)
print("Saved SCANVI model to", SCANVI_DIR, flush=True)

# ---------- outputs ----------
adata.obsm["X_scANVI"] = m_scanvi.get_latent_representation()
proba = m_scanvi.predict(soft=True, use_posterior_mean=True)
adata.obs["pred_conf"] = proba.max(1)
adata.obs["pred_label"] = proba.idxmax(1).astype(str)

low = adata.obs["pred_conf"] < 0.8
adata.obs.loc[low, "pred_label"] = "LowConf"

adata.write_h5ad(str(OUT_H5AD), compression="gzip")
print("Wrote:", OUT_H5AD.resolve(), flush=True)

for p in OUT_DIR.iterdir():
    try:
        print("Output:", p.name, p.stat().st_size, "bytes", flush=True)
    except Exception:
        pass

del qry, ref
gc.collect()
print("DONE.", flush=True)