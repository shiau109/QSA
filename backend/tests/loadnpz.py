import numpy as np

data = np.load('backend/tests/test.npz')

print(data.keys())
print(len(data.keys()), len(data["Qi_dia_corr"]))

print(type(data["Qi_dia_corr"]))

test_data = np.empty(200000)
print(test_data.shape)
test_np = test_data
test_list = test_data.tolist()

np.savez("test_np.npz", test_np)
np.savez("test_list.npz", test_list)
