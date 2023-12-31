import numpy as np
import pandas as pd
from orCal.Simplex import Simplex
from dataclasses import dataclass
from typing import List
import io

@dataclass
class BigMInput:
    cost_coef: List[float]
    resources_coef: List[List[float]]
    resources: List[float]
    objective: str
    num_of_products: int
    constraint_char: List[List[str]]
    
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
        
        if not isinstance(self.constraint_char, (list, np.ndarray)) or not all(isinstance(x, (str, np.str_)) for x in self.constraint_char):
            raise TypeError("contraint_characters should be a list of string")

        if not self.num_of_products == len(self.resources_coef[0]) == len(self.cost_coef):
            raise ValueError("The size of products' coefficeint and cost coefficient needs to match with number of products")
        
        if not len(self.resources) == len(self.resources_coef) == len(self.constraint_char):
            raise ValueError('The size of parameters of limits, coefficients and characters needs to match with each other')  

def Cal_Artificial(input):
        artificial = {}
        artificial_idx = 1
        help = {}
        help_idx = input.num_of_products + 1
        for j, char in enumerate(input.constraint_char):
            if char not in ['<=','<']:
                artificial[j] = f'Y{artificial_idx}'
                artificial_idx += 1
            help[j] = f'X{help_idx}'
            help_idx += 1
        return artificial, help

def construct_bigM_df(input, artifical, help):
    # artifical, help = self.Cal_Artificial(input)
    num = input.num_of_products
    num_con = len(input.resources)
    df1 = pd.DataFrame(input.resources_coef, columns=[f'X{i + 1}' for i in range(num)])

    df2_col_name = [f'X{i + 1}' for i in range(num, num + num_con)]
    df2_value = np.zeros((num_con, num_con))
    np.fill_diagonal(df2_value, val = 1)
    df2 = pd.DataFrame(df2_value, columns=df2_col_name)
    for idx in artifical.keys():
        df2.loc[idx, help[idx]] = -1

    df3_col_name = list(artifical.values())
    df3_value = { col: [0] * num_con  for col in df3_col_name }
    df3 = pd.DataFrame(df3_value, columns=df3_col_name)
    for idx, j in artifical.items():
        df3.loc[idx, j] = 1

    df4 = pd.DataFrame({'Sol': input.resources})
    df = pd.concat([df1, df2, df3, df4], axis=1)

    df4_val = list(map(lambda x: -x, input.cost_coef)) + [0] * (num_con + 1 + len(artifical))
    df4 = pd.DataFrame({col: [val] for col, val in zip(df.columns.tolist(), df4_val)})
    df4[df3_col_name] = float('inf')

    df = pd.concat([df, df4], axis=0)
    df_col_name = [artifical[idx] if idx in artifical.keys() else col for idx, col in help.items()] + ['z']
    df.index = df_col_name
    return df

class Big_M(object):
    
    def __init__(self, cost_coef, resources_coef, resources, objective,
                    num_of_products, constraint_char) -> None:
        
        self.cost_coef = cost_coef
        self.resources_coef = resources_coef
        self.resources = resources
        self.objective = objective
        self.num_of_products = num_of_products
        self.constraint_char = constraint_char
    
class BigM_Simplex(Simplex):

    def __init__(self, df):
        super().__init__(df)
        self.df = df
    

    def iterate(self, df):
         # set the code
        code = 1

        # Get the col need to be added
        if not self.check_valid(df):
            z = df.loc['z'].values
            col = df.columns[z > 0].to_list()[np.argmin(z[z > 0])]
        else:
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

def check_index(df, artificial):
    
    artificial_list = artificial.values()
    return any([i in df.index.to_list() for i in artificial_list])

def BigM_loop(input):
    
    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine = 'xlsxwriter')
    artificial, help = Cal_Artificial(input)
    df = construct_bigM_df(input, artificial, help)
    bigM = BigM_Simplex(df)
    df.to_excel(writer, sheet_name='initial tableau')

    
    ite = 0
    max_iter = 2000
   

    while (bigM.check_valid(df) or check_index(df,artificial)) and max_iter <= 2000:

        df, code = bigM.iterate(df)
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



     


 
        