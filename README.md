# template-repo
Use this as a starting point for any Paulsson Lab repo. Comes with code formatting pre-commit hooks (black, jupytext, nbstripout) preconfigured.

## How to make a new repo
1. Go to the https://github.com/paulssonlab/template-repo (this page) and click "Use this template" to create a new repo under the Paulsson Lab GitHub organization. Click “Clone or download” and copy the git URL and save it for later (e.g., `git@github.com:paulssonlab/new-repo.git`).
2. Click "Fork" to fork this repo under your personal GitHub account. Click “Clone or download” and copy the git URL.
3. Run `git clone git@github.com:shenker/new-repo.git` (where that is the git URL for your personal fork; in this case, `shenker` is my GitHub username).
4. Run `cd new-repo; git add remote upstream git@github.com:paulssonlab/new-repo.git` (where that is the git URL of the original new repo, in the paulssonlab GitHub organization). Now you can `git push origin` to push to your personal branch and `git push upstream` when you are ready to push your changes to the rest of the lab.

## Installation
After cloning this repository, run the following (replace `template` with the desired name for your conda environment):
```
conda env create -n template -f environment.yml
echo "conda activate template" > .envrc
direnv allow
pre-commit install
nbstripout --install
```

The first command creates a conda environment using the list of packages in `environment.yml`. The next two commands make this conda environment activate automatically when you `cd` into this repo (if you aren't using direnv, skip these two commands and run an explicit `conda activate template` instead). The last two commands set up the pre-commit hooks that automatically format code (in both `.ipynb` and `.py` files) and strip output from jupyter notebooks before adding them to git. If you're starting from an empty conda environment, install these tools with `conda install -c conda-forge pre-commit black jupytext nbstripout`.
