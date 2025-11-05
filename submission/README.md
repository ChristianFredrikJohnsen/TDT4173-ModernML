# Instructions for reproducing results

In order to get reproducible results, you need the exact same GPU as the one we used for training.
We had different team members using different GPUs, so the two submission were using different GPUs.

We believe the different results appear because random seeds are not set the same way across different GPU architectures.

HOWEVER, if you are on the same hardware configuration as us, you will get the exact same results **every time** you run the notebooks. One hardware configuration leads to **exactly one** result for a jupyter notebook file.

## Python packages

To get the exact same environment as we used, we've provided the `pyproject.toml` and `uv.lock` files as part of the submission.

The python packages are obtained using `uv sync`.
After `uv sync`, you can do a `uv run python -m ipykernel install --user --name=uv` to create a jupyter kernel named `uv`, which you then can select to run the notebooks.

## Short_notebook_1.ipynb

The hardware used when running this notebook was:

- GPU: NVIDIA RTX A3000 12GB Laptop GPU
- OS: Ubuntu 25.10

The file which is produced when running this notebook is `FULL_PIPELINE_short.csv`, which got a score of 4898.77900 on the public leaderboard on Kaggle.

## Short_notebook_2_MORE_FEATURES.ipynb

The hardware used when running this notebook was:

- GPU: NVIDIA GeForce RTX 3070
- OS: Windows 11 Home 24H2

The file which is produced when running this notebook is `FULL_PIPELINE_more_features.csv`, which got a score of 4014.47884 on the public leaderboard on Kaggle.
