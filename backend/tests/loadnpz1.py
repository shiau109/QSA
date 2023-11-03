import numpy as np

cat = np.load("test.npz")
dog = np.load("20231012-152827_06_resonator_spectroscopy_vs_amplitude.npz")
print(dog["R1"])