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
my_model.import_trainingData(training_data.transpose())
label = my_model.get_prediction(test_data.transpose())+1

plot_data_dict = {
    "I": test_data[0],
    "Q": test_data[1],
    "label":label#.tobytes()
}
import plotly.express as px
from pandas import DataFrame
df = DataFrame(plot_data_dict)
print(df.dtypes)

df["label"] = df["label"].astype(str)
# df["label"]
# color_discrete_map = {
#     "1": 'blue', 
#     "2": 'red'
#     }
# for k in color_discrete_map.keys():
#     print(df["label"].values[0] == k)
# print(df["label"].values[0])
# print(df["label"].values[1])

print(color_discrete_map[df["label"].values[0]])
fig = px.scatter(df, x="I", y="Q",  color="label", color_discrete_sequence=["blue","red"])
fig.show()