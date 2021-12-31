import pandas as pd
import numpy as np



### function that splits data into columns
def split_csv_data(df):
    df[['type', 'option1','option2','option3', 'option4']] = df['data'].str.split(';',n=4,expand=True)
    ## remove extra semicolons from last column
    df['option4'] = df['option4'].str.strip(';')
    ## drop the data column
    df.drop(['data'],axis=1, inplace=True)
    return df

### makes dataframe/series for each card type
def make_entry_list(df, val_type):
    # filter dataframe by type
    filtered_df = df[df['type'] == val_type]
    vals = pd.concat([filtered_df['option1'], filtered_df['option2'], filtered_df['option3'], filtered_df['option4']], ignore_index=True)
    vals.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    vals.dropna(how='any',inplace=True)
    return vals

def create_asset_lists(df, card_types):
    ### create dict of card type dataframes
    df_dict = {}
    for card_type in card_types:
        df_dict[card_type] = make_entry_list(df, card_type)
    return df_dict

def print_card_stack(df_dict):
    for card_type in df_dict:
        print('Your %s:  %s'%(card_type, df_dict[card_type].sample().to_string(index=False)))
    return 0

def print_some_cards(n, assets):
    for card_stack in range(0,n):
        print('Stack %d'%(card_stack+1))
        print_card_stack(assets)
    return


def get_card_stack(df_dict, printer=False):
    card_stack = {}
    for card_type in df_dict:
        card_stack[card_type] = df_dict[card_type].sample().to_string(index=False)
    if printer:
        for card_type in card_stack:
            print('Your %s:  %s'%(card_type, card_stack[card_type]))
    return card_stack


def get_batch_cards(n, card_set, printer=False):
    card_batch = []
    for card_stack in range(0,n):
        card_batch.append(get_card_stack(card_set))
        
    if printer:
        for card_stack in range(0,len(card_batch)):
            print('---------------')
            print('Card Stack %d'%(card_stack+1))
            print('---------------')
            for key in card_batch[card_stack].keys():
                print('Your %s: %s'%(key, card_batch[card_stack][key]))
    return card_batch

def card_set_tofile(card_batch):
    card_set = open(fr'./card_set.txt','w')
    
    for card_stack in range(0,len(card_batch)):
            card_set.writelines('---------------\n')
            card_set.writelines('Card Stack %d\n'%(card_stack+1))
            card_set.writelines('---------------\n')
            for key in card_batch[card_stack].keys():
                card_set.writelines('Your %s: %s\n'%(key, card_batch[card_stack][key]))
    card_set.close()

    return 0