import json
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


def read_stats(path):
    import json
    os.chdir(path)
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
    with open("./mergedjson/merged_file.json", "w") as outfile:
        json.dump(result, outfile)

    with open('./mergedjson/merged_file.json') as f:
        data = json.load(f)

        
    d = {}

    for json in data:
        for object_ in json.keys():
            for i in json[object_]:
                key = object_ +"_"+ i
                value = len(json[object_][i])
                d.setdefault(key, []).append(value)

    df = pd.DataFrame(d, index=index)
    df.to_csv('Object Materials/stats.csv')


    sns.barplot(data=df, color="blue")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

path = '/Users/jlee/Code-Data/Clearbot_Project/testing/2021-05-07/predictions_15_06'
read_stats(path)