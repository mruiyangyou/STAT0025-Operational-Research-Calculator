import numpy as np
import pandas as pd
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import time
from itertools import cycle
from dataclasses import dataclass
from typing import List, Union
import numpy as np
from dataclasses import dataclass
from typing import List, Union
from io import BytesIO

@dataclass
class GraphicSol_Input:
    cost_coef: Union[List[Union[int, float]], np.ndarray]
    resources_coef: Union[List[List[Union[int, float]]], np.ndarray]
    resources: Union[List[Union[int, float]], np.ndarray]
    product_name: List[str]
    resource_name: List[str]
    num_of_products: int = 2

    def __post_init__(self):
        # Check if all elements in cost_coef are of type int or float
        if not isinstance(self.cost_coef, (list, np.ndarray)) or not all(isinstance(x, (int, float, np.integer, np.floating)) for x in self.cost_coef):
            raise ValueError("cost_coef needs to be a list or numpy array of integers or floats")

        # Check if all elements in resources_coef are lists of int or float
        if not isinstance(self.resources_coef, (list, np.ndarray)) or not all(all(isinstance(x, (int, float, np.integer, np.floating)) for x in sublist) for sublist in self.resources_coef):
            raise ValueError("resources_coef needs to be a list or numpy array of integers or floats")

        # Check if all elements in resources are of type int or float
        if not isinstance(self.resources, (list, np.ndarray)) or not all(isinstance(x, (int, float,np.integer, np.floating)) for x in self.resources):
            raise ValueError("resources need to be a list or numpy array of integers or floats")

        # Check if all elements in product_name are of type str
        if not all(isinstance(x, str) for x in self.product_name):
            raise ValueError("product_name needs to be a list of strings")

        # Check if all elements in resource_name are of type str
        if not all(isinstance(x, str) for x in self.resource_name):
            raise ValueError("resource_name needs to be a list of strings")

        # Check if num_of_products is equal to 2
        if self.num_of_products != 2:
            raise ValueError("num_of_products needs to be 2")
        
        if not self.num_of_products == len(self.resources_coef[0]) == len(self.cost_coef) == len(self.product_name):
            raise ValueError("The size of products' coefficeint and cost coefficient needs to match with number of products")
        
        if not len(self.resources) == len(self.resources_coef) == len(self.resource_name):
            raise ValueError('The size of parameters of limits, coefficients and characters needs to match with each other')  


class SolveGraphicSolution(object):

    def solve_lp(self, input: GraphicSol_Input):
        coef = [-1 * i for i in input.cost_coef]
        lp = linprog(c = coef, 
                    A_ub = input.resources_coef,
                    b_ub = input.resources)
        return np.round(lp.x, 3), np.round(-lp.fun, 3)
    
    def get_minmax(self, input: GraphicSol_Input):
        res = []
        x_max = 0
        y_max = 0 
        doc = []

        for j, (coef, val) in enumerate(zip(input.resources_coef, input.resources)):
            limit = []
            for i in range(len(coef)):
                if coef[i] == 0:
                    doc.append((j, 0) if i == 0 else (j, 1))
                    limit.append(0)
                else:
                    limit.append(val / coef[i])
                    if i == 0:
                        x_max = max(x_max, val / coef[i])
                    else:
                        y_max = max(y_max, val/ coef[i])
            res.append(limit)

        for row, col in doc:
            res[row][col] = x_max if col == 0 else y_max

        return x_max, y_max, res, doc

    def plot(self, input: GraphicSol_Input,
                   x_max: float, 
                   y_max: float, 
                   res : List[List[float]], 
                   doc: List[tuple],
                   x: List[float], 
                   value: float):
        plt.figure(dpi = 300)
        plt.xlim((0, x_max * (6/5)))
        plt.ylim((0, y_max * (6/5)))
        plt.xlabel(input.product_name[0])
        plt.ylabel(input.product_name[1])
        #plot result
        # linestyle = ['-', ':', '-.','--'][:len(input.resources_coef)]
        cycol = cycle('bgrcmk')

        for i, (li, name) in enumerate(zip(res, input.resource_name)):
            if (i, 0) in doc:
                plt.hlines(li[1], xmin = 0, xmax = x_max, label = name, color = next(cycol))
            elif (i, 1) in doc:
                plt.vlines(li[0], ymin = 0, ymax = y_max, label = name, color = next(cycol))
            else:
                plt.plot([li[0], 0], [0, li[1]], label = name, color = next(cycol))

        #Get the optimum point
        opt_line_coef1 = -(input.cost_coef[0]/input.cost_coef[1])
        opt_line_coef2 = (x[1] + (-opt_line_coef1 * x[0]))

        def opt_line(x):
            return opt_line_coef1 * x + opt_line_coef2

        dot = np.arange(0, x_max+10, 1/40)
        plt.plot(dot, opt_line(dot), label = f'Optimum line, v = {value}', color = next(cycol), linestyle = '--')
        plt.plot(x[0], x[1], 'go', animated = True, markersize = 6, color = 'black', label = f'Optimum points: ({x[0], x[1]})')
        plt.legend()
        plt.title('Graphic Solution')
        fig_name = time.strftime('fig_' + '%m%d_%H:%M:%S.png')
        # plt.savefig(os.path.join('app/static/imgs',
        #                     fig_name))
        return fig_name

    def create_plot(self, 
                   input: GraphicSol_Input,
                   x_max: float, 
                   y_max: float, 
                   res : List[List[float]], 
                   doc: List[tuple],
                   x: List[float], 
                   value: float):
        fig, ax = plt.subplots(dpi = 300)
        ax.set_xlim((0, x_max * (6/5)))
        ax.set_ylim((0, y_max * (6/5)))
        ax.set_xlabel(input.product_name[0])
        ax.set_ylabel(input.product_name[1])

        cycol = cycle('bgrcmk')

        for i, (li, name) in enumerate(zip(res, input.resource_name)):
            if (i, 0) in doc:
                ax.hlines(li[1], xmin = 0, xmax = x_max, label = name, color = next(cycol))
            elif (i, 1) in doc:
                ax.vlines(li[0], ymin = 0, ymax = y_max, label = name, color = next(cycol))
            else:
                ax.plot([li[0], 0], [0, li[1]], label = name, color = next(cycol))

        opt_line_coef1 = -(input.cost_coef[0]/input.cost_coef[1])
        opt_line_coef2 = (x[1] + (-opt_line_coef1 * x[0]))

        def opt_line(x):
            return opt_line_coef1 * x + opt_line_coef2

        dot = np.arange(0, x_max+10, 1/40)
        ax.plot(dot, opt_line(dot), label = f'Optimum line, v = {value}', color = next(cycol), linestyle = '--')
        ax.plot(x[0], x[1], 'go', animated = True, markersize = 6, color = 'black', label = f'Optimum points: ({x[0], x[1]})')
        ax.legend()
        ax.set_title('Graphic Solution')
        
        return fig


    def to_frame(self,input, x: List[float], value: float):
        df = pd.DataFrame({'Num of products': [{ name: v for name, v in zip(input.product_name, x)}],
                        'Value': [value]})
        df.set_index(pd.Index(['Result']), inplace=True)
        return df
    


# data = GraphicSol_Input(
#         cost_coef = [3,8],
#         resources_coef = [[2,4],[6,2],[0,1]],
#         resources = [1600,1800,350],
#         product_name = ["x1","x2"],
#         resource_name = ["l1","l2","l3"],
#         num_of_products = 2
# )

# solver = SolveGraphicSolution()
# x, value = solver.solve_lp(data)
# x_max, y_max, res, doc = solver.get_minmax(data)
# fig = solver.create_plot(
#     data,x_max, y_max, res, doc, x, value
# )
