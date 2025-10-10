# Christian's experiments

## Getting started

Make sure you have `uv` installed on your system.
View the [documentation](https://docs.astral.sh/uv/#installation) for installation instructions.

Then, create a virtual environment using `uv`:

```bash
uv sync
```

Then add the venv to a list of known jupyter kernels. The storage location is `~/.local/share/jupyter/kernels/` on Linux.

```bash
uv run python -m ipykernel install --user --name=modern-ml
```

When selecting kernel in VSCode, you should be able to find `modern-ml` in the list of *Jupyter kernels*.
This ensures that you're getting the latest and greatest python 3.14, and a set of dependencies that are known to work with the project files.

## Run python file

To use the virtual environment created by `uv`, run the python file like this:

```bash
uv run python main.py
```

`main.py` checks that you're using the correct python version (3.14.0).
If you run `python main.py`, you'll be using system python, which is most likely not 3.14.0.
