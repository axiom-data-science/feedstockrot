[![Build Status](https://travis-ci.org/axiom-data-science/feedstockrot.svg)](https://travis-ci.org/axiom-data-science/feedstockrot)

### Installation

```bash
conda install --channel conda-forge feedstockrot
```

Or, in its own environment:

```bash
conda create --name feedstockrot feedstockrot
source activate feedstockrot
```

### Usage:

To start, just execute and specify which packages to check:

```bash
feedstockrot cherrypy matplotlib flake8 netcdf4 redis-py
```

To check all of *your* feedstocks, export a GitHub token and run:

```bash
export FEEDSTOCKROT_GITHUB_TOKEN=your-github-token
feedstockrot --github
```

## Development

### Setup

Setup a conda environment and install dependencies:

```bash
conda create -name feedstockrot-dev --file requirements.txt python=3.5
source activate feedstockrot-dev
conda install --file requirements-dev.txt
```

Optionally, install this tool in editable mode. This isn't required, as `main.py` can be executed directly.

```bash
pip install --editable .
```

***

Brought to you by [Axiom Data Science](http://www.axiomdatascience.com/).
