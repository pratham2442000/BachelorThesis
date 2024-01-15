import lcdb
import numpy as np
import os
import pandas as pd

a = lcdb.get_all_curves()
print(a.info())

pd.to_pickle(a, '/mnt/c/Users/prath/PycharmProjects/rp/LCDB_localised/all_curves.pkl')
# read from pickle
path = os.path.dirname(os.path.abspath(__file__))
a = pd.read_pickle(path + '/all_curves.pkl')

print(path)
print("start")

# create a dict of all pair of openmlid and learner
openmlid_learner = {}
for i in range(len(a)):
    #     i , openmlid, learner
    print('\r', i, end='')
    if a.iloc[i, 0] in openmlid_learner:
        if a.iloc[i, 1] not in openmlid_learner[a.iloc[i, 0]]:
            openmlid_learner[a.iloc[i, 0]].append(a.iloc[i, 1])
    else:
        openmlid_learner[a.iloc[i, 0]] = [a.iloc[i, 1]]

print(openmlid_learner)
# write dic to file
with open('/mnt/c/Users/prath/PycharmProjects/rp/LCDB_localised/openmlid_learner.txt', 'w') as f:
    f.write(str(openmlid_learner))
# read from file
with open('/mnt/c/Users/prath/PycharmProjects/rp/LCDB_localised/openmlid_learner.txt', 'r') as f:
    openmlid_learner = eval(f.read())

print(sum([len(i) for i in openmlid_learner.values()]))
print(a.info())


# ---------------------------------------------------------------------------------------------------


def get_curve(rng: np.random, verbose=False):
    # get a random openmlid
    openmlid = rng.choice(list(openmlid_learner.keys()))
    # get a random learner
    learner = rng.choice(openmlid_learner[openmlid])
    # # remove the openmlid and learner from the dict
    # openmlid_learner[openmlid].remove(learner)
    # # if there are no more learners for this openmlid, remove it from the dict
    # if len(openmlid_learner[openmlid]) == 0:
    #     del openmlid_learner[openmlid]
    if verbose:
        print(f"openmlid: {openmlid}, learner: {learner}")
    return get_curve_from_dataframe(get_curve_as_dataframe(openmlid, learner))


def get_curve_as_dataframe(openmlid, learner):
    df = a.copy()
    df = df[(df["openmlid"] == openmlid)]
    if len(df) == 0:
        raise Exception(f"No curves found for openmlid {openmlid}")
    df = df[(df["learner"] == learner)]
    if len(df) == 0:
        raise Exception(f"No curves found for learner {learner} on openmlid {openmlid}")
    return df


def get_curve_from_dataframe(curve_df):
    # sanity check to see that, if we know the learner, that there is only one of them
    if "learner" in curve_df.columns and len(pd.unique(curve_df["learner"])) > 1:
        raise Exception("pass only dataframes with entries for a single learner.")
    if "openmlid" in curve_df.columns and len(pd.unique(curve_df["openmlid"])) > 1:
        raise Exception("pass only dataframes with entries for a single openmlid.")

    # gather data
    anchors = sorted(list(pd.unique(curve_df["size_train"])))
    values_train = []
    values_valid = []
    values_test = []

    # extract curve
    for anchor in anchors:
        curve_df_anchor = curve_df[curve_df["size_train"] == anchor]
        values_train.append(list(curve_df_anchor["score_train"]))
        values_valid.append(list(curve_df_anchor["score_valid"]))
        values_test.append(list(curve_df_anchor["score_test"]))

    return anchors, values_train, values_valid, values_test


# for each openmlid and leaner, get an anchor, values_train, values_valid, values_test and save it for faster access
def get_all_curves():
    all_curves = []
    for openmlid in openmlid_learner.keys():
        for learner in openmlid_learner[openmlid]:
            print(f"openmlid: {openmlid}, learner: {learner}")
            anchors, values_train, values_valid, values_test = get_curve_from_dataframe(
                get_curve_as_dataframe(openmlid, learner))
            means = [np.mean(sublist) for sublist in values_valid]
            all_curves.append(
                [openmlid, learner, anchors, means, np.std([max(sublist) - min(sublist) for sublist in values_valid])])
    all_curves = pd.DataFrame(all_curves, columns=['openmlid', 'learner', 'anchors', 'means', 'std'])
    return all_curves


a = get_all_curves()
a.to_pickle('/mnt/c/Users/prath/PycharmProjects/rp/LCDB_localised/all_curves_preprocessed.pkl')

print(a.info())
print(a.head())
print(a.tail())
print(a.describe())

# ---------------------------------------------------------------------------------------------------


df = pd.read_pickle('/mnt/c/Users/prath/PycharmProjects/rp/LCDB_localised/all_curves_preprocessed.pkl')
from sklearn.model_selection import train_test_split

train, test = train_test_split(df, test_size=0.2, random_state=42)
print(train.info())
print(test.info())
# save the data
train.to_pickle('/mnt/c/Users/prath/PycharmProjects/rp/LCDB_localised/train_curves.pkl')
test.to_pickle('/mnt/c/Users/prath/PycharmProjects/rp/LCDB_localised/test_curves.pkl')
