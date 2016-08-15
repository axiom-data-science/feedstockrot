### Installation

Setup a conda environment and install dependencies:

```bash
conda create -n feedstockrot --file requirements.txt python=3.5
source activate feedstockrot
```

Then install this tool:

```bash
cd /path/to/feedstockrot
pip install .
```

### Usage:

To start, just execute and specify which packages to check:

```
feedstockrot cherrypy matplotlib flake8 netcdf4 redis-py
```

To check all of *your* feedstocks, export a GitHub token and run:

```
export FEEDSTOCKROT_GITHUB_TOKEN=your-github-token
feedstockrot --github
```

***

Brought to you by [Axiom Data Science](http://www.axiomdatascience.com/).
