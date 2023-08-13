import numpy as np
import pandas as pd
import io
from dataclasses import dataclass
from typing import List


@dataclass
class SimplexInput:
    cost_coef: List[float]
    resources_coef: List[List[float]]
    resources: List[float]
    objective: str
    num_of_products: int

    def __post_init__(self):
        if not isinstance(self.cost_coef, (list, np.ndarray)) or not all(isinstance(x, (int, float, np.integer, np.floating)) for x in self.cost_coef):
            raise TypeError("cost_coef should be a list of int or float")
        
        if not isinstance(self.resources_coef, (list, np.ndarray)) or not all(all(isinstance(x, (int, float, np.integer, np.floating)) for x in sublist) for sublist in self.resources_coef):
            raise TypeError("resources_coef should be a list of lists with int or float")
        
        if not isinstance(self.resources, (list, np.ndarray)) or not all(isinstance(x, (int, float,np.integer, np.floating)) for x in self.resources):
            raise TypeError("resources should be a list of int or float")
        
        if not isinstance(self.objective, str) or self.objective not in ['min', 'max', 'Min', 'Max']:
            raise ValueError("objective should be 'min' or 'max'")

        if not isinstance(self.num_of_products, int):
            raise TypeError("num_of_products should be an int")
        
        if not self.num_of_products == len(self.resources_coef[0]) == len(self.cost_coef):
            raise ValueError("The size of products' coefficeint and cost coefficient needs to match with number of products")
        
        if not len(self.resources_coef) == len(self.resources):
            raise ValueError('The size of parameters of limits, coefficients and characters needs to match with each other')  


# Construct the intial tableau
def Construct_initial_df(input):
    num = input.num_of_products
    num_con = len(input.resources)
    df1 = pd.DataFrame(input.resources_coef, columns=[f'X{i + 1}' for i in range(num)])

    df2_col_name = [f'X{i + 1}' for i in range(num, num + num_con)]
    df2_value = np.zeros((num_con, num_con))
    np.fill_diagonal(df2_value, val = 1)
    df2 = pd.DataFrame(df2_value, columns=df2_col_name)

    df3 = pd.DataFrame({'Sol': input.resources})
    df = pd.concat([df1, df2, df3], axis=1)

    df4_val = list(map(lambda x: -x, input.cost_coef)) + [0] * (num_con + 1)
    df4 = pd.DataFrame({col: [val] for col, val in zip(df.columns.tolist(), df4_val)})

    df = pd.concat([df, df4], axis=0)
    df.index = df2_col_name + ['z']
    return df


# Construct a simplex class
class Simplex(object):

    def __init__(self, df):
        self.df = df

    def check_valid(self, df):
        z = df.loc['z']
        return any(z.values < 0)

    def iterate(self, df):

        # set the code
        code = 1

        # Get the col need to be added
        col = df.columns.to_list()[np.argmin(df.loc['z'].values)]  # 'x2'

        # Calulcate the theta
        def cal_theta(x, y):
            return y / x if x > 0 else -float('inf')

        df['theta'] = df.apply(lambda x: cal_theta(x[col], x['Sol']), axis = 1)

        # check whether unbound exist
        if all(df['theta'].values <= 0):
            code = 2
            return df, code

        # Find the exit idx
        postive_theta = df['theta'].values[df['theta'].values > 0]
        postive_idx = df.index[df['theta'].values > 0]
        exit_idx = postive_idx.to_list()[np.argmin(postive_theta)]
        exit_val = df.loc[exit_idx, col] if df.loc[exit_idx, col] > 0 else \
            -df.loc[exit_idx, col]
        df.loc[exit_idx] = df.loc[exit_idx].div(exit_val)
        remain_idx = df.index.to_list()
        index_idx = remain_idx.index(exit_idx)
        # remain_idx.remove(exit_idx)
        for i, idx in enumerate(remain_idx):
            if i != index_idx:
                val = df.loc[idx, col]
                df.loc[idx] = (df.loc[idx] - df.loc[exit_idx].mul(val)) # if val >= 0 else (df.loc[idx] + df.loc[exit_idx].mul(val))
            else:
                pass
        remain_idx[index_idx] = col
        df.index = remain_idx
        df.drop(columns = ['theta'], inplace = True)
        return df, code

def Simplex_loop(input):
    
    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine = 'xlsxwriter')

    df = Construct_initial_df(input)
    df.to_excel(writer, sheet_name='initial tableau')

    simplex = Simplex(df)
    ite = 0
    max_iter = 2000
   

    while simplex.check_valid(df) and ite <= max_iter:

        df, code = simplex.iterate(df)
        if code == 1:
            df.to_excel(writer, sheet_name=f'{ite + 1} tableau')
            output = 'Successfully Calculated'
        else:
            output = 'The feasible is unbounded so there are no solution!'
            break

       
        ite += 1
        if ite > 2000:
           
            output = 'Warning:!!! The solution can not be found by simplex algorithm'

    writer.save()


    return output, df, buffer