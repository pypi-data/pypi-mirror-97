# Phylodeep

Phylodeep is a python library for parameter estimation and model selection from phylogenetic trees, based on deep learning.

## Installation

Use the package [pip](https://pip.pypa.io/en/stable/) to install phylodeep.

## Usage 

###Python

```python
import phylodeep
from phylodeep import BD, BDSS, BD_vs_BDEI, BD_vs_BDSS, SUMSTATS, FULL

path_to_tree = './tests/Zurich.trees'

# set presumed sampling probability
sampling_proba = 0.20

# a priori check


# model selection
model_BD_vs_BDEI = phylodeep.modeldeep(path_to_tree, sampling_proba, vector_representation=SUMSTATS)
model_BD_vs_BDSS = phylodeep.modeldeep(path_to_tree, sampling_proba, vector_representation=FULL)

# the selected model is BDSS

# parameter inference
inference_param_BD = phylodeep.paramdeep(path_to_tree, sampling_proba, model=BD, vector_representation=FULL)
inference_param_BDSS = phylodeep.paramdeep(path_to_tree, sampling_proba, model=BDSS, vector_representation=FULL)

```

###Command line
```python
paramdeep -t ./tests/Zurich.trees -p 0.25 -m BDSS -v CNN_FULL_TREE -o HIV_Zurich_BDSS_CNN.csv
paramdeep -t ./tests/Zurich.trees -p 0.25 -m BDSS -v FFNN_SUMSTATS -o HIV_Zurich_BDSS_FFNN.csv

```



## Citation


## Contributing


## License