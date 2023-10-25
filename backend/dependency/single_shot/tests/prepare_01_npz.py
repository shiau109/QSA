from random_cluster_generator import *
import os
import sys
import pathlib

# print(pathlib.Path(__file__).parent.resolve())
new_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(new_path))

from src.single_shot.distribution_model import *

pos = np.array([[0,0.3], [1,0.7]])
prepare_0 = [0.95,0.05]
prepare_1 = [0.20,0.80]


noise = 0.4
total_points = 10000
preapre_0_data = get_sim_data( pos, prepare_0, noise, total_points )    
preapre_1_data = get_sim_data( pos, prepare_1, noise, total_points )  
print(preapre_0_data.shape)

import matplotlib.pyplot as plt
plt.plot(preapre_0_data[0],preapre_0_data[1],"o")
plt.show()
output_file = {
    "4.01001": np.array([preapre_0_data,preapre_1_data])
}

import os
import sys
import pathlib

# print(pathlib.Path(__file__).parent.resolve())
new_path = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(new_path))
fn = "sim_pre01.npz"
output_path = str(new_path)+r"/"+fn

np.savez(output_path,**output_file)

read_data = np.load(output_path)

# print(len(data.keys()), len(data["Qi_dia_corr"]))
for label in read_data.keys():
    print(f"{label} with shape {read_data[label].shape}")