# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_forecasting',
 'pytorch_forecasting.data',
 'pytorch_forecasting.models',
 'pytorch_forecasting.models.deepar',
 'pytorch_forecasting.models.mlp',
 'pytorch_forecasting.models.nbeats',
 'pytorch_forecasting.models.nn',
 'pytorch_forecasting.models.rnn',
 'pytorch_forecasting.models.temporal_fusion_transformer']

package_data = \
{'': ['*']}

install_requires = \
['fsspec>=0.8.5,<0.9.0',
 'matplotlib',
 'optuna>=2.3.0,<3.0.0',
 'pandas>=1.1.0,<2.0.0',
 'pytorch-lightning>=1.0.4,<2.0.0',
 'scikit-learn>=0.23,<0.25',
 'scipy',
 'statsmodels',
 'torch>=1.7,<2.0']

extras_require = \
{'github-actions': ['pytest-github-actions-annotate-failures']}

setup_kwargs = {
    'name': 'pytorch-forecasting',
    'version': '0.8.4',
    'description': 'Forecasting timeseries with PyTorch - dataloaders, normalizers, metrics and models',
    'long_description': '![](./docs/source/_static/logo.svg)\n\nOur article on [Towards Data Science](https://towardsdatascience.com/introducing-pytorch-forecasting-64de99b9ef46)\nintroduces the package and provides background information.\n\nPytorch Forecasting aims to ease state-of-the-art timeseries forecasting with neural networks for real-world cases and research alike. The goal is to provide a high-level API with maximum flexibility for professionals and reasonable defaults for beginners.\nSpecifically, the package provides\n\n- A timeseries dataset class which abstracts handling variable transformations, missing values,\n  randomized subsampling, multiple history lengths, etc.\n- A base model class which provides basic training of timeseries models along with logging in tensorboard\n  and generic visualizations such actual vs predictions and dependency plots\n- Multiple neural network architectures for timeseries forecasting that have been enhanced\n  for real-world deployment and come with in-built interpretation capabilities\n- Multi-horizon timeseries metrics\n- Ranger optimizer for faster model training\n- Hyperparameter tuning with [optuna](https://optuna.readthedocs.io/)\n\nThe package is built on [pytorch-lightning](https://pytorch-lightning.readthedocs.io/) to allow training on CPUs,\nsingle and multiple GPUs out-of-the-box.\n\n# Installation\n\nIf you are working on windows, you need to first install PyTorch with\n\n`pip install torch -f https://download.pytorch.org/whl/torch_stable.html`.\n\nOtherwise, you can proceed with\n\n`pip install pytorch-forecasting`\n\nAlternatively, you can install the package via conda\n\n`conda install pytorch-forecasting pytorch -c pytorch>=1.7 -c conda-forge`\n\nPyTorch Forecasting is now installed from the conda-forge channel while PyTorch is install from the pytorch channel.\n\n# Documentation\n\nVisit [https://pytorch-forecasting.readthedocs.io](https://pytorch-forecasting.readthedocs.io) to read the\ndocumentation with detailed tutorials.\n\n# Available models\n\n- [Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting](https://arxiv.org/pdf/1912.09363.pdf)\n  which outperforms DeepAR by Amazon by 36-69% in benchmarks\n- [N-BEATS: Neural basis expansion analysis for interpretable time series forecasting](http://arxiv.org/abs/1905.10437)\n  which has (if used as ensemble) outperformed all other methods including ensembles of traditional statical\n  methods in the M4 competition. The M4 competition is arguably the most important benchmark for univariate time series forecasting.\n- [DeepAR: Probabilistic forecasting with autoregressive recurrent networks](https://www.sciencedirect.com/science/article/pii/S0169207019301888)\n  which is the one of the most popular forecasting algorithms and is often used as a baseline\n- A baseline model that always predicts the latest known value\n- Simple standard networks for baselining: LSTM and GRU networks as well as a MLP on the decoder\n\nTo implement new models, see the [How to implement new models tutorial](https://pytorch-forecasting.readthedocs.io/en/latest/tutorials/building.html).\nIt covers basic as well as advanced architectures.\n\n# Usage\n\n```python\nimport pytorch_lightning as pl\nfrom pytorch_lightning.callbacks import EarlyStopping, LearningRateMonitor\nfrom pytorch_forecasting.metrics import QuantileLoss\nfrom pytorch_forecasting import TimeSeriesDataSet, TemporalFusionTransformer\n\n# load data\ndata = ...\n\n# define dataset\nmax_encoder_length = 36\nmax_prediction_length = 6\ntraining_cutoff = "YYYY-MM-DD"  # day for cutoff\n\ntraining = TimeSeriesDataSet(\n    data[lambda x: x.date <= training_cutoff],\n    time_idx= ...,\n    target= ...,\n    group_ids=[ ... ],\n    max_encoder_length=max_encoder_length,\n    max_prediction_length=max_prediction_length,\n    static_categoricals=[ ... ],\n    static_reals=[ ... ],\n    time_varying_known_categoricals=[ ... ],\n    time_varying_known_reals=[ ... ],\n    time_varying_unknown_categoricals=[ ... ],\n    time_varying_unknown_reals=[ ... ],\n)\n\n\nvalidation = TimeSeriesDataSet.from_dataset(training, data, min_prediction_idx=training.index.time.max() + 1, stop_randomization=True)\nbatch_size = 128\ntrain_dataloader = training.to_dataloader(train=True, batch_size=batch_size, num_workers=2)\nval_dataloader = validation.to_dataloader(train=False, batch_size=batch_size, num_workers=2)\n\n\nearly_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=1, verbose=False, mode="min")\nlr_logger = LearningRateMonitor()\ntrainer = pl.Trainer(\n    max_epochs=100,\n    gpus=0,\n    gradient_clip_val=0.1,\n    limit_train_batches=30,\n    callbacks=[lr_logger, early_stop_callback],\n)\n\n\ntft = TemporalFusionTransformer.from_dataset(\n    training,\n    learning_rate=0.03,\n    hidden_size=32,\n    attention_head_size=1,\n    dropout=0.1,\n    hidden_continuous_size=16,\n    output_size=7,\n    loss=QuantileLoss(),\n    log_interval=2,\n    reduce_on_plateau_patience=4\n)\nprint(f"Number of parameters in network: {tft.size()/1e3:.1f}k")\n\n# find optimal learning rate\nres = trainer.lr_find(\n    tft, train_dataloader=train_dataloader, val_dataloaders=val_dataloader, early_stop_threshold=1000.0, max_lr=0.3,\n)\n\nprint(f"suggested learning rate: {res.suggestion()}")\nfig = res.plot(show=True, suggest=True)\nfig.show()\n\ntrainer.fit(\n    tft, train_dataloader=train_dataloader, val_dataloaders=val_dataloader,\n)\n```\n',
    'author': 'Jan Beitner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pytorch-forecasting.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
