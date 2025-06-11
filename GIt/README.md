# Here are some notes and resources I found to master Git and GitHub:

- [How We Encode Code Reviews at Netlify](https://www.netlify.com/blog/2020/03/05/feedback-ladders-how-we-encode-code-reviews-at-netlify/)

_Good insights on how to contribute effectively and issues categorization tutorial_
--------------------------------

# I am trying to make GitHub actions work with my Patoq book
1. first I made a new branch using:

```bash
   # Create and switch to a new backup branch
   git checkout -b backup-before-actions
   
   # Push this branch to GitHub
   git push -u origin backup-before-actions 
```
The backup branch should be an exact copy of your main branch before we add the GitHub Actions. The GitHub Actions workflow should only be in the main branch
This way, if something goes wrong, you can easily revert to the pre-Actions state

2. where are we?
```bash
cd ./patoq && git status | cat
```
we have to switch to the main branch:
```bash
git checkout main
```
now we can add the newly made ".github\workflows\render-book.yml" GitHub Actions workflow to the main branch:
```bash
git add .github/ && git commit -m "Add GitHub Actions workflow for Quarto rendering"
```

let's push the changes to github:

```bash
git push -u origin main
```

3. GitHub> Settings> Actions> General> Workflow permissions> Read and write permissions
4. GitHub> Setting > pages > Source > Branch: gh-pages / root: /(root)


--------------------------------


# I had some faluires with the GitHub Actions workflow, so I had to revert to some specific commit.

there are two ways to do this:
1. making a new revert-to-commit branch and pull request to main on github. didn't worked for me. 

2. forced push to main branch:

Temporarily disable protection (Admin access required)
Go to your repository on GitHub:
https://github.com/arashabadi/patoq/settings/branches

Under "Branch protection rules", find the rule for main.

Click "Edit", check "Allow force pushes", and save.
Then run the following commands:

```bash
git checkout main
git log --oneline | head -n 5
git reset --hard HEAD~2 # HEAD~2 is two commits before the last commit (or I can use the commit hash)
git push origin main --force
```



















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

## 7. Versioning your **conda** environment files

When a single‑cell pipeline depends on a curated Conda environment, treat the *.yml* file as a **first‑class release artifact** and version it in lock‑step with the code.

| Goal                         | Recommended practice                                                                                                                                                                                                          |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Human‑readable file name** | `envs/sc‑pipeline‑v1.4.0.yml` – mirror the Git tag (`v1.4.0`).                                                                                                                                                                |
| **Self‑identifying YAML**    | Inside the file set `name: sc‑pipeline‑v1.4.0` so `conda env create` produces an environment whose `conda env list` entry already tells you its lineage.                                                                      |
| **Exact package set**        | Pin every dependency (`scanpy=1.11.0`, `python=3.11.*`) or, for complete reproducibility, export with `conda list --explicit > env‑v1.4.0.txt` or generate a lock‑file via **conda‑lock**. Commit these alongside the *.yml*. |
| **Git storage layout**       | Keep an immutable copy under `envs/`:<br/>`repo root/ <br/>├── envs/ <br/>│   ├── sc-pipeline-v1.3.2.yml <br/>│   └── sc-pipeline-v1.4.0.yml <br/>└── ...`                                                                    |
| **Tagging & CI**             | In your release workflow, after bumping `envs/sc‑pipeline‑vX.Y.Z.yml`, tag the commit as usual (`git tag -a vX.Y.Z …`). Your CI job can then do:<br/>`bash<br/>mamba env create -f envs/sc-pipeline-v${{TAG_NAME}}.yml<br/>`  |
| **User docs**                | Tell users: “For version *v1.4.0*, run<br/>`bash<br/>mamba env create -f envs/sc-pipeline-v1.4.0.yml<br/>conda activate sc-pipeline-v1.4.0<br/>`”.                                                                            |

### Quick recipe for a new release

```bash
# 1. Update dependencies
conda env export --from-history | \
  sed '/prefix:/d' > envs/sc-pipeline-v1.5.0.yml     # remove machine‑specific prefix

# 2. Bump the name field inside the YAML
#    name: sc-pipeline-v1.5.0

# 3. Commit & tag
git add envs/sc-pipeline-v1.5.0.yml
git commit -m "Add Conda env for v1.5.0"
git tag -a v1.5.0 -m "Release v1.5.0 – new env"
git push origin main --follow-tags
```

### Pro tips

* **conda‑lock** generates platform‑specific lock files (`*.conda.lock`) that pin exact build strings; include them for bit‑for‑bit reproducibility on CI/cloud.
* If your environment changes between **PATCH** releases only for bug‑fix versions of packages, you can keep the YAML name stable (`sc‑pipeline‑1.4.x`) and just regenerate `conda.lock` on each patch tag.
* To ship a self‑contained tarball, run `conda‑pack -n sc-pipeline-v1.4.0 -o sc_pipeline_v1.4.0.tar.gz` in CI and attach it to the GitHub Release.

With these conventions, anyone can reconstruct the **exact** software stack that produced a given single‑cell result—even years later—by simply checking out tag *vX.Y.Z* and creating the accompanying Conda environment.















# Tags vs Branches for “backup” snapshots

| Purpose    | What it is                                                                                 | When strong teams use it                                                                                                                          |
| ---------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tag**    | An immutable pointer to a single commit.<br>Has metadata (author, date, message, GPG sig). | Version numbers (`v1.4.0`), publication checkpoints (“paper‑revision‑submitted”), dataset freezes.                                                |
| **Branch** | A *moving* pointer that can accept new commits.                                            | ‑ **Long‑lived**: `main`, `develop`, `release/1.x` for maintenance.<br>‑ **Short‑lived**: feature or bug‑fix branches that disappear after merge. |

> **Rule of thumb:**
> *Use a tag when you just need a bookmark; use a branch only if further work will continue on top of that snapshot.*

---

## Common “backup” patterns that stay tidy

| Pattern                                  | How it works                                                                                                                                                | Pros                                                                               | Cons                                                                           |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Annotated tag + pushed to origin**     | `git tag -a backup‑2025‑06‑11 -m "Pre‑refactor snapshot"` → `git push origin backup‑2025‑06‑11`                                                             | Zero clutter in branch list, cannot be overwritten by accident.                    | Static—can’t add more commits.                                                 |
| **Archive branch kept *only* on remote** | `git checkout -b archive/2025‑06‑11 && git push -u origin archive/2025‑06‑11`<br>Then *delete it locally*: `git checkout main && git branch -D archive/...` | You can still cherry‑pick or hot‑fix on top of it later.                           | Shows up in remote branch list forever; can pile up if you’re not disciplined. |
| **Release branch (Git Flow style)**      | `release/2.0` branched off `main`, receives only bug fixes; each hot‑fix is tagged (`v2.0.1`).                                                              | Clear maintenance lane; production code stays shielded from new features.          | More branches to protect/manage; overkill for very small teams.                |
| **Full mirror backup**                   | `git remote add backup git@bitbucket:lab/sc‑proj.git` then `git push backup --mirror`.                                                                      | Disaster‑recovery copy of *all* refs, not just selective tags/branches.            | Needs automation (cron/CI) and access to another server.                       |
| **GitHub/GitLab Release**                | Push a tag, click *“Draft release”*, attach artifacts (conda‑pack, h5ad).                                                                                   | Combines code snapshot *and* binary outputs in one place with DOI option (Zenodo). | Still relies on the tag mechanism; not ideal for WIP.                          |

---

## What productive teams actually do

1. **Work trunk‑based or Git Flow**

   * Small teams: a single `main`/`dev` branch + short‑lived feature branches.
   * Bigger teams: `main` → release branches (`release/1.x`) + hot‑fix branches.

2. **Tag every production or analytical milestone**
   *Automated in CI:* when `main` is tagged `vX.Y.Z`, pipelines run, containers build, releases publish.

3. **Delete merged feature branches**
   Keeps `git branch -r` list ≤ \~10. Historic commits + tags are enough to recover code.

4. **Protect critical branches, lock tags**
   GitHub branch protection + “Require signed tags” prevents accidental force‑pushes.

5. **Secondary off‑site mirror**
   Nightly `git push --mirror` to a second host (Bitbucket, GitLab, AWS CodeCommit) for “air‑gapped” backup.

---

## A pragmatic backup recipe for your single‑cell project

```bash
# 1. Before a risky refactor
git tag -a backup-pre-refactor-20250611 -m "Stable before new QC module"
git push origin backup-pre-refactor-20250611   # safe snapshot

# 2. Start work on a *temporary* feature branch
git checkout -b feat/new-qc

# 3. When feature merges, delete the branch
git checkout main && git merge --no-ff feat/new-qc
git push origin main
git push origin --delete feat/new-qc
```

*Result:* your branch list stays clean, but the tag permanently records the pre‑refactor state.

---

## TL;DR

* **Need a quick, permanent snapshot?** → Use an **annotated tag** and push it.
* **Need to continue editing that snapshot?** → Create a **branch**, but delete it locally when merged, or move it under an `archive/` namespace.
* **Worried about losing everything?** → Automate a `--mirror` push to a second remote.

Combine these with protected branches and automated releases, and you’ll have both tidy history **and** rock‑solid backups—just like the big teams.

















# Which reference type is fastest for **jumping back‑and‑forth** and **diffing**?

| Action                           | Lightweight **tag**                                            | **Branch**                                           | Why it matters                                           |
| -------------------------------- | -------------------------------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| **Checkout (read‑only)**         | `git switch --detach v1.4.0` → *detached HEAD*                 | `git switch backup/2025‑06‑11`                       | Both are one‑line and instant; no real speed difference. |
| **Make edits / hot‑fix**         | Must first make a branch: `git switch -c hotfix/v1.4.0 v1.4.0` | Already writable                                     | Branch wins for anything beyond inspection.              |
| **Diff against `main`**          | `git diff v1.4.0..main path/to/file.py`                        | `git diff backup/2025‑06‑11..main`                   | Same syntax; both easy.                                  |
| **List history graphically**     | `git log --decorate --graph --oneline --all` shows tags inline | Branch shows up in `git branch -a` list, tags do not | Too many *backup* branches can clutter the view.         |
| **Accidental edits on snapshot** | Impossible—the tag is immutable                                | Possible if you forget to protect the branch         | Tag is safer.                                            |

---

### Recommended workflow for **“switch, inspect, maybe patch”**

1. **Tag first – for a pristine snapshot**

   ```bash
   git tag -a snapshot‑2025‑06‑11 -m "Before major refactor"
   git push origin snapshot‑2025‑06‑11
   ```

2. **Create a *throw‑away* branch only when you need to touch code**

   ```bash
   # jump to the snapshot in read‑only mode (detached HEAD)
   git switch --detach snapshot‑2025‑06‑11

   # realise you need to patch something?
   git switch -c hotfix/snapshot‑2025‑06‑11   # now you're on a branch
   ```

3. **Compare specific files or directories**

   ```bash
   # Compare a single module
   git diff snapshot‑2025‑06‑11..main src/qc/filtering.py

   # or interactive tool (requires difftool configured)
   git difftool snapshot‑2025‑06‑11..HEAD -- src/qc/
   ```

4. **Merge or cherry‑pick if the patch is valuable**

   ```bash
   git checkout main
   git merge --no-ff hotfix/snapshot‑2025‑06‑11      # or cherry‑pick one commit
   git push origin main
   ```

5. **Delete the temporary branch to keep things tidy**

   ```bash
   git branch -d hotfix/snapshot‑2025‑06‑11
   git push origin --delete hotfix/snapshot‑2025‑06‑11
   ```

---

### Power tip: **`git worktree`** for *simultaneous* views

```bash
# Check out the tag in a sibling directory without touching your main working tree
git worktree add ../proj‑snapshot snapshot‑2025‑06‑11
```

You now have two folders:

* `sc‑project/` – the normal `main`
* `proj‑snapshot/` – frozen at the tag

Open both in your IDE and diff visually; no branch juggling required. When done:

```bash
git worktree remove ../proj‑snapshot
```

---

## TL;DR

* **Tag** every backup point — it’s immutable and invisible in the branch list.
* **Branch only as a scratchpad** when you discover you actually need to edit or test code on that snapshot.
* Use `git diff TAG..main <file>` or `git worktree` for side‑by‑side comparison.

This hybrid (“tag + ad‑hoc branch”) keeps history clean **and** lets you jump, compare, or patch in seconds—exactly how mature teams stay productive without drowning in stale branches.

