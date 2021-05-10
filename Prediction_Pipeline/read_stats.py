import json
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#Not needed as main_gui runs this function and the variables are there
# from datetime import date, datetime
# date = str(date.today())
# time = datetime.now().strftime("%H_%M")

def read_stats(path, date, time):
    import json
    os.chdir(path)

    with open(f"./Object Materials/stats.json") as f:
        data = json.load(f)
    
    d = {}

    for object_ in data:
        for i in data[object_]:
            key = object_ +"_"+ i
            value = len(data[object_][i])
            d.setdefault(key, []).append(value)
    index = [f"{date}_{time}"]
    df = pd.DataFrame(d, index=index)
    df.to_csv(f'Object Materials/stats.csv')

    sns.barplot(data=df, color="blue")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
