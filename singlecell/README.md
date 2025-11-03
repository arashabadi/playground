
# Suggested layout for a reproducible single-cell analysis project

Designed to work with *Snakemake*, *Nextflow*, or simple scripts.
Environment strategy:

* Python + scverse in **conda** (`.yml`)
* R + Seurat in **renv** (`renv.lock`)
* Connected via **reticulate** (if needed to be inside one ipynb)

```
sc-project/                           ← Git repo root (tagged vMAJOR.MINOR.PATCH)
├── README.md                         ← Quick-start, data sources, citation
├── LICENSE
├── CHANGELOG.md                      ← Mirrors Git tags
├── .gitignore
│
├── envs/                             
│   ├── sc-pipeline-v1.4.0.yml    # conda env for Python + scverse
│   ├── renv.lock                 # R lockfile from renv
│   └── Brewfile                  # optional: macOS system deps (BLAS, hdf5…)
│
├── workflow/                         ← Executable pipeline logic
│   ├── Snakefile | main.nf
│   ├── modules/                      ← Re-usable rules/processes
│   └── config/
│       ├── samples.tsv               ← Sample sheet (fastq paths, metadata)
│       └── params.yaml               ← Tunable pipeline parameters
│
├── data/                             ← **Read-only, version-controlled pointers** ➜ real data lives in `../data-store/`
│   ├── raw/                          ← Fastqs, Cell Ranger outputs, etc.
│   ├── reference/                    ← Indexed genome, GTFs, feature barcodes
│   └── processed/                    ← Post-QC count matrices (e.g. `.h5` from CellRanger)
│
├── output/                           ← All pipeline-generated objects (ignored by Git)
│   ├── anndata/                      ← `.h5ad` per sample & combined
│   ├── seurat/                       ← `.rds`
│   ├── qc/                           ← doublet scores, metrics
│   └── loom/
│
├── analyses/                         ← **Human-driven** exploration & downstream stats
│   ├── notebooks/
│   │   └── 01_qc_visualize.ipynb
│   └── scripts/
│       └── export_marker_genes.R
│
├── results/                          ← Final, publication-ready artefacts
│   ├── figures/                      ← `.svg` or `.pdf`
│   ├── tables/                       ← `.tsv`, `.xlsx`
│   └── reports/                      ← MultiQC, HTML pipelines, manuscripts
│
├── containers/                       ← Docker/Singularity build context (optional)
│   └── Dockerfile
│
└── tests/                            ← Unit tests & minimal datasets
    └── test_pipeline.py
```

---

### What lives where — and why

| Folder          | Purpose & best practices                                                                                                                                                                            |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **envs/**       | Keep environment manifests here: `sc-pipeline-vX.Y.Z.yml` for Python (conda), `renv.lock` for R, and optional `Brewfile` for mac system deps. Never edit in place—make a new file per version bump. |
| **workflow/**   | All machine-executable steps. Commit every change; tag releases exactly after this folder is frozen.                                                                                                |
| **data/**       | Use symbolic links or DVC references; keeps *raw* data out of Git while letting pipelines resolve paths.                                                                                            |
| **output/**     | Auto-generated files. Git-ignored so the repo stays clean.                                                                                                                                          |
| **analyses/**   | Human-driven exploration: notebooks, ad-hoc plots, statistical tests. Keep version-controlled to cite exact exploratory work.                                                                       |
| **results/**    | Only polished deliverables—figures, Supplementary Tables, HTML reports. These are what you actually ship to collaborators.                                                                          |
| **containers/** | (Optional) Ensure cloud/HPC runs mirror your dev software stack. Tag images with the same SemVer string.                                                                                            |
| **tests/**      | Tiny toy dataset (10–100 cells) + simple assertions; keeps CI fast and ensures pipeline works after dependency bumps.                                                                               |

---

### Why Conda for Python, renv for R

* **Python fits conda well**: conda-forge has mature, stable builds for scverse (scanpy, anndata, scvelo, squidpy).
* **R does not fit conda well**:

  * Bioconductor packages often fail in conda yaml installation(especially on macOS ARM and Windows).
  * Updates lag behind CRAN/Bioconductor, breaking reproducibility.
  * Toolchain conflicts (BLAS, compilers) cause fragile builds and slower performance.
* **renv is designed for R**: lockfiles are portable, reproducible, and work with system R or HPC modules.
* **Clean separation**: Python deps locked in `environment.yml`, R deps in `renv.lock`. Reticulate bridges them without mixing ecosystems.
* **Portability**: on HPC you can use system R modules + renv, while reusing the same conda env for Python. No clashes.

---

### Release flow recap

1. **Freeze parameters ⟶** commit to `workflow/config/`.
2. **Export environments:**

   * Python: `micromamba env export -n scverse > envs/sc-pipeline-vX.Y.Z.yml`
   * R: `renv::snapshot()` → updates `envs/renv.lock`
3. **Run the pipeline end-to-end** on canonical data; stash outputs in `output/`.
4. **Update CHANGELOG.md**.
5. `git tag -a vX.Y.Z -m "Release vX.Y.Z – …"; git push --follow-tags`.
6. **CI job** builds container, re-executes pipeline, and uploads `output/` artefacts + environment manifests to the GitHub Release page.

---

This structure guarantees:

* Clear separation of Python and R environments.
* No dependency fights between conda and Bioconductor.
* Easy portability between macOS and HPC.
* Explicit mapping from repo version → software env → figures and results.


 

# Loading h5ad file into R Seurat object

sceasy uses reticulate and thus depends on python environment. Proved to be unstable and hard to use.
SeuratDisk also uses rhdf5, but uses h5-based Seurat format as an intermediate that looks like overcomplication. Additionally, SeuratDisk seems to be almost not supported and it fails even on examples from its own tutorial.
Despite all problems of both packages above they have clear advantage over schard: they allow not only to read h5ad into R but also to write it.

https://github.com/cellgeni/sceasy

https://github.com/cellgeni/schard

https://github.com/xleizi/easySCF

No to seuratdisk as it works with V3 assay and outdated. It also crashes on heavy datasets!


Also:
https://github.com/theislab/anndata2ri

Also:
https://github.com/theislab/zellkonverter

# Wrappers 
### wrapper to run SCTransform for anndata

https://github.com/normjam/benchmark/blob/master/normbench/methods/ad2seurat.py

I have found this link in response to this [issue](https://github.com/scverse/scanpy/issues/1068).