# Tidy3d Python API

To compile the docs, you'll need to install `sphinx`, `sphinx-rtd-theme`, and `jupyter-sphinx`. Then:

```
cd docs
make html
browse _build/html/index.html
```

## How to update what

- Stuff in the `tidy3d/` folder here (apart from the `web/` module inside of it) is never directly updated. Instead the `sim/` folder is copied over from the `tidy3d` repo.
- Docs are only updated here. After an update, all the notebooks from `docs/examples` should be pushed to the public `tidy3d-notebooks` repo, and the build in `docs/_build/html/` should be pushed to the docs folder of the `tidy3d_static_web`.
