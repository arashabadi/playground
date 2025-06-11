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








# tagging

In Git, “adding a version” usually means **tagging** a specific commit (often the tip of `main`/`master`) with a version label such as `v1.2.0`. Tags are immutable markers: once created they always point to exactly that snapshot of the code, so you can check it out later or attach release notes to it.

```bash
# 1 — Commit whatever changes make up the release
git add .
git commit -m "Prepare v1.2.0 release"

# 2 — Create an *annotated* tag (carries author, date, and message)
git tag -a v1.2.0 -m "Release v1.2.0"

# 3 — Push the commit *and* the tag
git push origin main          # or whatever branch
git push origin v1.2.0        # or: git push --tags
```

---

### Why annotated tags?

* They store extra metadata (author, timestamp, message) and are treated as first‑class “releases” by platforms like GitHub/GitLab.
* Lightweight tags (`git tag v1.2.0`) exist but are just pointers—fine for quick bookmarks but not ideal for published releases.

---

### Picking a version string

Most projects follow **Semantic Versioning** (`MAJOR.MINOR.PATCH`):

| Part      | Bumps when you…                                | Example |
| --------- | ---------------------------------------------- | ------- |
| **MAJOR** | break backward compatibility                   | 2.0.0   |
| **MINOR** | add functionality in a backward‑compatible way | 1.3.0   |
| **PATCH** | fix bugs without changing the API              | 1.3.1   |

Pre‑release identifiers (`-alpha.1`, `-rc.2`) and build metadata (`+001`) are also allowed.

---

### Keep the version inside your code, too

Many languages let you define a `__version__`, `VERSION`, or similar constant so the application can report its own version at runtime. Bump *both* the in‑code constant and the Git tag at release time, and consider automating the pair with a release script or CI job.

---

### Automating releases on GitHub/GitLab

1. **GitHub:** After pushing a tag, open *Releases → Draft new release*. Select the tag, write notes, and publish. CI/CD workflows (e.g., GitHub Actions) can be triggered on `push.tags`.
2. **GitLab:** Similar—navigate to *Repository → Tags*, click the tag, and create a release or configure a pipeline on `only: tags`.

---

### Common pitfalls

| Pitfall                                      | Fix                                                                                                                          |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Tag created on the wrong commit              | Delete locally (`git tag -d v1.2.0`), delete remotely (`git push origin :refs/tags/v1.2.0`), then re‑tag the correct commit. |
| Forgot to push the tag                       | `git push origin --tags` pushes all missing tags.                                                                            |
| Local version constant doesn’t match the tag | Add a release checklist or CI step that fails if they differ.                                                                |

---

### Next steps

* If you need to **sign** releases, use `git tag -s v1.2.0` (requires GPG key).
* Want a **branch‑based** flow? Keep a long‑lived `release/1.x` branch and tag each patch off it.
* Need language‑specific packaging (PyPI, npm, crates.io)? Let CI listen for version tags and publish automatically.

Let me know if you’d like an example CI workflow, version‑bumping script, or guidance for a specific language or hosting platform!




