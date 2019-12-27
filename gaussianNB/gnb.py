#!/usr/bin/env python
# coding: utf-8

import os
import json
import argparse
import numpy as np
import pandas as pd
import pickle
from sklearn.utils import shuffle
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB

class DataReader():
    def __init__(self, data_dir, train_valid_file, test_file, feature_in, output_col, k_fold):
        self.data_dir = data_dir
        self.train_valid_file = os.path.join(data_dir, train_valid_file)
        self.test_file = os.path.join(data_dir, test_file)
        self.feature_in = feature_in
        self.output_col = output_col       
        self.k_fold = k_fold
        self.usecols = feature_in + [output_col]
        
    def get_train_valid_data(self, is_shuffle, split_ratio):
        train_valid_data = pd.read_excel(self.train_valid_file, usecols=self.usecols)
        ## Classification Type of t.rain_valid_data is ascending. 
        ## It will cause unbalenced data when we split it into training set and validation set without shuffling it.
        if is_shuffle:
            train_valid_data = shuffle(train_valid_data, random_state=0)
            train_valid_data.index = range(len(train_valid_data))
        
        if self.k_fold == 1:
            split_idx = int(train_valid_data.shape[0]*split_ratio)
            train_data, valid_data = train_valid_data[:split_idx], train_valid_data[split_idx:]
            train_x, train_y = train_data[self.feature_in], train_data[self.output_col]
            valid_x, valid_y = valid_data[self.feature_in], valid_data[self.output_col]
            return train_valid_data, train_data, train_x, train_y, valid_data, valid_x, valid_y 
        
        elif self.k_fold > 1:
            kf = KFold(n_splits=self.k_fold)
            return train_valid_data, kf.split(train_valid_data)
                
    def get_test_data(self):
        test_data = pd.read_excel(self.test_file, usecols=self.usecols)
        test_x, test_y = test_data[self.feature_in], test_data[self.output_col]
        return test_data, test_x, test_y

class GNB():
    def __init__(self):
        self.gnb = GaussianNB()
        
    def train(self, data_x, data_y): 
        return self.gnb.fit(data_x, data_y) 
    
    def evaluate(self, data_x, data_y):
        return self.gnb.score(data_x, data_y)
    
    def predict(self, data_x):
        return self.gnb.predict(data_x)
    
    @staticmethod
    def classification_report(y_true, y_pred):        
        ## Number of digits for formatting output floating point values. 
        # When output_dict is True, this will be ignored and the returned values will not be rounded.
        print (classification_report(y_true, y_pred, digits=4))        ## for terminal look
        return classification_report(y_true, y_pred, output_dict=True) ## for report   
        
    @staticmethod
    def confusion_matrix(y_true, y_pred, labels):
        def cm2pd(cm, labels):            
            cm_df = pd.DataFrame(index=labels)
            for idx, label in enumerate(labels):
                cm_df[f'pred_{label}'] = cm[:, idx]
            return cm_df
        cm = confusion_matrix(y_true, y_pred)
        print(cm)
        cm_df = cm2pd(cm, labels)
        return cm_df  
    
def no_k_fold(datareader, gnb, output_dir):
    
    ## data preparation
    train_valid_data, \
    train_data, train_x, train_y, \
    valid_data, valid_x, valid_y = datareader.get_train_valid_data(is_shuffle=True, split_ratio=0.8)       
    test_data, test_x, test_y = datareader.get_test_data()       
    
    ## classification
    ## train gnb
    gnb.train(train_x, train_y)
    with open(output_dir+'/gnb.pickle', 'wb') as f:
        pickle.dump(gnb, f)
    
    ## predict 
    train_y_pred = gnb.predict(train_x)
    valid_y_pred = gnb.predict(valid_x)
    test_y_pred = gnb.predict(test_x)                
        
    ## evaluate
    print ('###################')
    print ('#### train set ####')
    print ('###################')
    train_report = gnb.classification_report(train_y, train_y_pred)
    train_labels = [*train_report][:-3]
    train_report = pd.DataFrame(train_report).transpose()    
    train_cm_df  = gnb.confusion_matrix(train_y, train_y_pred, train_labels)    
    print ()
    
    print ('###################')
    print ('#### valid set ####')
    print ('###################')
    valid_report = gnb.classification_report(valid_y, valid_y_pred) 
    valid_labels = [*valid_report][:-3]
    valid_report = pd.DataFrame(valid_report).transpose()
    valid_cm_df = gnb.confusion_matrix(valid_y, valid_y_pred, valid_labels)
    print ()
    
    print ('##################')
    print ('#### test set ####')
    print ('##################')
    test_report = gnb.classification_report(test_y, test_y_pred)
    test_labels = [*test_report][:-3]
    test_report = pd.DataFrame(test_report).transpose()
    test_cm_df = gnb.confusion_matrix(test_y, test_y_pred, test_labels)
    
    ## report to excel file
    with pd.ExcelWriter(output_dir+'/result.xlsx') as writer:   
        train_data.insert(len(datareader.usecols), 'pred_Type', train_y_pred)        
        train_data.to_excel(writer, sheet_name='train_data')        
        train_report.to_excel(writer, sheet_name='train_report')
        train_cm_df.to_excel(writer, sheet_name='train_cm')
        
        valid_data.insert(len(datareader.usecols), 'pred_Type', valid_y_pred)
        valid_data.to_excel(writer, sheet_name='valid_data')
        valid_report.to_excel(writer, sheet_name='valid_report')
        valid_cm_df.to_excel(writer, sheet_name='valid_cm')
        
        test_data.insert(len(datareader.usecols), 'pred_Type', test_y_pred)
        test_data.to_excel(writer, sheet_name='test_data')
        test_report.to_excel(writer, sheet_name='test_report')
        test_cm_df.to_excel(writer, sheet_name='test_cm')

def k_fold_validation(datareader, gnb, output_dir):
    
    ## data preparation
    train_valid_data, kf = datareader.get_train_valid_data(is_shuffle=True, split_ratio=None)       
    test_data, test_x, test_y = datareader.get_test_data()
    
    result = pd.DataFrame()
    ## k-fold validation
    for i, (train_idx, valid_idx) in enumerate(kf):
        train_data, valid_data = train_valid_data.iloc[train_idx], train_valid_data.iloc[valid_idx]
        train_x, train_y = train_data[datareader.feature_in], train_data[datareader.output_col]
        valid_x, valid_y = valid_data[datareader.feature_in], valid_data[datareader.output_col]
        
        ## classification
        ## train gnb
        gnb.train(train_x, train_y)                
        
        ## evaluate
        acc_train = gnb.evaluate(train_x, train_y) 
        acc_valid = gnb.evaluate(valid_x, valid_y) 
        acc_test = gnb.evaluate(test_x, test_y) 
        
#         train_report = gnb.classification_report(train_y, train_y_pred)
#         train_report = pd.DataFrame(train_report).transpose()
#         valid_report = gnb.classification_report(valid_y, valid_y_pred) 
#         valid_report = pd.DataFrame(valid_report).transpose()
#         test_report = gnb.classification_report(test_y, test_y_pred)
#         test_report = pd.DataFrame(test_report).transpose()
#         print (f"precision: {train_report.loc['weighted avg', 'precision']}")
#         print (f"precision: {train_report.loc['weighted avg', 'recall']}")
#         print (f"precision: {train_report.loc['weighted avg', 'f1-score']}")
        
        result.loc[i, 'k_fold'] = str(i+1)
        result.loc[i, 'train'] = acc_train
        result.loc[i, 'valid'] = acc_valid
        result.loc[i, 'test'] = acc_test
    
    ## report to excel file
    result.loc[i+1, 'k_fold'] = 'avg'
    result.loc[i+1, 'train'] = np.mean(result['train'][:i+1])
    result.loc[i+1, 'valid'] = np.mean(result['valid'][:i+1])
    result.loc[i+1, 'test'] = np.mean(result['test'][:i+1])
    #print (result)
    with pd.ExcelWriter(output_dir+'/result.xlsx') as writer:           
        result.to_excel(writer, sheet_name='accuracy_report') 
    
    return result.loc[i+1,'train'], result.loc[i+1,'valid'], result.loc[i+1,'test']                

def configuration(datareader, gnb):
    config = {
        'data_dir': datareader.data_dir,
        'train_valid_file': datareader.train_valid_file,
        'test_file': datareader.test_file,
        'feature_input': datareader.feature_in,
        'output_column': datareader.output_col,
        'is_shuffle': True,
        'k_fold': datareader.k_fold}        
    
    return config

def main():
    #--- parser setting ---#
    parser = argparse.ArgumentParser(description='run sklearn/gnb for classification.')
    
    ## data setting
    parser.add_argument('--data_dir',
                        type=str,
                        required=True,
                        help='location of raw data')
    
    parser.add_argument('--train_valid_file',
                        type=str,
                        required=True,
                        help='train valid file name, it must be a .xlsx file.')
    
    parser.add_argument('--test_file',
                        type=str,
                        required=True,
                        help='test file name, it must be a .xlsx file.')
    
    parser.add_argument('--output_dir',
                        type=str,
                        required=True,
                        help='location of results')
    
    parser.add_argument('--feature_in',
                        required=True,
                        nargs='+')      
    
    parser.add_argument('--output_col',
                        type=str,
                        default='Type',
                        help='output column name of data')
    
    parser.add_argument('--is_shuffle',
                        type=bool,
                        required=True,
                        help='shuffle for training set and validation set')
    
    ## use k fold validation or not
    parser.add_argument('--k_fold',
                        type=int,
                        required=True,
                        help='k=1 means no k fold validation. k>1 means k fold validation')    
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.output_dir):
        os.makedirs(args.output_dir)        
    
    if args.k_fold < 1:
        raise ValueError('k fold must equal or be greater than 1.')   
    
    if len(args.feature_in) < 1:
        raise ValueError('len of feature must equal or be greater than 1.')        
    
    datareader = DataReader(data_dir = args.data_dir,
                            train_valid_file = args.train_valid_file, 
                            test_file = args.test_file,
                            feature_in = args.feature_in,
                            output_col = args.output_col,
                            k_fold = args.k_fold)
        
    gnb = GNB()
            
    if args.k_fold == 1:                
        no_k_fold(datareader, gnb, args.output_dir)    
    elif args.k_fold > 1:
        k_fold_validation(datareader, gnb, args.output_dir)     
        
    config = configuration(datareader, gnb)
    with open(args.output_dir+'/config.json', 'w') as fout:
        json.dump(config, fout, indent = 4)
        
if __name__ == '__main__':    
    main()



