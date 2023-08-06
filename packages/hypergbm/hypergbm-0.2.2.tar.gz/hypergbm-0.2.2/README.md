# HyperGBM
[![Python Versions](https://img.shields.io/pypi/pyversions/hypergbm.svg)](https://pypi.org/project/hypergbm)
[![Downloads](https://pepy.tech/badge/hypergbm)](https://pepy.tech/project/hypergbm)
[![PyPI Version](https://img.shields.io/pypi/v/hypergbm.svg)](https://pypi.org/project/hypergbm)

[Doc](https://hypergbm.readthedocs.io/en/latest/) | [中文](https://hypergbm.readthedocs.io/zh_CN/latest/)

## What is HyperGBM
HyperGBM is a library that supports full-pipeline AutoML, which completely covers the end-to-end stages of data cleaning, preprocessing, feature generation and selection, model selection and hyperparameter optimization.It is a real-AutoML tool for tabular data.

## Overview 

Unlike most AutoML approaches that focus on tackling the hyperparameter optimization problem of machine learning algorithms, HyperGBM can put the entire process from data cleaning to algorithm selection in one search space for optimization. End-to-end pipeline optimization is more like a sequential decision process, thereby HyperGBM uses reinforcement learning, Monte Carlo Tree Search, evolution algorithm combined with a meta-learner to efficiently solve such problems.

As the name implies, the ML algorithms used in HyperGBM are all GBM models, and more precisely the gradient boosting tree model, which currently includes XGBoost, LightGBM and Catboost.

The underlying search space representation and search algorithm in HyperGBM are powered by the [Hypernets](https://github.com/DataCanvasIO/Hypernets) project a general AutoML framework.

## Tutorial
* [Quick Start](https://hypergbm.readthedocs.io/en/latest/quick_start.html)
* [Examples](https://hypergbm.readthedocs.io/en/latest/example.html)
* [CompeteExperiment](https://hypergbm.readthedocs.io/en/latest/compete_experiment.html)
* [HyperGBM](https://hypergbm.readthedocs.io/en/latest/hypergbm.html)
* [Searchers](https://hypergbm.readthedocs.io/en/latest/searchers.html)

## Installation
```shell script
pip install hypergbm
```

## Examples

User can create experiment instance with `make_experiment` and run it quickly。`train_data` is the only required parameter, all others are optional.   The `target` is also required if your target feature name isn't `y`。

Codes:
```python
from hypergbm import make_experiment
from tabular_toolbox.datasets import dsutils

train_data = dsutils.load_blood()
experiment = make_experiment(train_data, target='Class')
estimator = experiment.run()
print(estimator)
```

Outputs：
```
Pipeline(steps=[('data_clean',
                 DataCleanStep(...),
                ('estimator',
                 GreedyEnsemble(...)])

Process finished with exit code 0
``` 

Hypergbm also provides command line tools to train models and predict data:
```
hypergm -h

usage: hypergbm [-h] --train_file TRAIN_FILE [--eval_file EVAL_FILE]
                [--eval_size EVAL_SIZE] [--test_file TEST_FILE] --target
                TARGET [--pos_label POS_LABEL] [--max_trials MAX_TRIALS]
                [--model_output MODEL_OUTPUT]
                [--prediction_output PREDICTION_OUTPUT] [--searcher SEARCHER]
...
```

For example,  train dataset [blood.csv](https://github.com/DataCanvasIO/tabular-toolbox/blob/main/tabular_toolbox/datasets/blood.csv):
```shell script
hypergbm --train_file=blood.csv --test_file=blood.csv --target=Class --pos_label=1 --model_output=model.pkl
```


## Hypernets related projects

* [HyperGBM](https://github.com/DataCanvasIO/HyperGBM): A full pipeline AutoML tool integrated various GBM models.
* [HyperDT/DeepTables](https://github.com/DataCanvasIO/DeepTables): An AutoDL tool for tabular data.
* [HyperKeras](https://github.com/DataCanvasIO/HyperKeras): An AutoDL tool for Neural Architecture Search and Hyperparameter Optimization on Tensorflow and Keras.
* [Cooka](https://github.com/DataCanvasIO/Cooka): Lightweight interactive AutoML system.
* [Hypernets](https://github.com/DataCanvasIO/Hypernets): A general automated machine learning framework.

![DataCanvas AutoML Toolkit](docs/static/images/datacanvas_automl_toolkit.png)


## DataCanvas
HyperGBM is an open source project created by [DataCanvas](https://www.datacanvas.com/). 
