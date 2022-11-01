import pandas
import json
import matplotlib.pyplot as plt
import numpy as nnp
import seaborn as sns
from pyspc import *

diameter_dates = []
diameter_avgs = []
with open("example_data.json") as f:
    load_data = json.load(f)
    diameter_USL = load_data["Diameter"]["ULS"]
    diameter_LSL = load_data["Diameter"]["LSL"]
    diameter_NOM = load_data["Diameter"]["NOM"]
    diameter_dates = load_data["Diameter"]["dates"]
    diameter_avgs = load_data["Diameter"]["avgs"]


