from random_cluster_generator import *
import os
import sys
import pathlib

# print(pathlib.Path(__file__).parent.resolve())
new_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(new_path))

from src.single_shot.distribution_model import *

pos = np.array([[0,0], [0,1]])
training_ratio = [0.5,0.5]
test_ratio = [0.2,0.8]


noise = 0.02
total_points = 1000
training_data = get_sim_data( pos, training_ratio, noise, total_points )    
test_data = get_sim_data( pos, test_ratio, noise, total_points )  
print(training_data.shape)

my_model = GMM_model()
my_model.training(training_data.transpose())
my_model.predict_data(test_data.transpose())

print(my_model.get_label())

