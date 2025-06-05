## Here are some notes and resources I found to master Git and GitHub:

- [How We Encode Code Reviews at Netlify](https://www.netlify.com/blog/2020/03/05/feedback-ladders-how-we-encode-code-reviews-at-netlify/)

_Good insights on how to contribute effectively and issues categorization tutorial_
--------------------------------

## I am trying to make GitHub actions work with my Patoq book
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


### I had some faluires with the GitHub Actions workflow, so I had to revert to some specific commit.

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


