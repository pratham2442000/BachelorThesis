# BachelorThesis
A Thesis Submitted to EEMCS Faculty Delft University of Technology, in Partial Fulfilment of the Bachelor of Computer Science and Engineering Requirements. Code for bachelor thesis. 
This is for [Research Project](https://github.com/TU-Delft-CSE/Research-Project.git) for the year 2024 Q2.


# How to run
We use a conda environment to run the code. It is running on WLS 2 with Ubuntu.

To use conda in WSL, you need to set up WSL first, then install conda in WSL. Then you can create a conda environment and install the packages required.

After that, you can run the code in the environment.

First, run the LCDB_loclised.py to get the curves required.

Afterwards, you can run exp_1.ipynb to check metrics, exp_2.ipynb to see where the LC-PFN model suffers and training_lcdb.ipynb to train the model(currently causing the trained model to not give proper results leading a straight-line at 0.8).

If you have issues with the LC-PFN, change all the `from lcpfn.lcpfn import *` to `from lcpfn import *` in the folder lcpfn.

# Additional information:

For experiment 2, you need the baseline (Last 1 and mmf4). You can get it from the LCDB Github [repo](https://github.com/fmohr/lcdb/blob/main/publications/2022-ecml/analysis/3b%20-%20analysis%20of%20curve%20fits.ipynb)
follow the instructions to get the "df_total.gz" file. Then you can run the experiment 2 notebook. If you run it with getting the baseline you will only get the MSE for LC-PFN.

Code for LC-PFN from :

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

Code for LCDB from :
https://github.com/fmohr/lcdb/
```
@inproceedings{lcdb,
  title={LCDB 1.0: An Extensive Learning Curves Database for Classification Tasks},
  author={Mohr, Felix and Viering, Tom J and Loog, Marco and van Rijn, Jan N},
  booktitle = {Machine Learning and Knowledge Discovery in Databases. Research Track - European Conference, {ECML} {PKDD} 2022, Grenoble, France, September 19-24, 2022},
  year={2022}
}
```
