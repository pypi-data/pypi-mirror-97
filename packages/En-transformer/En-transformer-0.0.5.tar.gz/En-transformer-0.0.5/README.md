## E(n)-Equivariant Transformer (wip)

Implementation of E(n)-Equivariant Transformer, which extends the ideas from Welling's <a href="https://github.com/lucidrains/egnn-pytorch">E(n)-Equivariant Graph Neural Network</a> with attention.

Note - still having issues where at depths greater than 1, equivariance is not preserved.

## Install

```bash
$ pip install En-transformer
```

## Usage

```python
import torch
from en_transformer import EnTransformer

model = EnTransformer(
    dim = 512,
    depth = 4,
    dim_head = 64,
    heads = 8,
    edge_dim = 4,
    fourier_features = 2
)

feats = torch.randn(1, 16, 512)
coors = torch.randn(1, 16, 3)
edges = torch.randn(1, 16, 16, 4)

feats, coors = model(feats, coors, edges)  # (1, 16, 512), (1, 16, 3)
```

## Todo

- [ ] masking
- [ ] neighborhoods by radius

## Citations

```bibtex
@misc{satorras2021en,
    title 	= {E(n) Equivariant Graph Neural Networks}, 
    author 	= {Victor Garcia Satorras and Emiel Hoogeboom and Max Welling},
    year 	= {2021},
    eprint 	= {2102.09844},
    archivePrefix = {arXiv},
    primaryClass = {cs.LG}
}
```
