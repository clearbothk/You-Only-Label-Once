import json
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np


def combine_stats(path,date):
    csv_paths = []
    for f in glob.glob(f"{path}/*.csv"):
        csv_paths.append(f)
    grab_headers = pd.read_csv(csv_paths[0]).columns.tolist()
    df = pd.DataFrame(columns=grab_headers)
    for csv in csv_paths:
        new_data = pd.read_csv(csv)
        df = df.append(new_data, ignore_index=True)
    grab_headers[0] = "date"
    df.columns = grab_headers
    df = df.set_index("date") 
    df_plot = df.sum(axis = 0, skipna = True)




    plt.rcParams["figure.figsize"] = [15, 20]
    df_plot.plot(kind="bar")
    plt.title(f"{date} Stats",fontsize=24);
    plt.ylabel("Count");

    df_plot.values
    xs = np.arange(0,len(df_plot.values),1)
    for x, y in zip(xs,df_plot):
        y_ = y+0.2
        plt.text(x,y_,f"{int(y)}")
    plt.tight_layout()
    plt.show()