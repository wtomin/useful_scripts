import os
import pandas as pd
import numpy as np

"""
make_dict_label: a dictionary with [partition]:[sample_name]:[label_1], [label_2]...
"""
def load_pickle(pickle_file):
    try:
        with open(pickle_file, 'rb') as f:
            pickle_data = pickle.load(f)
    except UnicodeDecodeError as e:
        with open(pickle_file, 'rb') as f:
            pickle_data = pickle.load(f, encoding='latin1')
    except Exception as e:
        print('Unable to load data ', pickle_file, ':', e)
        raise
    return pickle_data

def dump_pickle(object_local, pickle_file):
    with open(pickle_file, 'wb') as handle:
        pickle.dump(object_local, handle, protocol=pickle.HIGHEST_PROTOCOL)

def read_csv(csv):
    if os.path.exists(csv):
        df = pd.read_csv(csv, skipinitialspace=True, sep="\s+|;|:|,",engine="python")
        return df
    else:
        print("No such file exists, skip : ", csv)    
        return None
        
def make_dict_label(train_csv, dict_file_path = None, partition_col=None, vd_name_col =None, utr_name_col = None, label_name_list = [], \
                     is_partitioned= True, is_utterance=False):
    """ Make a dictionary with [partition]:[sample_name]:[label_1], [label_2]...
    Args:
        train_csv: a csv file which specifys the video name (utterance name if applicable), labels, parititions
        dict_file_path: a file path for saving samples and labels
        partition_col: column name of partition, e.g., train, dev, val
        vd_name_col: column of video name
        label_name_list: a list of names of labels, e.g., emotion, age
        is_partitioned: whether the dataset has been partitioned already
        is_utterance: whether the video is subdivided into utterances
    """
    data = pd.read_csv(train_csv, skipinitialspace=True, sep="\s+|;|:|,",engine="python")
    dictionary = {}
    if is_partitioned:
        p_df = data[partition_col]
        partitions = list(np.unique(p_df))
        for partition in partitions:
            dictionary[partition] = {}
            part_df = data[data[partition_col]==partition]
            if is_utterance:
                for index, row in part_df.iterrows():
                    vd_name = row[vd_name_col]
                    utr_name = row[utr_name_col]
                    if vd_name not in dictionary[partition].keys():
                        dictionary[partition][vd_name] = {}
                    dictionary[partition][vd_name][utr_name] = {}
                    for label_name in label_name_list:
                        dictionary[partition][vd_name][utr_name][label_name] = row[label_name]
            else:
                #if no utterance exists
                for index, row in part_df.iterrows():
                    vd_name = row[vd_name_col]
                    dictionary[partition][vd_name] = {}
                    for label_name in label_name_list:
                        dictionary[partition][vd_name][label_name] = row[label_name]
    else:
        #if orginal video dataset has not been paritioned
        if is_utterance:
            for index, row in data.iterrows():
                vd_name = row[vd_name_col]
                utr_name = row[utr_name_col]
                if vd_name not in dictionary.keys():
                    dictionary[vd_name] = {}
                dictionary[vd_name][utr_name] = {}
                for label_name in label_name_list:
                    dictionary[vd_name][utr_name][label_name] = row[label_name]
        else:
            #if no utterance exists
            for index, row in data.iterrows():
                vd_name = row[vd_name_col]
                dictionary[vd_name] = {}
                for label_name in label_name_list:
                    dictionary[vd_name][label_name] = row[label_name]
    dump_pickle(dictionary, dict_file_path)
    print("Dictionary saved in :" + dict_file_path)
    return dictionary
