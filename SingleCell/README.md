# Loading h5ad file into R Seurat object

sceasy uses reticulate and thus depends on python environment. Proved to be unstable and hard to use.
SeuratDisk also uses rhdf5, but uses h5-based Seurat format as an intermediate that looks like overcomplication. Additionally, SeuratDisk seems to be almost not supported and it fails even on examples from its own tutorial.
Despite all problems of both packages above they have clear advantage over schard: they allow not only to read h5ad into R but also to write it.

https://github.com/cellgeni/sceasy

https://github.com/cellgeni/schard

https://github.com/xleizi/easySCF

No to seuratdisk as it works with V3 assay and outdated. It also crashes on heavy datasets!
















# Suggested directory layout for a reproducible single‑cell analysis project
It’s designed to work whether you drive the pipeline with *Snakemake*, *Nextflow*, or a simple set of scripts—and lines up with the SemVer + Conda conventions

```
sc‑project/                           ← Git repo root (tagged vMAJOR.MINOR.PATCH)
├── README.md                         ← Quick‑start, data sources, citation
├── LICENSE
├── CHANGELOG.md                      ← Mirrors Git tags
├── .gitignore
│
├── envs/                             ← *Immutable* Conda env files
│   ├── sc‑pipeline‑v1.4.0.yml
│   └── sc‑pipeline‑v1.4.0.conda.lock
│
├── workflow/                         ← Executable pipeline logic
│   ├── Snakefile | main.nf
│   ├── modules/                      ← Re‑usable rules/processes
│   └── config/
│       ├── samples.tsv               ← Sample sheet (fastq paths, metadata)
│       └── params.yaml               ← Tunable pipeline parameters
│
├── data/                             ← **Read‑only, version‑controlled pointers** ➜ real data lives in `../data‑store/`
│   ├── raw/                          ← Fastqs, Cell Ranger outputs, etc.
│   │   ├── fastq/
│   │   └── cellranger_mkfastq/
│   ├── reference/                    ← Indexed genome, GTFs, feature barcodes
│   └── processed/                    ← Post‑QC count matrices (e.g. `.h5` from CellRanger)
│
├── output/                           ← All pipeline‑generated objects (ignored by Git)
│   ├── anndata/                      ← `.h5ad` per sample & combined
│   ├── seurat/                       ← `.rds`
│   ├── qc/                           ← doublet scores, metrics
│   └── loom/ |
│
├── analyses/                         ← **Human‑driven** exploration & downstream stats
│   ├── notebooks/
│   │   └── 01_qc_visualize.ipynb
│   └── scripts/
│       └── export_marker_genes.R
│
├── results/                          ← Final, publication‑ready artefacts
│   ├── figures/                      ← `.svg` or `.pdf`
│   ├── tables/                       ← `.tsv`, `.xlsx`
│   └── reports/                      ← MultiQC, HTML pipelines, manuscripts
│
├── docker/ | containers/             ← Docker/Singularity build context (optional)
│   └── Dockerfile
│
└── tests/                            ← Unit tests & minimal datasets
    └── test_pipeline.py
```

### What lives where — and why

| Folder        | Purpose & best practices                                                                                                         |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **envs/**     | One *version‑named* `.yml` (and optional lock file) per Git tag; never edit in place—create a new file when dependencies change. |
| **workflow/** | All machine‑executable steps. Commit every change; tag releases exactly after this folder is frozen.                             |
| **data/**     | Symbolic links or DVC references keep *raw* data out of Git history while letting the pipeline find them.                        |
| **output/**   | Auto‑generated files go here; a single `.gitignore` entry keeps the repo clean.                                                  |
| **analyses/** | Interactive work: notebooks, ad‑hoc plots, statistical tests. Version control these so you can cite them.                        |
| **results/**  | Only polished deliverables—figures, Supplementary Tables, final HTML reports. These are what you share with collaborators.       |
| **docker/**   | Ensures cloud / HPC runs use the *identical* software stack as local dev. Tag images with the same SemVer string.                |
| **tests/**    | Tiny toy dataset (10–100 cells) keeps CI fast; assert pipeline still runs after dependency bumps.                                |

### Release flow recap

1. **Freeze parameters ⟶** commit to `workflow/config/`.
2. **Export Conda env ⟶** add new `envs/sc‑pipeline‑vX.Y.Z.yml`.
3. **Run the pipeline end‑to‑end** on canonical data; stash outputs in `output/`.
4. **Update CHANGELOG.md**.
5. `git tag -a vX.Y.Z -m "Release vX.Y.Z – …"; git push --follow-tags`.
6. **CI job** builds container, re‑executes pipeline, and uploads `output/` artefacts + env tarball (`conda‑pack`) to the GitHub Release page.

Stick to this structure and Future‑You (and every collaborator, reviewer, or lab mate) will always know **exactly** where code, data, environments, and results live—and which version produced which figure.











