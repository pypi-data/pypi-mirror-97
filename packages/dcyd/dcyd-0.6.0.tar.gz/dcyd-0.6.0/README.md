# DCYD Model Performance Monitoring Client

This is a development README, for end users' README, see [setup.py](setup.py)

## Development

### Environment requirements

* Python 3.8.x is installed. See [pyenv](https://github.com/pyenv/pyenv)
* pipenv is installed. See [Install Pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today )
* git is installed. See [Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git )

### Initial project setup

```bash
git clone git@github.com:dcyd-inc/dcyd-mpm-client-python.git
cd dcyd-mpm-client-python
git checkout develop
pipenv install --dev
```


### Distributing the package in PyPI

This process comes from [this turorial](https://packaging.python.org/tutorials/packaging-projects/).
1. Increment the version in `setup.py`, using [these rules](https://www.python.org/dev/peps/pep-0440/) (or newer).
2. Install/update some modules:

```bash
pipenv install --dev
```

3. From the directory containing `setup.py` (and _not_ in a virtual environment), create the wheel:

```bash
rm -rf build/ dist/
pipenv run python3 setup.py sdist bdist_wheel
```

4. Upload the wheel to PyPI:
```bash
pipenv run python3 -m twine upload dist/*
```
