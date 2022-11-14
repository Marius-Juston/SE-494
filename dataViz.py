import json
import matplotlib.pyplot as plt
import pandas as pd  
from matplotlib import ticker

class dataVisualization: 
    def graph(self):
        diameter_dates = []
        diameter_avgs = []
        freq_dates = []
        freq_avgs = []
        amp_dates = []
        amp_avgs = []

        with open("example_data.json") as f:
            load_data = json.load(f)
            diameter_USL = load_data["Diameter"]["ULS"]
            diameter_LSL = load_data["Diameter"]["LSL"]
            diameter_NOM = load_data["Diameter"]["NOM"]
            diameter_dates = load_data["Diameter"]["dates"]
            diameter_avgs = load_data["Diameter"]["avgs"]

            freq_USL = load_data["Frequency"]["ULS"]
            freq_LSL = load_data["Frequency"]["LSL"]
            freq_NOM = load_data["Frequency"]["NOM"]
            freq_dates = load_data["Frequency"]["dates"]
            freq_avgs = load_data["Frequency"]["avgs"]

            amp_USL = load_data["Aplitude"]["ULS"]
            amp_LSL = load_data["Aplitude"]["LSL"]
            amp_NOM = load_data["Aplitude"]["NOM"]
            amp_dates = load_data["Aplitude"]["dates"]
            amp_avgs = load_data["Aplitude"]["avgs"]


        all_diameter_dates = []
        all_freq_dates = []
        all_amp_dates = []

        for key in diameter_dates:
            all_diameter_dates.append(key.split('T')[0])

        for key in freq_dates:
            all_freq_dates.append(key.split('T')[0])

        for key in amp_dates:
            all_amp_dates.append(key.split('T')[0])

        diameter_df = zip(all_diameter_dates, diameter_avgs)
        diameter_df_new = pd.DataFrame(diameter_df, columns=('date', 'avg'))
        diameter_df_new['num'] = diameter_df_new.reset_index().index + 1
        diameter_df_new['USL']=diameter_USL
        diameter_df_new['LSL']=diameter_LSL
        diameter_df_new['NOM']=diameter_NOM
        diameter_df_new = diameter_df_new.head(15)
        print (diameter_df_new)

        freq_df = zip(all_freq_dates, freq_avgs)
        freq_df_new = pd.DataFrame(freq_df, columns=('date', 'avg'))
        freq_df_new['num'] = freq_df_new.reset_index().index + 1
        freq_df_new['USL']=freq_USL
        freq_df_new['LSL']=freq_LSL
        freq_df_new['NOM']=freq_NOM
        freq_df_new = freq_df_new.head(15)
        print (freq_df_new)

        amp_df = zip(all_amp_dates, amp_avgs)
        amp_df_new = pd.DataFrame(amp_df, columns=('date', 'avg'))
        amp_df_new['num'] = amp_df_new.reset_index().index + 1
        amp_df_new['USL']=amp_USL
        amp_df_new['LSL']=amp_LSL
        amp_df_new['NOM']=amp_NOM
        amp_df_new = amp_df_new.head(15)
        print (amp_df_new)

        fig, axs = plt.subplots(3, figsize=(9, 7))

        # For diameter
        d_xpoints = diameter_df_new['num'].tolist()
        d_ypoints = diameter_df_new['avg'].tolist()
        axs[0].axhline(y=diameter_USL, color='r', linestyle='-')
        axs[0].axhline(y=diameter_LSL, color='r', linestyle='-')
        axs[0].set_xlabel("Data points")
        axs[0].set_ylabel("Diameter measurements")
        axs[0].plot(d_xpoints, d_ypoints)
        axs[0].set_xticks(d_xpoints)
        dy = ticker.MaxNLocator(4)
        axs[0].yaxis.set_major_locator(dy)
        axs[0].set_title("Diameter")

        # For frequency
        f_xpoints = freq_df_new['num'].tolist()
        f_ypoints = freq_df_new['avg'].tolist()
        axs[1].axhline(y=freq_USL, color='r', linestyle='-')
        axs[1].axhline(y=freq_LSL, color='r', linestyle='-')
        axs[1].set_xlabel("Data points")
        axs[1].set_ylabel("Frequency measurements")
        axs[1].plot(f_xpoints, f_ypoints)
        axs[1].set_xticks(f_xpoints)
        fy = ticker.MaxNLocator(4)
        axs[1].yaxis.set_major_locator(fy)
        axs[1].set_title("Frequency")

        # For amplitude
        a_xpoints = amp_df_new['num'].tolist()
        a_ypoints = amp_df_new['avg'].tolist()
        axs[2].axhline(y=amp_USL, color='r', linestyle='-')
        axs[2].axhline(y=amp_LSL, color='r', linestyle='-')
        axs[2].set_xlabel("Data points")
        axs[2].set_ylabel("Amplitude measurements")
        axs[2].plot(a_xpoints, a_ypoints)
        axs[2].set_xticks(a_xpoints)
        ay = ticker.MaxNLocator(4)
        axs[2].yaxis.set_major_locator(ay)
        axs[2].set_title("Amplitude")

        # Combining all the operations and display
        plt.tight_layout()
        plt.show()







            
