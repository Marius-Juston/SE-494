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

df_new['USL']=diameter_USL
df_new['LSL']=diameter_LSL
df_new['NOM']=diameter_NOM

xdf = df_new.groupby("date", as_index=False).mean() 
print (xdf)
xpoints = xdf['date'].tolist()
ypoints = xdf['avg'].tolist()
plt.axhline(y=diameter_USL, color='r', linestyle='-')
plt.axhline(y=diameter_LSL, color='r', linestyle='-')
plt.xticks(rotation=20)
plt.xlabel("Date")
plt.ylabel("Diameter averages")
plt.title("Historic data visualization for diameter")
plt.plot(xpoints, ypoints)
plt.show()






    
