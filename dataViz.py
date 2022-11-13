import json
import matplotlib.pyplot as plt
import pandas as pd  


diameter_dates = []
diameter_avgs = []
with open("example_data.json") as f:
    load_data = json.load(f)
    diameter_USL = load_data["Diameter"]["ULS"]
    diameter_LSL = load_data["Diameter"]["LSL"]
    diameter_NOM = load_data["Diameter"]["NOM"]
    diameter_dates = load_data["Diameter"]["dates"]
    diameter_avgs = load_data["Diameter"]["avgs"]


all_dates = []

for key in diameter_dates:
    all_dates.append(key.split('T')[0])

df = zip(all_dates, diameter_avgs)
df_new = pd.DataFrame(df, columns=('date', 'avg'))
df_new['num'] = df_new.reset_index().index + 1
df_new['USL']=diameter_USL
df_new['LSL']=diameter_LSL
df_new['NOM']=diameter_NOM
df_new = df_new.head(15)
print (df_new)
xpoints = df_new['num'].tolist()
ypoints = df_new['avg'].tolist()
plt.axhline(y=diameter_USL, color='r', linestyle='-')
plt.axhline(y=diameter_LSL, color='r', linestyle='-')
plt.xlabel("Data point")
plt.ylabel("Diameter")
plt.title("Historic data visualization for diameter")
plt.plot(xpoints, ypoints)
plt.xticks(xpoints)
plt.show()






    
