import numpy as np
import pandas as pd

class Helpers():
    
    @staticmethod
    def docs():
        print('Scikit learn RF hyperparameters')
        print(' - https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html')
        print('\n')

        print('XGBoost classifier hyperparameters')
        print(' - https://xgboost.readthedocs.io/en/latest/parameter.html')
        print('\n')

    @staticmethod
    def calc_params(x):
        n = 1/1000000
        for i in [len(v) for k,v in x.items()]:
            n = n*i
        return n

    @staticmethod
    def grid_sklearn_RFC():
        
        grid={
            'criterion':['entropy', 'gini'],
            'max_depth':[None,2,4,6,8], 
            'max_features':['sqrt', 'log2','auto',0.95, 0.90, 0.85, 0.80, 0.75, 0.70],
            'max_leaf_nodes':[None,10, 15, 20, 25, 30, 35, 40, 45, 50],
            'max_samples':[0.5, 0.6, 0.7, 0.8, 0.9, None],
            'min_impurity_decrease':[0.0, 0.0005, 0.005, 0.05, 0.10, 0.15, 0.2],
            'min_samples_leaf':[1, 0.01, 0.02, 0.03, 0.04], 
            'min_samples_split':[2, 3, 4, 5, 6, 8, 10],
            'min_weight_fraction_leaf':[0.0, 0.0025, 0.005, 0.0075, 0.01, 0.05],
            'n_estimators':[10, 40, 100]
        }

        n = Helpers.calc_params(grid)        
        print(f'Note, grid contains {np.round(n,1)} mn combinations!')
        print('Check docs for details on hyperparameters: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html')
        print('\n')

        return grid

    @staticmethod
    def grid_xgboost_XGBC(booster='gbtree'):
        
        # gbtree default
        grid = {
            'colsample_bylevel':[0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            'colsample_bynode':[0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            'colsample_bytree':[0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            'gamma':[0, 0.01, 0.05, 0.1, 0.5, 1, 2, 3],
            'learning_rate':[0.1, 0.2, 0.3, 0.4, 0.5],
            'max_depth':[1, 2, 3, 4, 5, None],
            'min_child_weight':[1, 2, 3, 4, 5],
            'n_estimators':[2, 25, 50, 75, 100],
            'num_parrallal_tree':[1,10,20],
            'subsample':[0.5, 0.6, 0.7, 0.8, 0.9, 1],
        }

        if booster == 'dart':
            grid['sample_type']=['uniform', 'weighted']
            grid['normalize_type']=['tree', 'forest']
            grid['rate_drop']=[0, 0.1, 0.2, 0.3, None]
            grid['one_drop']=[0, 1]
            grid['skip_drop']=[0, 0.25, 0.5, 0.75, None]

        elif booster == 'gblinear':
            grid = {
                'reg_alpha':[0.0,0.1,0.5,1.0],  #L1 regularization
                'reg_lambda':[0.0,0.1,0.5,1.0],  #L2 regularization
                'colsample_bylevel':[0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                'colsample_bynode':[0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                'colsample_bytree':[0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                'learning_rate':[0.1, 0.2, 0.3, 0.4, 0.5],
                'n_estimators':[2, 25, 50, 75, 100],
            }

        
        n = Helpers.calc_params(grid)   
        print(f'Note, grid contains {np.round(n,1)} mn combinations!')
        print('\n')

        return grid



    @staticmethod
    def list_transformers():
        transformers =  {
            'general':[
                ('ColSelector', 'Select column in df'),
                ('PipeMerger', 'Combine pipelines'),
                ('TypeCaster', 'Cast col to type'),
            ],
            'handle nan & outliers':[
                ('NullishToNan', 'Replace nullish vals with np.nan'),
                ('NanImputer', 'NaN to imputed value'),
                ('OutlierTrimmer', 'Trim outliers'),
            ],
            'scalers & transformers':[
                ('StdScaler', 'Standard scale feature'),
                ('MinMaxScaler', 'Min-max scale feature'),
                ('BoxCoxTransformer', 'Box-cox transform feature')
            ],
            'encoders':[
                ('OrdinalEncoder', 'Ordinal encode catcol'),
                ('OnehotEncoder', 'Onehot encode'),
            ]
        }
        print('TRANSFORMERS IN PACKAGE:\n')
        for k,v in transformers.items():
            print(f'\n{k.upper()} --->')
            for e in v:
                print(f'{e[0]}:\t\t{e[1]}')
