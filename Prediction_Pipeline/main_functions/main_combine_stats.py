import glob
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


def combine_stats(date):
    """Combine_stats goes through both Object Materials and Relabel_Object Materials folders to find all the csv files.
    It is then combined into a pandas dataframe and plotted.

    Args:
        date (string): date is taken from the main_gui.py 
    """
    csv_paths = []
    print(os.getcwd())
    for f in glob.glob("../predictions*/Object Materials/*.csv"):
        csv_paths.append(f)
    for f in glob.glob("../predictions*/relabel_Object Materials/*.csv"):
        csv_paths.append(f)

    grab_headers = pd.read_csv(csv_paths[0]).columns.tolist()
    df = pd.DataFrame(columns=grab_headers)
    for csv in csv_paths:
        new_data = pd.read_csv(csv)
        df = df.append(new_data, ignore_index=True)
    grab_headers[0] = "date"
    df.columns = grab_headers
    df = df.set_index("date") 

    #Save CSV to Project Root File
    df.to_csv(f"../{date}.csv")

    csv_all = glob.glob("../*.csv")
    df_all = pd.read_csv(csv_all[0])
    df_all = df_all.set_index('date')
    df_plot = df_all.sum(axis = 0, skipna = True)
    
    plt.rcParams["figure.figsize"] = [12, 15]

    df_plot.plot(kind="bar")
    plt.title(f"{date} Stats",fontsize=24);
    plt.ylabel("Count");

    df_plot.values
    xs = np.arange(0,len(df_plot.values),1)
    for x, y in zip(xs,df_plot):
        y_ = y+0.2
        x = x-0.3
        plt.text(x,y_,f"{int(y)}")
    plt.tight_layout()
    plt.show()