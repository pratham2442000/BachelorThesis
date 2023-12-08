# BachelorThesis
A Thesis Submitted to EEMCS Faculty Delft University of Technology, in Partial Fulfilment of the Requirements for the Bachelor of Computer Science and Engineering. Code for bachelor thesis.


# How to run
I am using a conda environment to run the code. It is running on wls 2 with ubuntu.

To use conda in wsl, you need to setup wsl fist, then install conda in wsl. Then you can create a conda environment and install the packages required.

After that, you can run the code in the environment.

First run the LCDB_loclised.py to get the train and test data.

After which you can run check_error.ipynb to check metrics or run training_lcdb.ipynb to train the model.

If you have issues with the lcpfn, change all the `from lcpfn.lcpfn import *` to `from lcpfn import *` in the folder lcpfn.


Code for LCPFN from :

https://github.com/automl/lcpfn

```
@inproceedings{
anonymous2023efficient,
title={Efficient Bayesian Learning Curve Extrapolation using Prior-Data Fitted Networks},
author={Adriaensen, Steven and Rakotoarison, Herilalaina and Müller, Samuel and Hutter, Frank},
booktitle={Thirty-seventh Conference on Neural Information Processing Systems},
year={2023},
url={https://openreview.net/forum?id=xgTV6rmH6n}
}
```