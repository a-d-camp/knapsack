from knapsack import *
import pickle
import pandas as pd

# run all
pth = './data/knapsack-data'
files = os.listdir(pth)
# files = [files[1]]
all_outputs = {}
for f in files:
    kp_mod = knapsack_model(os.path.join(pth, f))
    kp_mod.solve_model()
    print('solving: ', f)
    all_outputs[f] = kp_mod.parse_output()

# save results
with open('./data/knapsack_output.pickle', 'wb') as handle:
    pickle.dump(all_outputs, handle, protocol=pickle.HIGHEST_PROTOCOL)

# parse outputs
file_names = all_outputs.keys()
n_items = [len(d['packed_items']) for d in all_outputs.values()]
caps = [d['capacity'] for d in all_outputs.values()]
n_avail_items = [d['n_avail_items'] for d in all_outputs.values()]
solve_times = [d['solve_time'] for d in all_outputs.values()]
obj_vals = [d['obj_val'] for d in all_outputs.values()]

df = pd.DataFrame({
    'File': file_names, 
    'Number of Available Items': n_avail_items,
    'Number of Packed Items': n_items,
    'Solve Time': solve_times,
    'Total Knapsack Value': obj_vals,
    'Capacity': caps
    })

df.to_csv('./data/knapsack_summary.csv', index_label=False)
