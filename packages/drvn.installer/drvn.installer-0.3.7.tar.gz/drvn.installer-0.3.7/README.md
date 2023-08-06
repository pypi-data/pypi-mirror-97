# Installer

## Usage

```
drvn_installer --help
```

## Installing

### Installing in editable-mode

```
sudo -H python3.8 -m pip install --editable .
```

### Installing in the usual, non-editable mode

```
python3.8 -m pip install --user drvn.installer
```

## Testing

### Testing prerequisites

```
python3.8 -m pip install --user --upgrade tox
```

### Running all tests

Runs unit- and integration tests using multiple python versions (specified by tox.ini's envlist)

```
tox
```

### Running unit tests

```
tox -e unit
```

### Running integration tests

```
tox -e integration
```

## Uploading

### Uploading to PyPi

```
#
# Make sure python3.8 setup.py --version is correct
# (edit version by creating a git tag ..see setuptools_scm)
#
# then:
python3.8 setup.py sdist bdist_wheel
twine upload dist/*
# or:
twine upload -u USER -p PASSWORD dist/*
```
