#  Utility data handling, 
# - Convert parquet to csv dataframes.
# - Consolidate parquet data files. 
# - load parquet 
import sys
#import glob
import pprint
import re
import string
import time
from pathlib import Path

ROOT_PATH = Path('D:/OneDrive - Microsoft/data/20news') # /20news-bydate-train/train_clean'
import pyarrow
import pandas as pd

def cnvt2csv(path):
    'path = path to the train_clean directory'
    try:
        adf = pd.read_parquet(path)
        print(path, ': ', adf.shape)
        new_name = Path(path.parent) / Path(path.stem + '.csv')
        # create strings from txt lists
        msg_col = adf['msg']
        msg_col = msg_col.apply(flatten_msg)
        item_col = adf['item']
        item_col = item_col.apply(lambda x: Path(x).name)
        adf['msg'] = msg_col
        adf['item'] = item_col
        adf.to_csv(new_name)
    except Exception as e:
        print(f"for file {new_name} got exception {e}.")
    print('wrote ', new_name)

def flatten_msg(msg):
    'Concatenate lines to form a single string, removing punctuation.'
    # Convert array to one text string. 
    txt = ' '.join(list(msg))
    # Remove punct. 
    txt =''.join([k for k in txt if k not in string.punctuation])
    return txt

def consolidate_parquet(path):
    'Combine all parquet files into one df'
    full_df = pd.DataFrame()
    globpath =  Path(path)
    for a_file in globpath.glob('*.parquet'):
        try:
            adf = pd.read_parquet(a_file)
        except Exception as e:
            print(f"for file {a_file} got exception {e}.")
        full_df = pd.concat([full_df, adf])
    print("Full df:", full_df.shape)
    return full_df

def reload_parquet(path):
    'dont load invidual files if the entire file is there.'
    full_file = Path(path) / 'full_df.parquet'
    if Path(full_file).exists():
        print(f"Reloaded {full_file}", file=sys.stderr)
        return pd.read_parquet(full_file)
    else:
        full_df = consolidate_parquet(path)
        full_df['msg'] = full_df['msg'].apply(flatten_msg)
        full_df['item'] = full_df['item'].apply(lambda x: Path(x).name)
        full_df.to_parquet(full_file)
        return full_df

# convert tests 
def cnvt_all(P = ROOT_PATH / "test_clean"):
    for a_file in Path(P).glob('*.parquet'):
        cnvt2csv(a_file)


# cnvt_all()
