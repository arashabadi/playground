# Loading h5ad file into R Seurat object

sceasy uses reticulate and thus depends on python environment. Proved to be unstable and hard to use.
SeuratDisk also uses rhdf5, but uses h5-based Seurat format as an intermediate that looks like overcomplication. Additionally, SeuratDisk seems to be almost not supported and it fails even on examples from its own tutorial.
Despite all problems of both packages above they have clear advantage over schard: they allow not only to read h5ad into R but also to write it.

https://github.com/cellgeni/sceasy

https://github.com/cellgeni/schard

https://github.com/xleizi/easySCF

No to seuratdisk as it works with V3 assay and outdated. It also crashes on heavy datasets!

# Version‑tagging a single‑cell analysis project with SemVer (and slight tweaks)

Below is a lightweight **release playbook**—written for a computational‑biology codebase or pipeline that ingests raw single‑cell data, produces processed objects (e.g., `.h5ad`/`.rds`), and generates figures or downstream resources. Adjust the specifics to match your stack (Scanpy, Seurat, Nextflow, Snakemake, etc.).

---

## 1. Version‑string format

```
vMAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

| Component      | When you bump it                                                                                                                                                             | Example for single‑cell work |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| **MAJOR**      | Breaking changes in input/output contracts – e.g. switching the default reference genome, altering AnnData slot names, renaming pipeline parameters.                         | 2.0.0                        |
| **MINOR**      | Backward‑compatible feature additions – e.g. adding doublet filtering module, supporting CITE‑seq alongside RNA.                                                             | 1.3.0                        |
| **PATCH**      | Pure bug fixes or tiny, non‑breaking tweaks – e.g. fixing a gene‑name case bug, bumping a dependency without changing results.                                               | 1.3.2                        |
| **PRERELEASE** | Unstable preview (`-alpha`, `-beta.2`, `-rc.1`). CI can publish Docker images like `myproj:1.4.0-rc.1`.                                                                      |                              |
| **BUILD**      | Optional build metadata (`+nlp1`, `+20250611`). Ignored by SemVer precedence rules; handy if you must embed run date, dataset ID, or commit hash in the artifact’s filename. |                              |

---

## 2. Recommended Git tag convention

* **Prefix with `v`** (`v1.4.0`, not just `1.4.0`) – many tooling ecosystems expect it.
* **Always create an *annotated* tag**, never a lightweight one:

```bash
git tag -a v1.4.0 -m "Release v1.4.0 – add CITE‑seq support, bump Scanpy 1.11"
git push origin v1.4.0
```

---

## 3. Map versions to your project pieces

| Artifact                                                | Versioning strategy                                                                                                 |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Pipeline code / scripts**                             | Tag with SemVer exactly as above.                                                                                   |
| **Frozen reference files** (gene annotations, barcodes) | Keep in `assets/` and bump **MINOR** when you update them without breaking downstream; **MAJOR** if formats change. |
| **Processed datasets**                                  | Embed both pipeline tag *and* dataset release date in the file (e.g. `pbmc10k_v1.2.1_2025‑06‑11.h5ad`).             |
| **Docker/Singularity image**                            | Same tag as the pipeline (`ghcr.io/...:v1.2.1`).                                                                    |
| **Figures/manuscript panels**                           | Put a small caption or legend note like “generated with pipeline v1.2.1”.                                           |

---

## 4. Release checklist (single‑cell edition)

1. **Freeze parameters**
   Commit the exact `config.yaml` or `params.json` used for the release; bump in code if defaults changed.
2. **Update `__version__` / `VERSION` file**
   Keep one source of truth inside the repo; unit tests can assert the tag matches.
3. **Run pipeline end‑to‑end**
   Verify reproducibility on canonical dataset(s).
4. **Generate/refresh CHANGELOG.md**
   Use a template: “Added”, “Changed”, “Fixed”, “Breaking”.
5. **Tag & push**

   ```bash
   git tag -a v1.4.0 -m "Release v1.4.0"
   git push origin main --follow-tags
   ```
6. **Publish on GitHub/GitLab**
   GitHub Releases can attach `.h5ad` or Docker digest; CI/CD can auto‑publish on `push: tags: ["v*"]`.
7. **Archive in Zenodo (optional)**
   Zenodo‑GitHub integration will mint a DOI for each tag beginning with `v`.

---

## 5. Handling inevitable mistakes

| Scenario                                | Remedy                                                                      |
| --------------------------------------- | --------------------------------------------------------------------------- |
| Tagged wrong commit                     | `git tag -d v1.4.0 && git push origin :refs/tags/v1.4.0` → retag correctly. |
| Forgot to bump in‑code version constant | Patch release: commit bump, tag `v1.4.1`.                                   |
| Need to hot‑fix an old major line       | Create maintenance branch `release/1.x`, cherry‑pick fix, tag `v1.5.3`.     |

---

## 6. Beyond classical SemVer

If your project’s *datasets* evolve independently of *code*, you can use **double versioning**:

```
PIPE_VER-DATA_VER
e.g. v2.1.0-d20250611
```

Or follow **CalVer** (calendar versioning) for data: `2025.06.11`.

---

### TL;DR

1. Stick to **vMAJOR.MINOR.PATCH** annotated Git tags for the pipeline.
2. Bump MAJOR = breaking, MINOR = new features, PATCH = bug fixes.
3. Embed the tag in every downstream artifact (HDF5, Docker, figures).
4. Automate the release through CI to guarantee reproducibility.

With this scheme, collaborators (and Future‑You) can always trace any figure or result back to the exact commit, parameters, and reference resources used. Happy versioning!

