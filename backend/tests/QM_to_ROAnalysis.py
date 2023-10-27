import numpy as np

import os
import sys
import pathlib

# print(pathlib.Path(__file__).parent.resolve())
new_path = str(pathlib.Path(__file__).parent.resolve())
sys.path.append(new_path)
file_name = "20231014-015452_11_IQ_blobs"
data = np.load(new_path+r'/'+file_name+".npz", allow_pickle=True)

print(len(data.keys()))
for label in data.keys():
    print(f"{label} with shape {data[label].shape}")
    shot_num = data[label].shape[-1]


output_array = np.empty([2,2,shot_num])
qubit_name = "q4"
prepare_state = ["g","e"]
measurement = ["I","Q"]
for i, ps in enumerate(prepare_state):
    for j, m in enumerate(measurement):
        label = f"{m}_{ps}_{qubit_name}"
        output_array[i][j] = data[label]*1000
print(output_array.shape)

# test_data = np.empty(200000)
# print(test_data.shape)
# test_np = test_data
# test_list = test_data.tolist()

np.savez(new_path+r'/'+file_name+"_new"+".npz", output_array)
# np.savez("test_list.npz", test_list)
