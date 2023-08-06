import numpy as np
import pandas as pd
from joblib import Parallel
from sklearn.utils.fixes import delayed
from scipy.stats import boxcox
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion, _fit_transform_one, _transform_one
from pandas.tseries.holiday import USFederalHolidayCalendar
from datetime import datetime
from typing import List, Dict, Union

class ColSelector(BaseEstimator, TransformerMixin):
    '''
    Transformer to select feature from frame
    '''
    def __init__(self, col:Union[str,List[str]])->None:
        super().__init__()
        if type(col)==str:
            col = [col]
        self.col = col

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None):
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:
        X=X.copy()
        return X[self.col]

class TypeCaster(BaseEstimator, TransformerMixin):
    '''
    Cast col to proper type, np.nan on error
    '''
    def __init__(self, type:str, date_format:str='%Y-%m-%d')->None:
        self.type=type
        self.date_format=date_format

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None):
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:
        X=X.copy()
        for c in X.columns:
            if self.type=='numeric':
                X[c] = pd.to_numeric(X[c], errors='coerce')
            if self.type=='string':
                X[c] = X[c].astype(str)
            if self.type=='date':
                X[c] = pd.to_datetime(X[c], format=self.date_format, errors='coerce')
            return X           

class OrdinalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, mapping_dict:Dict=None):        
        self.mapping_dict=mapping_dict

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X=X.copy()
        if not self.mapping_dict:
            self.mapping_dict={}
            assert X.shape[1]==1, 'Transformer support only one column'
            columns=list(X.columns)
            for c in columns:
                self.mapping_dict[c] = {
                    e[0]:e[1] for e in zip(
                        X[c].unique(),
                        range(len(X[c].unique()))
                    )
                }
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:
        X = X.copy()
        for k in self.mapping_dict.keys():
            X[k] = X[k].map(self.mapping_dict[k])
        return X

    def inverse_transform(self, X, y=None):
        X = X.copy()
        for v in self.mapping_dict.keys():
            inverse_map = {
                v:k for k,v in self.mapping_dict[v].items()
            }
            X[v] = X[v].map(inverse_map)
        return X        
    
class NanImputer(BaseEstimator, TransformerMixin):
    def __init__(self, strategy:str='mean', fillvalue=np.nan, fillvalue_map:Dict=None):
        #super().__init__()
        self.strategy=strategy
        self.fillvalue=fillvalue
        self.fillvalue_map=fillvalue_map

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None):
        if not self.fillvalue_map:
            self.fillvalue_map={}
            for c in X.columns:
                if self.strategy == 'mean':    
                    self.fillvalue_map[c]={
                        'fill_value':X[c].mean()
                    }
                if self.strategy == 'median':    
                    self.fillvalue_map[c]={
                        'fill_value':X[c].quantile(.5)
                    }   
                if self.strategy == 'constant':
                    self.fillvalue_map[c]={
                        'fill_value':self.fillvalue
                    }                     
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X=X.copy()
        for c in X.columns:
            X[c]=X[c].replace(np.nan, self.fillvalue_map[c]['fill_value'])
        return X
    
class NullishToNan(BaseEstimator, TransformerMixin):

    NULLISH=[np.nan, 0, -999, 'missing', '?', '', ' ', '  ', '   ']
    def __init__(self, null_def:List[Union[str,int,float]]=NULLISH):
        super().__init__()
        self.null_def=null_def

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None):
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X=X.copy()
        for c in X.columns:
            X.loc[X[c].isin(self.null_def), c]=np.nan
        return X

class OutlierTrimmer(BaseEstimator, TransformerMixin):
    'replace values of outliers to either bound or np.nan'
    def __init__(self, method='to_bound', threshold_map:Dict=None):
        self.method=method
        self.threshold_map=threshold_map

    def fit(self, X, y=None):
        if not self.threshold_map:
            self.threshold_map={}
            for c in X.columns:
                p75=X[c].quantile(0.75)
                p25=X[c].quantile(0.25)
                lb = p25-1.5*(p75-p25)
                ub = p75+1.5*(p75-p25)                
                self.threshold_map[c]={
                    'lb':lb,
                    'ub':ub
                }
        return self

    def transform(self, X, y=None):
        X=X.copy()
        for c in X.columns:
            lb=self.threshold_map[c]['lb']
            ub=self.threshold_map[c]['ub']

            if self.method == 'to_bound':    
                X[c] = np.where(X[c] < lb, lb, X[c])
                X[c] = np.where(X[c] > ub, ub, X[c])
            else:
                X[c] = np.where(X[c] < lb, np.nan, X[c])
                X[c] = np.where(X[c] > ub, np.nan, X[c])
        return X

class OnehotEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.unique_value_map={}

    def format_colname(self,c):
        return c.lstrip().rstrip().lower().replace('-','_') 

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None):
        for c in X.columns:
            #self.unique_value_map[c]=[str(e) for e in X[c].unique()]
            self.unique_value_map[c]=list(np.sort(X[c].unique()))
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X = X.copy()
        for k,v in self.unique_value_map.items():
            ohe=pd.DataFrame({
                f'{k}_{self.format_colname(str(e))}':
                    np.where(X[k]==e, 1,0) for e in v
            }, index=X[k].index)
            X=pd.concat([X,ohe], axis=1)
            X.drop(k, axis=1, inplace=True)
        return X

class StdScaler(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.scaler_map={}

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:        
        for c in X.columns:
            self.scaler_map[c]={
                'mu':X[c].mean(),
                'std':X[c].std()
            }   
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X = X.copy()
        for c in X.columns:
            mu=self.scaler_map[c]['mu']
            std=self.scaler_map[c]['std']
            X[c]=(X[c]-mu)/std
        return X

class MinMaxScaler(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.scaler_map={}

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:        
        for c in X.columns:
            self.scaler_map[c]={
                'min':X[c].min(),
                'max':X[c].max()
            }   
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X = X.copy()
        for c in X.columns:
            min=self.scaler_map[c]['min']
            max=self.scaler_map[c]['max']
            X[c]=(X[c]-min)/(max-min)
        return X

class BoxCoxTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.scaler_map={}

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:        
        for c in X.columns:
            _,l=boxcox(X[c])
            self.scaler_map[c]={
                'lambda':l
            }   
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X = X.copy() 
        for c in X.columns:    
            l=self.scaler_map[c]['lambda']
            X[c]=boxcox(X[c],l)
        return X


class DaylightHoursTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, earth_axis=23.44, latitude=59.83644689):
        super().__init__()
        self.earth_axis=earth_axis
        self.latitude=latitude

    def daylight_hrs(self,dt_srs):
        
        lat_rad=np.tan(np.radians(self.latitude))
        
        cos_days=np.cos((dt_srs-datetime(2000,1,1)).dt.days * 2 *np.pi / 365.25)
        long_rad=np.tan(np.radians(self.earth_axis)*cos_days)
        
        dd = 1.-long_rad*lat_rad
        hrs=24. * np.degrees(np.arccos(1 - np.clip(dd, 0, 2))) / 180.
        
        return hrs


    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()
        for c in X.columns:
            
            # Calculate dayhours
            X[f'{c}_daylight_hrs']=self.daylight_hrs(X[c])
            X.pop(c)
            
            
        return X
    
    
class DayOfWeekTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.weekday_map={
                0:'Mon', 
                1:'Tue', 
                2:'Wed', 
                3:'Thu', 
                4:'Fri', 
                5:'Sat', 
                6:'Sun'
            }

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()
        for c in X.columns:
            X[f'{c}_weekday']=X[c].dt.weekday.map(self.weekday_map)
            X.pop(c)         
            
        return X
    
class MonthNumberTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()
        for c in X.columns:
            X[f'{c}_month_no']=X[c].dt.month
            X.pop(c)         
            
        return X
    
class QuarterNumberTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()
        for c in X.columns:
            X[f'{c}_quarter']=X[c].dt.quarter
            X.pop(c)         
            
        return X
    
    
class IsHolidayTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        pass
        X = X.copy()
        
        for c in X.columns:
            mindt=X[c].min().strftime("%Y-%m-%d")
            maxdt=X[c].max().strftime("%Y-%m-%d")
            cal = USFederalHolidayCalendar()
            holiday_flags = pd.Series(1, index=cal.holidays(mindt, maxdt), name=f'{c}_holiday')

            X=X.join(holiday_flags)
            X[f'{c}_holiday'].fillna(0, inplace=True)            
            X.pop(c)
            
        return X


class PipeMerger(FeatureUnion):
    def vstack(self, Xs):
        return pd.concat(Xs, axis="columns", copy=False)

    def lolbua(self, X, y=None, **fit_params):
        for name, trans, weight in self._iter():
            print(f'name is {name}')
            print(f'trans is {trans}')
            print(f'weight is {weight}')
            print('\n\n')

    def fit_transform(self, X, y=None, **fit_params):

        self._validate_transformers()
    
        results = self._parallel_func(X, y, fit_params, _fit_transform_one)
        if not results:
            # All transformers are None
            return np.zeros((X.shape[0], 0))

        Xs, transformers = zip(*results)
        self._update_transformer_list(transformers)

        return self.vstack(Xs)
        
       #if not result:
            # All transformers are None
       #     return np.zeros((X.shape[0], 0))
       # Xs, transformers = zip(*result)
       # self._update_transformer_list(transformers)
       # return self.vstack(Xs)

    def transform(self, X):
        Xs = Parallel(n_jobs=self.n_jobs)(
            delayed(_transform_one)(trans, X, None, weight)
            for name, trans, weight in self._iter())
        if not Xs:
            # All transformers are None
            return np.zeros((X.shape[0], 0))
        Xs = self.vstack(Xs)
        return Xs