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
<<<<<<< Updated upstream
    os.makedirs("./mergedjson",exist_ok=True)
    os.chdir(path+'/Object Materials')
    result = []
    index = []

    for f in glob.glob("*.json"):
        print(f)
        index.append(f.split(".")[0])
        with open(f, "r") as infile:
            dict_ = json.load(infile)
            result.append(dict_)
    os.chdir(path)
    with open(f"./mergedjson/{date}_{time}_merged_file.json", "w") as outfile:
        json.dump(result, outfile)

    with open(f"./mergedjson/{date}_{time}_merged_file.json") as f:
        data = json.load(f)

        
=======

    with open(f"./Object Materials/stats.json") as f:
        data = json.load(f)
          
>>>>>>> Stashed changes
    d = {}

    for json in data:
        for object_ in json.keys():
            for i in json[object_]:
                key = object_ +"_"+ i
                value = len(json[object_][i])
                d.setdefault(key, []).append(value)

    df = pd.DataFrame(d, index=index)
<<<<<<< Updated upstream
    df.to_csv(f'Object Materials/{date}_{time}_stats.csv')

=======
    df.to_csv(f'Object Materials/stats.csv')
>>>>>>> Stashed changes

    sns.barplot(data=df, color="blue")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

