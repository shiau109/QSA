import numpy as np

import os
import sys
import pathlib

# print(pathlib.Path(__file__).parent.resolve())
current_folder_path = str(pathlib.Path(__file__).parent.resolve())
file_path = current_folder_path+r'\20231012-172907_06_resonator_spectroscopy_vs_flux.npz'
data = np.load(file_path)

# print(len(data.keys()), len(data["Qi_dia_corr"]))
for label in data.keys():
    print(f"{label} with shape {data[label].shape}")

ax_name = ["flux","F"]
qubit_idx = int(1)
y_value = 0
m_type = "A"



idata_name = "I"+str(qubit_idx)
qdata_name = "Q"+str(qubit_idx)
idata = data[idata_name]
qdata = data[qdata_name]
axis_0 = data[ax_name[0]]
axis_1 = data[ax_name[1]+str(qubit_idx)]
if y_value == None:
    y_idx = None
else:
    y_idx = np.searchsorted(axis_0,y_value)
    idata = idata.transpose()[y_idx]
    qdata = qdata.transpose()[y_idx]

    
match m_type:
    case "A":
        measurement = np.sqrt(idata**2+qdata**2)
    case "P":
        measurement = np.arctan2()
    case "I":
        measurement = idata
    case "Q":
        measurement = qdata




import plotly.graph_objects as go

if y_idx == None:
    scalar_3d_fig = go.Figure(data=go.Heatmap(
                        x=axis_0,
                        y=axis_1,
                        z=measurement))
    scalar_3d_fig.show()
else:
    line_2d_fig = go.Figure(data=go.Scatter(
                x=axis_1, y=measurement, 
                mode='lines+markers'))
    line_2d_fig.show()

