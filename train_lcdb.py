import pandas as pd

import lcpfn.lcpfn as lcpfn
import numpy as np
from matplotlib import pyplot as plt
import lcdb
import torch
from scipy.interpolate import interp1d

df_train = pd.read_pickle('/mnt/c/Users/prath/PycharmProjects/rp/LCDB_localised/train_curves.pkl')
def get_validation_curve(rng:np.random):
    """Retrieve the validation curve for a given model and dataset."""
    #slect a random row from the dataframe
    row = rng.choice(len(df_train)-1)
    row = df_train.iloc[row]
    #get the openml id
    openlid = row['openmlid']
    learner = row['learner']
    anchors = row['anchors']
    means = row['means']
    std = row['std']
    return anchors, means, std, openlid, learner

# Create a function that generates a batch of samples from the LCBD dataset
def sample_from_lcbd(n:np.random, plot=False, seq_len=100):
    return sample(n, components=None, distribution=None, plot=plot)


def sample(rng:np.random,
            components,
            distribution,
            var_lnloc=-4,
            var_lnscale=1,
            range_constraint=True,
            seq_len=100,
            plot=False):

    anchors, means, std, openmlid, learner = get_validation_curve(rng=rng)

    means = np.array(means)
    #change the anchors to be between 0 and 1
    anchors = np.array(anchors)
    anchors = (anchors - np.min(anchors)) / (np.max(anchors) - np.min(anchors))
    try:
        f = interp1d(anchors, means, kind='cubic')
    except Exception as e:
        print(f"openmlid: {openmlid}, learner: {learner}")
        print(e)
        f = interp1d(anchors, means)

    x_smooth = np.linspace(min(anchors), max(anchors), seq_len)
    y_smooth = f(x_smooth)
    y_smooth = np.clip(y_smooth, 0, 1)
    y_smooth = y_smooth-0.000000001

    y_noise = rng.normal(0, std, seq_len)
    y_noise = y_smooth + y_noise
    y_noise = np.clip(y_noise, 0, 1)
    y_noise = y_noise-0.000000001

    if plot:
        plt.scatter(anchors*100, means, label='Original Points')
        plt.plot(y_smooth, "*" ,label='Interpolated Curve', color='red', alpha=0.1)
        plt.plot(y_noise,  "*", label='Interpolated noise Curve', color='blue', alpha=0.1)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.ylim(0, 1)
        plt.show()

        print("anchors", anchors.shape)
        print("means", means.shape)
        print("y_noise", y_noise.shape)
        print("y_smooth", y_smooth.shape)
        print("types:", type(y_smooth))
        print("types:", type(y_noise))


    def curve():
        return y_smooth, y_noise
    return curve


get_batch_func = lcpfn.create_get_batch_func(prior=sample_from_lcbd)

result = lcpfn.train_lcpfn(get_batch_func=get_batch_func,
                         num_borders=100)

model = result[2]
print(type(result))
torch.save(model, "/mnt/c/Users/prath/PycharmProjects/rp/model_lcdb.pt")
print(model)


