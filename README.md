Usage:

To start, just execute and specify which packages to check:

```
python main.py cherrypy matplotlib flake8 netcdf4 redis-py
```

To check all of *your* feedstocks, export a GitHub token and run:

```
export FEEDSTOCKROT_GITHUB_TOKEN=your-github-token
python main.py --github
```
