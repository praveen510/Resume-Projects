import pandas as pd

def create_crosstab(data, index_col, columns_col, value_col, aggfunc=None):
    if aggfunc is None:
        crosstab = pd.crosstab(data[index_col], data[columns_col], values=None)
    else:
        if aggfunc == 'count':
            crosstab = pd.crosstab(data[index_col], data[columns_col], values=None, aggfunc='count')
        elif aggfunc == 'mean':
            crosstab = pd.crosstab(data[index_col], data[columns_col], values=data[value_col], aggfunc='mean')
        elif aggfunc == 'max':
            crosstab = pd.crosstab(data[index_col], data[columns_col], values=data[value_col], aggfunc='max')
        elif aggfunc == 'std':
            crosstab = pd.crosstab(data[index_col], data[columns_col], values=data[value_col], aggfunc='std')
        elif aggfunc == 'round_mean':
            crosstab = pd.crosstab(data[index_col], data[columns_col], values=data[value_col], aggfunc=lambda x: round(x.mean(), 2))
        elif aggfunc == 'round_max':
            crosstab = pd.crosstab(data[index_col], data[columns_col], values=data[value_col], aggfunc=lambda x: round(x.max(), 2))
        elif aggfunc == 'round_std':
            crosstab = pd.crosstab(data[index_col], data[columns_col], values=data[value_col], aggfunc=lambda x: round(x.std(), 2))
        elif aggfunc == 'corr':
            crosstab = pd.crosstab(data[index_col], data[columns_col], values=data[value_col], aggfunc=lambda x: round(x.corr(data[columns_col]), 2))
        else:
            raise ValueError("Invalid aggregation function")
    
    return crosstab
