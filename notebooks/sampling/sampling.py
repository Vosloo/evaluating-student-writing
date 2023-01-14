import pandas as pd
import numpy as np


def count_label(df, labels):
    label_count_dict = {}
    labeled_df_dict = {}
    for label in labels:
        label_df = df[df['discourse_type']==label]
        label_count_dict[label] = len(label_df)
        labeled_df_dict[label] = label_df
    return label_count_dict, labeled_df_dict

def oversampling(df, labels, amount_for_class = 1000):
    new_df = pd.DataFrame()
    label_count, labeled_df_dict = count_label(df, labels)
    print(label_count)
    for label, count in label_count.items():
        print(label)
        lb_df = labeled_df_dict[label]
        if count < amount_for_class:
            while len(lb_df) < amount_for_class:
                row = labeled_df_dict[label].sample()
                lb_df = pd.concat([lb_df, row])
        new_df = pd.concat([new_df, lb_df])
    new_df = new_df.sample(frac=1).reset_index(drop=True)
    return new_df

def undersampling(df, labels, amount_for_class = 1000):
    new_df = pd.DataFrame()
    label_count, labeled_df_dict = count_label(df, labels)
    for label, count in label_count.items():
        lb_df = pd.DataFrame()
        if count < amount_for_class:
            lb_df = labeled_df_dict[label]
            new_df = pd.concat([new_df, lb_df])
        else:
            while len(lb_df) < amount_for_class:
                row = labeled_df_dict[label].sample()
                lb_df = pd.concat([lb_df, row])
            new_df = pd.concat([new_df, lb_df])
    return new_df