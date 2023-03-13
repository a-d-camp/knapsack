from ortools.algorithms import pywrapknapsack_solver
import time
import pandas as pd
import os
import pickle

class knapsack_model():
    def __init__(self, data_file) -> None:
        self.data_file = data_file
        self.read_data_file()
        self.solver = self.init_solver()
        self.solve_time = None
        self.obj_val = None

    def read_data_file(self):
        # read a single data file, set weights, values and max weight
        f = self.data_file
        raw_data = pd.read_csv(f, delim_whitespace=True, header=None)
        n_items = raw_data.iloc[0,0]
        max_weight = raw_data.iloc[0,1]
        data = raw_data.tail(-1)
        data.columns = ['value', 'weight']
        v = data['value'].to_list()
        w = [data['weight'].to_list()]
        self.index_item_map = dict(zip(range(len(v)), data.index))
        self.values = v
        self.weights = w
        self.capacity = max_weight

    def init_solver(self):
        # set up solver and kp model
        solver = pywrapknapsack_solver.KnapsackSolver(
          pywrapknapsack_solver.KnapsackSolver.
          KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER, 'KnapsackExample')
        solver.Init(self.values, self.weights, [self.capacity])
        return solver

    def solve_model(self):
        # solve and record solve time
        start = time.time()
        computed_value = self.solver.Solve()
        end = time.time()
        self.solve_time = end-start
        self.obj_val = computed_value

    def parse_output(self):
        # extract metrics from output
        packed_items = []
        packed_weights = []
        packed_values = []
        all_items = []
        total_weight = 0
        for i in range(len(self.values)):
            all_items.append(i)
            if self.solver.BestSolutionContains(i):
                packed_items.append(i)
                packed_weights.append(self.weights[0][i])
                packed_values.append(self.values[i])
                total_weight += self.weights[0][i]

        packed_items = [self.index_item_map[i] for i in packed_items]
        all_items = [self.index_item_map[i] for i in all_items]
        output = {
            'n_avail_items': len(self.values),
            'capacity': self.capacity,
            'obj_val': self.obj_val,
            'total_weight': total_weight,
            'packed_items': packed_items,
            'packed_weights':packed_weights,
            'packed_values':packed_values,
            'solve_time': self.solve_time,
        }
        return output