import numpy as np

import os
import sys
import pathlib

# print(pathlib.Path(__file__).parent.resolve())
new_path = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(new_path))
data = np.load(str(new_path)+r'\20231014-015452_11_IQ_blobs.npz', allow_pickle=True)

print(len(data.keys()))
for label in data.keys():
    print(f"{label} with shape {data[label].shape}")

# print(type(data["Qi_dia_corr"]))

# test_data = np.empty(200000)
# print(test_data.shape)
# test_np = test_data
# test_list = test_data.tolist()

# np.savez("test_np.npz", test_np)
# np.savez("test_list.npz", test_list)
