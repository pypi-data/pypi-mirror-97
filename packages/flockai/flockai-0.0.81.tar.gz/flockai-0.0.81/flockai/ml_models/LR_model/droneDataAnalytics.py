import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pickle

def loadModel(filename):
    return pickle.load(open(filename, 'rb'))
