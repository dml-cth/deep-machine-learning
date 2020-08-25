# Keeping the git repository in sync
During the course, the GitHub repository is expected to be updated many times, for various reasons, e.g.
- Updating instructions
- Posting new assignments
- Updating already released assignments (we will do our best to avoid it, but at times it may be necessary for us to do this)

All `git` commands assume that you have navigated to somewhere inside the repository (that is, the *deep-machine-learning* directory).

## Determining the state of your local git repository
If you are using Mac / Linux, and are not very familiar with git but still care about version control, Sourcetree is recommended as a graphical interface to git.
https://www.sourcetreeapp.com/

### Knowing whether you need to sync
- First of all (after you have navigated to your cloned git repo in the terminal), run the command `git fetch`. This will never modify any of the files you are working on - git will just find out which is currently the latest version on GitHub.
- Now, run `git log --all --decorate --oneline --graph` to see the commit history (a commit is a set of changes), and locate "*master*" (which should be prepended by "*HEAD ->*"), and "*origin/master*". Note: your terminal & git installation can probably be configured to provide you color-coded output from `git log`, which makes it a bit easier to parse.
- In the output above, "*master*" shows where your local repository is, and "*origin/master*" shows the most recent version on GitHub. If they are not the same, you should probably update.
- If you get "stuck" inside the git log, press `q` to exit.
- If you are hesitant to sync, you can further investigate what the changes consist of. For instance, if you run the `git log` command above, but now add the `--stat` argument as well, you will see which files were modified in each commit.

### Examining your local modifications
- Run `git status` for an overview over the files you have modified. That is, the files which deviate from *master* in the git log above. Note that *master* is not necessarily the same as the latest version on GitHub.
- Run `git diff` to list exactly what changes you have made, or optionally `git diff <REL_PATH_TO_FILE>` to examine the changes for a particular file. If you get stuck inside `git diff`, press `q` to exit.

## Syncing
### Avoid syncing by re-cloning
- Rename the current git repo (to *deep-machine-learning-old* or whatever).
- In the terminal, navigate to the directory one level above (inside of which *deep-machine-learning-old* resides)
- Re-run the command for cloning the course repository (according to the instructions you followed when doing this last time)
- Now, a new directory *deep-machine-learning* will be created next to *deep-machine-learning-old*.
- Copy-paste the code from your old notebooks to the new ones. You need to be able to open both the old & new notebooks simultaneously, and there are different ways to do this:
  1. One way is to first copy the old notebooks to the new repo (with replacing the new notebooks, rather having them side-by-side).
  1. Another way is to start the Jupyter server one level above the *deep-machine-learning* and *deep-machine-learning-old* directories, so that the files within both are accessible.
  1. Yet another way is to run two Jupyter servers simultaneously.
- Continue working in the new repo.

This procedure will always work, i.e. you do not need to sync as explained below. Syncing is however much more convenient, and you are encouraged to at least attempt the "easy" sync explained below, since it cannot really cause you any harm.

### Attempt an easy sync (for minor changes)
If you do not want to get your hands dirty with git, and hence have not made any commits of your own, there is still a way to safely attempt an "easy" sync, without possibly getting yourself into trouble. This operation does however assume that no files were modified both by you and on GitHub.
- Follow the "Prepare to sync" instructions at the end of this page.
- Run `git pull`. Pay attention to the output. Did it succeed?
- If you are lucky (i.e. git judges your local modifications to clearly not interfere with the updates on GitHub), the `git pull` will succeed, and you are good to go.
- If the command did not succeed, you will get the error message `error: Your local changes to the following files would be overwritten by merge:`, followed by a list of relative paths to files which have been modified both by you and on GitHub.
- Now it is up to you whether you can live with discarding your local changes to these particular files.
  - To discard your own modifications to a certain file, run `git checkout -- <REL_PATH_TO_FILE>`.
  - To interactively select which files (or parts of files even) to discard, run `git checkout -p`.
  - To discard all of your own modifications (to **all** files listed as modified by `git status`, but excluding the ones listed as untracked), run `git reset --hard`.
- If you have decided to (and managed to) discard your local modifications to the problematic files above, you should now succeed to run `git pull`.

### Syncing the "right" way
This assumes some familiarity with git. It is however always possible to abort the attempt to sync as explained below.
- Follow the "Prepare to sync" instructions at the end of this page.
- Add & commit your changes.
- Run `git pull`, or `git pull --rebase` (which results in a cleaner version history).
- If you get conflicts, you have two options:
  - **Resolve**
    - Resolve the conflicts, and continue the merge / rebase as explained by git
  - **Abort**
    - Run `git merge --abort`, or `git rebase --abort` (depending on whether you used the `--rebase` argument when pulling).\
    - Run `git reset HEAD^` to undo the commit you did before (files are not changed, you are just undoing reporting the changes in a git "commit").
    - Now, you can try to perform the sync as explained in the other sections.
- After the sync, make sure that the version check at the beginning of your notebooks succeed!

## Prepare to sync - clean up your notebook modifications
Your notebook is internally represented as a `.ipynb` text file, and it will not only contain your code, but also a number of other things, such as:
- The outputs from commands you have run, including plots
- Execution count, i.e. how many times each cell has been executed.

Whenever you interact with the notebook, this sort of data will change, which may result in complications when you use git to sync your changes with the changes on GitHub. It is therefore good procedure to clean up this data before attempting to sync.

Follow these steps before syncing:
- Click "Kernel" -> "Restart & Clear Output" in the Jupyter interface in the browser.
- Save the notebook (Important! You cannot always rely on autosave.)
- Click "File" -> "Close and Halt". If ommitting this step, Jupyter will complain later when git modifies the file from the outside.
