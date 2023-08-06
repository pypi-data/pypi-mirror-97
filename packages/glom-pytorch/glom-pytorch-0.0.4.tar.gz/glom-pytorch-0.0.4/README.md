<img src="./glom2.png" width="400px"></img>

<img src="./glom1.png" width="600px"></img>

## GLOM - Pytorch (wip)

An attempt at the implementation of <a href="https://arxiv.org/abs/2102.12627">Glom</a>, Geoffrey Hinton's new idea that integrates neural fields, predictive coding, top-down-bottom-up, and attention (consensus between columns) for emergent part-whole heirarchies from data.

## Install

```bash
$ pip install glom-pytorch
```

## Usage

```python
import torch
from glom_pytorch import Glom

model = Glom(
    dim = 512,         # dimension
    levels = 6,        # number of levels
    image_size = 224,  # image size
    patch_size = 14    # patch size
)

img = torch.randn(1, 3, 224, 224)
levels = model(img, iters = 12) # (1, 256, 6, 512) - (batch - patches - levels - dimension)
```

If you were to pass the `return_all = True` keyword argument on forward, you will be returned all the column and level states per iteration, including the initial state (so number of iterations + 1). You can then use this to attach any losses to any time step you wish, to induce emergence of whatever.

```python
import torch
from glom_pytorch import Glom

model = Glom(
    dim = 512,         # dimension
    levels = 6,        # number of levels
    image_size = 224,  # image size
    patch_size = 14    # patch size
)

img = torch.randn(1, 3, 224, 224)
all_levels = model(img, iters = 12, return_all = True) # (13, 1, 256, 6, 512) - (batch, patches, levels, dimension)

# get the top level outputs at iteration 6
top_level_output = all_levels[7, :, :, 5] # (1, 256, 512) - (batch, patches, dimension)
```

## Citations

```bibtex
@misc{hinton2021represent,
    title   = {How to represent part-whole hierarchies in a neural network}, 
    author  = {Geoffrey Hinton},
    year    = {2021},
    eprint  = {2102.12627},
    archivePrefix = {arXiv},
    primaryClass = {cs.CV}
}
```
