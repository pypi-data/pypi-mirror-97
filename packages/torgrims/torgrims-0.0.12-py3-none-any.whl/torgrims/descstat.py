
import numpy as np
import pandas as pd
from typing import List, Dict, Union

class DescStat():

    NULLISH=[np.nan, 0, -999, 'missing', '?', '', ' ', '  ', '   ']

    @staticmethod
    def correl(df:pd.DataFrame, x:str,y:str)->float:
        try:
            return np.corrcoef(df[x],df[y])[0,1]
        except:
            return np.nan


    @staticmethod
    def catcol(df:pd.DataFrame, col:str)->pd.DataFrame:
        '''
        Generate stats for single categorical column in dataframe
        '''
        try:
            return pd.DataFrame({
                'n_obs':df[col].value_counts(),
                'freq':df[col].value_counts(normalize=True),
                'n_missing':df.groupby(col)[col].count().rsub(df.groupby(col)[col].size(), axis=0),
                'pct_tot_missing': df.groupby(col)[col].count().rsub(df.groupby(col)[col].size(), axis=0)/df.shape[0]
            }).T  
        except:
            print('Column must be categorical')

    @staticmethod
    def catcol_trgt(df:pd.DataFrame, col:str, response:str)->pd.DataFrame:
        '''
        Generate stats for single categorical column in dataframe.
        Compare with response
        '''
        try:
            return pd.DataFrame({
                'mean_trgt':df.groupby(col)[response].mean(),
                'n_obs':df[col].value_counts(),
                'freq':df[col].value_counts(normalize=True),
                'n_missing':df.groupby(col)[col].count().rsub(df.groupby(col)[col].size(), axis=0),
                'pct_tot_missing': df.groupby(col)[col].count().rsub(df.groupby(col)[col].size(), axis=0)/df.shape[0]
            }).T        
        except:
            print('Catcol must be categorical, target must be numeric')

    @staticmethod
    def numcol(df:pd.DataFrame, col:str, nullish:List=NULLISH)->pd.DataFrame:
        '''
        Generate stats for single numerical column in dataframe
        '''

        try:
            q25 = df[col].quantile(.25)
            q75 = df[col].quantile(.75)
            IQR = q75-q25
            stats_frame =  pd.DataFrame({            
                'mean':[df[col].mean()],
                'min':[df[col].min()],
                'p25':[df[col].quantile(.25)],
                'p50':[df[col].quantile(.5)],
                'p75':[df[col].quantile(.75)],
                'max':[df[col].max()],
                'skew(pos=right tail)':[df[col].skew()],
                'fisher_kurtosis(pos=thick tail)':[df[col].kurt()],
                'neg_outlier_threshold':[q25-1.5*IQR],
                'neg_outliers': [df.loc[df[col]<(q25-1.5*IQR),col].shape[0]],
                'pos_outlier_threshold':[q75+1.5*IQR],
                'pos_outliers': [df.loc[df[col]>(q75+1.5*IQR),col].shape[0]],
                'n_nan': [df[col].isin([np.nan]).sum()],
                'n_nullish': [df[col].isin(nullish).sum()],
                'pct_tot_nullish': [df[col].isin(nullish).sum()/df.shape[0]],
                'dtype':[df[col].dtype]
            }).T
            stats_frame.columns=[col]
            return stats_frame
        except:
            print('Column must be numeric')

    @staticmethod
    def numcol_trgt(df:pd.DataFrame, col:str, response:str, nullish:List=NULLISH)->pd.DataFrame:
        '''
        Generate stats for single numerical column in dataframe
        '''
        try:
            stats_frame=DescStat.numcol(df, col)
            response_frame=pd.DataFrame({
                'correl_trgt':[DescStat.correl(df, col, response)],
                'std':[df[col].std()],
            }).T
            response_frame.columns=[col]
            return pd.concat([response_frame, stats_frame], axis=0)
        except:            
            print('Both columns must be numeric')


    @staticmethod
    def df(df:pd.DataFrame, nullish:List=NULLISH, \
            trgt=None, page_num:int=None, page_size:int=4)->pd.DataFrame:
        '''
        Generate statistics for pandas dataframe
        '''
        n_pages=1
        if page_num is not None:
            cols=df.columns
            n_cols=len(cols)
            n_pages=int(np.ceil(n_cols/page_size))
            start = page_num*page_size
            df = df.iloc[:,start:start+page_size]            

        corr_series = {c:'no_trgt' for c in df.columns}
        if trgt is not None:
            corr_series = pd.Series({c:DescStat.correl(df,trgt,c) for c in df.columns})

        q75=df.quantile(.75)
        q25=df.quantile(.25)
        IQR = q75-q25
        q_names = IQR.index

        return pd.DataFrame({
            'dtype':df.dtypes,
            'mode':df.mode().iloc[0,:],
            'cardinality':df.nunique(),
            'n_nan':df.isin([np.nan]).sum(),
            'n_nullish':df.isin(nullish).sum(),
            'corr_trgt':corr_series,
            'mean':df.mean(),
            'std':df.std(),
            'kurt(pos=thick tail)':df.kurt(),
            'skew(pos=right tail)':df.skew(),    
            'min':df.min(),
            'p_05':df.quantile(.05, axis=0),
            'p_25':df.quantile(.25, axis=0),        
            'p_50':df.quantile(.50, axis=0),
            'p_75':df.quantile(.75, axis=0),
            'p_95':df.quantile(.95, axis=0),
            'max':df.max(),
            'pos_outlier_thresh':q75+1.5*IQR,
            'neg_outlier_thresh':q25-1.5*IQR,
            'pos_outlier_count':(df[q_names] > q75+1.5*IQR).sum(),                    
            'neg_outlier_count':(df[q_names] < q25-1.5*IQR).sum(), 
            'page_displayed':np.where(page_num is not None, f'{page_num}/{n_pages-1}', 'all')
        }).T

    @staticmethod
    def col(df:pd.DataFrame,col:str, trgt=None, cardinality_bound:int=6):
        
        assert type(col) == str, "Function support only one column"
        assert col != trgt, "Col and Trgt can not be same value"
        df_slicer = [col,trgt] \
            if trgt is not None else [col]
        
        print(f'\nSUMMARY OF {col}:')
        print(DescStat.df(df[df_slicer], trgt=trgt).loc[:,col].dropna())

        if df[col].nunique() <= cardinality_bound:
            if not trgt:
                print('\n',DescStat.catcol(df, col))
            else:
                print('\n',DescStat.catcol_trgt(df, col, trgt))
        else:
            print(f'\nNote, cardinality table supressed for \
                cardinality greater than {cardinality_bound}. \
                Increase threshold to print')