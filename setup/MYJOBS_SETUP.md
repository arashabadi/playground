# `myjobs` Setup Guide for Linux Systems

This guide shows how to set up a `myjobs` command that gives you a live,
auto-refreshing view of your active Slurm jobs.

It is designed to be portable across Linux systems that use Slurm.

## What `myjobs` Does

`myjobs` runs a `watch` command that refreshes every second and shows:

- job ID
- job name
- state
- elapsed time
- time limit
- partition
- CPU count
- memory
- GPU request
- reason
- node

It shows active jobs in these Slurm states:

- `R` for running
- `CG` for completing
- `PD` for pending

## Important Requirement

This command is Slurm-specific.

It will only work on Linux systems where these commands are available:

- `squeue`
- `watch`

Check first:

```bash
command -v squeue
command -v watch
```

If either command is missing, `myjobs` will not work until the system admin or
package manager provides it.

Typical packages:

- Debian/Ubuntu: `procps` provides `watch`
- RHEL/CentOS/Rocky/Alma: `procps-ng` provides `watch`
- Slurm client tools are usually installed by the cluster

## Recommended Setup

The most reliable setup is to make `myjobs` a small executable script in
`~/bin` instead of a shell alias or function.

This avoids quoting problems and works across Bash and Zsh.

### Step 1: Create `~/bin` if needed

```bash
mkdir -p ~/bin
```

### Step 2: Create the `myjobs` script

```bash
cat > ~/bin/myjobs <<'EOF'
#!/bin/bash
watch -n 1 'printf "%-18s %-24s %-10s %-10s %-10s %-10s %-6s %-8s %-10s %-20s %-20s\n" JOBID NAME STATE ELAPSED LIMIT PARTITION CPU MEM GRES REASON NODE; squeue -h -r -u "$USER" -t R,CG,PD -o "%.18i %.24j %.10T %.10M %.10l %.10P %.6C %.8m %.10b %.20R %.20N" | sort -V'
EOF
```

### Step 3: Make it executable

```bash
chmod +x ~/bin/myjobs
```

### Step 4: Add `~/bin` to your `PATH`

For Bash:

```bash
grep -qxF 'export PATH="$HOME/bin:$PATH"' ~/.bash_profile || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bash_profile
export PATH="$HOME/bin:$PATH"
```

For Zsh:

```bash
grep -qxF 'export PATH="$HOME/bin:$PATH"' ~/.zshrc || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
export PATH="$HOME/bin:$PATH"
```

If you are not sure which shell you are using:

```bash
echo "$SHELL"
```

## Step 5: Test It

Run:

```bash
myjobs
```

You should see a live table that refreshes every second.

Exit with:

```bash
Ctrl+C
```

## What You Should See

A typical screen looks like this:

```text
JOBID              NAME                     STATE      ELAPSED    LIMIT      PARTITION  CPU    MEM      GRES       REASON               NODE
38050001           cellbender_rm_bg        R          00:13:04   12:00:00   pascalnodes 8      64G      gpu:1      n/a                  c123
38050002           cellbender_env          PD         00:00:00   02:00:00   short       4      32G      N/A        Priority             (null)
```

## How to Customize It

### Refresh slower or faster

Change:

```bash
watch -n 1
```

Examples:

- every 2 seconds: `watch -n 2`
- every 5 seconds: `watch -n 5`

### Show only running jobs

Change:

```bash
-t R,CG,PD
```

to:

```bash
-t R,CG
```

### Show only pending jobs

Change:

```bash
-t R,CG,PD
```

to:

```bash
-t PD
```

### Show only jobs whose names match a pattern

Add `awk` after `squeue`.

Example for names starting with `cellbender`:

```bash
squeue -h -r -u "$USER" -t R,CG,PD -o "..." | awk '$2 ~ /^cellbender/' | sort -V
```

## Troubleshooting

### `myjobs: command not found`

Usually means one of these:

- `~/bin/myjobs` does not exist
- `~/bin/myjobs` is not executable
- `~/bin` is not in `PATH`

Check:

```bash
ls -l ~/bin/myjobs
echo "$PATH"
```

### `squeue: command not found`

Your Linux system does not currently have Slurm client tools in `PATH`.

This command cannot work until `squeue` is available.

### `watch: command not found`

Install the package that provides `watch`.

Examples:

```bash
sudo apt install procps
```

```bash
sudo dnf install procps-ng
```

### Blank output

Usually means:

- you have no active Slurm jobs
- or the system is not using Slurm

Try:

```bash
squeue -u "$USER"
```

## Why This Approach Is Better Than an Alias

Using a standalone `~/bin/myjobs` script is usually better than an alias or a
shell function because:

- it works the same way in Bash and Zsh
- it avoids quote-escaping problems
- it is easier to edit later
- it is easier to copy to another system

## Copying to Another Linux System

On a second Linux machine with Slurm:

1. copy `~/bin/myjobs`
2. make sure it is executable
3. make sure `~/bin` is in `PATH`

That is all you need.
