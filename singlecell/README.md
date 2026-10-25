# Updated Layout — Nextflow-First, Modular & Reproducible Research

> **Goal:** Build a modular, flexible, testable, and reproducible bioinformatics workflow system powered by **Nextflow DSL2**, following **nf-core conventions**.
>
> The architecture should support Python, R, HPC/SLURM, interactive Jupyter exploration, multiple analysis strategies, and controlled AI-assisted development.
>
> **Core principle:** Every scientific result must be traceable to its exact inputs, code version, parameters, software environment, and execution history.

## 1. Proposed Project Structure

```text
sc-project/
│
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── AGENTS.md
│
├── main.nf
├── nextflow.config
├── nextflow_schema.json
│
├── conf/
│   ├── local.config
│   ├── cheaha.config
│   └── resources.config
│
├── workflows/
│   ├── scrnaseq.nf
│   ├── spatial.nf
│   └── multiomics.nf
│
├── subworkflows/
│   └── local/
│       ├── preprocessing/
│       ├── dimensionality_reduction/
│       ├── clustering/
│       └── annotation/
│
├── modules/
│   ├── local/
│   │   ├── scanpy_qc/
│   │   ├── scanpy_pca/
│   │   ├── scanpy_leiden/
│   │   ├── ambient_removal/
│   │   └── r_differential_expression/
│   └── nf-core/
│
├── bin/
│   ├── qc.py
│   ├── pca.py
│   ├── clustering.py
│   └── differential_expression.R
│
├── params/
│   ├── approved/
│   │   └── control.yaml
│   └── experiments/
│       ├── gene_removal.yaml
│       └── alternative_clustering.yaml
│
├── containers/
│   ├── definitions/
│   └── image-locks.yaml
│
├── envs/
│   ├── python.yml
│   └── renv.lock
│
├── assets/
│   └── samplesheet.csv
│
├── data/
│   └── manifests/
│
├── tests/
│   ├── modules/
│   ├── subworkflows/
│   ├── regression/
│   └── fixtures/
│
├── notebooks/
│   ├── exploration/
│   └── visualization/
│
├── results/
│   └── <run_id>/
│       ├── outputs/
│       ├── reports/
│       └── provenance/
│
└── docs/
    ├── analysis_contracts.md
    ├── reproducibility.md
    └── module_development.md
```

*This is the target architecture, not a representation of files already implemented. Start with the single-cell workflow and extend the structure as needed.*

## 2. Architecture Principles

### A. Modular and Dynamic Workflows

- Use **Nextflow DSL2** as the primary workflow orchestration engine.
- Follow nf-core conventions for modules, subworkflows, testing, and documentation.
- Separate individual computational processes from complete analysis workflows.
- Support optional processing steps, alternative algorithms, and configurable execution paths.
- Reuse modules across single-cell, spatial, imaging, and multi-omics analyses.
- Allow scientific parameters and predefined workflow branches to be selected through configuration files.
- Treat changes to workflow topology as version-controlled code changes requiring validation.
- Define explicit input/output contracts for every module, including data format, required metadata, and expected state of the data.

### B. Scientific Parameter Control

- Separate **scientific parameters** from **computational resource settings**.
- Maintain approved baseline configurations under `params/approved/`.
- Keep experimental configurations under `params/experiments/`.
- Never modify approved scientific configurations without explicit review.
- Record random seeds, thread settings, algorithm versions, and all parameters affecting scientific results.
- Validate parameters using `nf-schema` or equivalent schema validation.
- Ensure every parameter and file affecting a computation is represented in its tracked dependencies.

**Important:** Changing computational resources must not silently change algorithm behavior. CPU allocation and algorithm-level parallelism should be explicitly controlled.

### C. Reproducibility and Provenance

Every official analysis run should record:

- Git commit and pipeline release version.
- Complete effective scientific configuration.
- Input data identities and checksums.
- Reference genome, annotations, and reference dataset versions.
- Container image digests and software versions.
- Random seeds and relevant parallel execution settings.
- Nextflow execution metadata, task logs, and trace reports.
- Output artifact identities and provenance.

Use versioned or uniquely identified output directories to prevent accidental overwriting.

**Nextflow caching and `-resume` are execution optimizations, not independent guarantees of scientific reproducibility.**

### D. Environment and Language Independence

- Support Python, R, Bash, and other scientific tools as independent Nextflow processes.
- Prefer pinned Apptainer-compatible containers for production execution on HPC.
- Maintain Conda and renv environments for development and container construction when appropriate.
- Avoid unnecessary Python/R environment coupling through reticulate in production pipelines.
- Exchange data through documented, validated file formats.
- Record container digests or verified image checksums rather than relying exclusively on mutable version tags.

### E. Testing and Scientific Validation

Implement multiple testing layers:

1. **Module tests:** Validate individual Nextflow processes using `nf-test`.
2. **Workflow tests:** Verify expected connections, outputs, and execution behavior.
3. **Scientific regression tests:** Compare approved baseline results against new runs.
4. **Integration tests:** Verify Python/R interoperability, containers, and execution profiles.
5. **CI checks:** Automatically run appropriate tests before accepting changes.

Tests should verify both computational correctness and scientific expectations.

Reference test data and expected results must not be silently updated together with the implementation being tested.

### F. Controlled AI-Assisted Development

Codex, Claude Code, and other AI agents may assist with code development, debugging, and documentation, but must not independently approve scientific changes.

Development policy:

- Run AI agents in dedicated Git branches or worktrees.
- Restrict write access to approved configurations, reference data, and protected code.
- Review all proposed changes using Git diffs.
- Require explicit approval for changes to scientific parameters, algorithms, or analysis logic.
- Run automated tests before merging changes.
- Protect the main branch using required checks and review policies.
- Keep AI assistance outside the execution path of approved scientific analyses whenever possible.

`AGENTS.md` documents expected agent behavior but is not a security boundary. Technical access restrictions and independent validation are also required.

### G. Interactive Exploration

Maintain **JupyterLab and RStudio** as interactive exploration and visualization environments.

Recommended workflow:

**Explore → Develop → Validate → Approve → Execute → Inspect**

- Use notebooks for exploratory analysis, visualization, and hypothesis testing.
- Convert validated computational steps into reusable Python/R scripts and Nextflow modules.
- Execute approved analyses through versioned Nextflow workflows.
- Reopen intermediate and final outputs interactively without modifying approved artifacts.
- Promote experimental analyses to approved workflows only after review and testing.

### H. HPC Execution and Monitoring

- Use SLURM as the Nextflow executor on Cheaha.
- Use Apptainer for reproducible process environments.
- Define CPU, memory, and time requirements for individual processes.
- Maintain separate local development and HPC execution profiles.
- Use Nextflow reports, traces, timelines, and DAG visualization for monitoring.
- Optionally integrate Seqera Platform for centralized execution monitoring and parameter management.
- Follow cluster policies for interactive sessions, compute jobs, storage, and container execution.

## 3. Versioning and Release Strategy

Keep three distinct levels of change:

| Level | Example | Required action |
|---|---|---|
| Experimental | Different Leiden resolution or gene filtering | New experiment configuration and run |
| Scientific | New normalization or clustering method | Code review, scientific tests, and versioned workflow change |
| Infrastructure | New container, resource profile, or executor | Compatibility checks and documented environment change |

An approved release should link the exact source code, validated configurations, container identities, test results, and analysis provenance.

A successful pipeline execution alone does not constitute scientific validation.

## 4. Implementation Strategy

**Phase 1 — Foundation**

Set up Nextflow DSL2, nf-core conventions, Git protections, containers, parameter schemas, and testing infrastructure.

**Phase 2 — Reference Single-Cell Workflow**

Implement QC, preprocessing, PCA, neighborhood construction, and clustering. Reproduce an approved baseline before introducing experimental changes.

**Phase 3 — Dynamic Analysis**

Introduce optional ambient RNA correction, gene filtering, alternative clustering algorithms, Python/R integration, and validated branching strategies.

**Phase 4 — Interactive and HPC Integration**

Integrate JupyterLab, Cheaha/SLURM, execution reports, visualization, and experiment comparison.

**Phase 5 — Multi-Omics Expansion**

Extend the same architectural principles to spatial transcriptomics, imaging, multimodal omics, sequencing, and structural biology through independently versioned workflows and reusable modules.

---

## Relationship to the Original Layout

The original project layout below remains useful as an initial organizational reference.

This updated architecture extends it with:

- Nextflow-first execution and nf-core standards.
- Formal scientific configuration management.
- Modular and testable workflow design.
- Independent Python/R execution environments.
- AI-assisted development safeguards.
- Automated scientific regression testing.
- Reproducibility, provenance, and controlled releases.
- Interactive notebook exploration alongside production HPC workflows.

**Long-term objective:** A flexible research workflow system in which every analysis step can be inspected, tested, modified, independently executed when valid, and reliably traced back to its original inputs and scientific configuration.

---



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



# Wrappers 
### wrapper to run SCTransform for anndata

https://github.com/normjam/benchmark/blob/master/normbench/methods/ad2seurat.py

I have found this link in response to this [issue](https://github.com/scverse/scanpy/issues/1068).
