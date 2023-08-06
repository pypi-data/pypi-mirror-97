import numpy as np
import pickle
from droneDataAnalytics import loadModel

#Data Input Vector format
#["TempHighF","TempAvgF","TempLowF","HumidityHighPercent","HumidityAvgPercent","HumidityLowPercent"]

filename = '../../../simulation/controllers/mavic2dji/LinReg_model.sav'

# load the model from disk
loaded_model = loadModel(filename)

input = np.array([[74], [60], [45], [93], [75], [57]])
input = input.reshape(1, -1)
print(loaded_model.predict(input))
