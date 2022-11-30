# Importing Libraries 
import json
import matplotlib.pyplot as plt
import pandas as pd 
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import customtkinter
from configuration import Config
from sql_connection import SQLConnection
import matplotlib.pyplot as plt
import pandas as pd  
from matplotlib import ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from udp import SensorConnection
# Save the operators that have been used before
# Last user when opening up the application again is automatically set
# Dropdown option for the operators

class MainWindow:
    def __init__(self, master):
        self.config = Config()
    
        self.master = master
        inputLabel = customtkinter.CTkLabel(self.master, text="Input information", text_font=(None, 18),
                                            text_color="#4f95c0")
        inputLabel.grid(column=1, row=0, pady=20)

        opNameLabel = customtkinter.CTkLabel(self.master, text="Enter operator name: ")
        opNameLabel.grid(column=0, row=1, pady=10)
        
        #get existing operators
        with open('operators.json', 'r') as f:
            self.op_data = json.load(f)
        # adding Entry Field
        self.opNameCombo = customtkinter.CTkComboBox(master=self.master,
                                     values=self.op_data['operator_names'], 
                                     width = 195, fg_color="#1e1e1e", border_color = "#323232", text_color="white")
        self.opNameCombo.set(self.op_data['last_operator'])
        self.opNameCombo.grid(column=1, row=1, pady=10)

        #old entry for operator name
        #self.opNameText = EntryWithPlaceholder(self.master, "Enter your name!")
        #self.opNameText.bind('<Return>', (lambda _: self.op_callback(self.opNameText)))

        sfonLabel = customtkinter.CTkLabel(self.master, text="Enter shop floor order number: ")
        sfonLabel.grid(column=0, row=2, pady=10, padx=5)

        # adding Entry Field with event callback
        sfonReg = self.master.register(self.sfonValidation)
        self.sfonText = EntryWithPlaceholder(self.master, "Enter a 8-digit number!")
        self.sfonText.grid(column=1, row=2, pady=10)

        # adding Entry validation
        self.sfonText.config(validate="key", validatecommand=(sfonReg, '%P'))
        # Set Button
        sfonButton = customtkinter.CTkButton(self.master, text="Load data",
                                             command=self.sfonClicked)
        # Set Button Grid
        sfonButton.grid(column=2, row=2, pady=10)


        lineNumLabel = customtkinter.CTkLabel(self.master, text="Enter line number: ")
        lineNumLabel.grid(column=0, row=3, pady=10)

        # adding Entry Field
        lineNumReg = self.master.register(self.lineNumValidation)
        self.lineNumText = EntryWithPlaceholder(self.master, "Enter a 1-digit number!")
        self.lineNumText.grid(column=1, row=3, pady=10)

        # adding Entry validation
        self.lineNumText.config(validate="key", validatecommand=(lineNumReg, '%P'))

        # button widget 
        saveButton = customtkinter.CTkButton(self.master, text="Save Information",
                                             command=self.clicked)
        # Set Button Grid
        saveButton.grid(column=0, row=4, pady=15)

        measurementLabel = customtkinter.CTkLabel(self.master, text="Measurement output from the Keyence sensor",
                                                  text_font=(None, 18), text_color="#4f95c0")
        measurementLabel.grid(column=1, row=5, pady=20)

        diameterLabel = customtkinter.CTkLabel(self.master, text="Diameter")
        diameterLabel.grid(column=0, row=6, pady=10)

        sample_data = list(range(1,11))
        self.diameterTextbox = customtkinter.CTkTextbox(self.master)
        self.diameterTextbox.grid(row=7, column=0, padx=15)
        
        frequencyLabel = customtkinter.CTkLabel(self.master, text="Frequency")
        frequencyLabel.grid(column=1, row=6, pady=10)

        self.frequncyTextbox = customtkinter.CTkTextbox(self.master)
        self.frequncyTextbox.grid(row=7, column=1)

        ampLabel = customtkinter.CTkLabel(self.master, text="Amplitude")
        ampLabel.grid(column=2, row=6, pady=10)

        self.ampTextbox = customtkinter.CTkTextbox(self.master)
        self.ampTextbox.grid(row=7, column=2)

        # button widget 
        vizButton = customtkinter.CTkButton(self.master, text="Data visualization", width=200, command=self.command)
        # Set Button Grid
        vizButton.grid(column=1, row=8, pady=25)
        #self.sql = SQLConnection(self.config)

        self.sensorConfig = SensorConnection(self.config, self.data_callbak)

        #USL, LSL, Mean, std. dev, quartiles
    def spec_color(self,list,input_textbox, USL, LSL):
        #add clear textbox
        input_textbox.textbox.delete("1.0","end")

        input_textbox.tag_config("red", foreground="red")
        input_textbox.tag_config("green", foreground="green")
        for i in list:
            if LSL<=i<=USL:
                input_textbox.insert(END, str(i) + '\n', "green")
            else:
                input_textbox.insert(END, str(i) + '\n', "red")

    def test_spec_color(self,list,textbox):
        textbox.tag_config("red", foreground="red")
        textbox.tag_config("green", foreground="green")
        for i in list:
            if i%2 == 0:
                textbox.insert(END, str(i) + '\n', "green")
            else:
                textbox.insert(END, str(i) + '\n', "red")

    def command(self):
        self.app = Graph(self.master)
       

    # function to validate that sfon is a 8 digit number
    def sfonValidation(self, sfonInput):
        if sfonInput.isdigit() and len(sfonInput) <= 8:
            return True
        elif sfonInput == "":
            return True
        else:
            return False

    # function to validate that line number is a 1 digit number
    def lineNumValidation(self, sfonInput):
        if sfonInput.isdigit() and len(sfonInput) <= 1:
            return True
        elif sfonInput == "":
            return True
        else:
            return False
        
    def sfonClicked(self):
        sfonText = self.sfonText.get()
        if sfonText.isdigit() and len(sfonText) == 8:
            print(sfonText.get())
            #self.sql.collect_previous_data(sfonText.get())
        else:
            print("error")
            self.popup("Invalid shop floor order number")

    def popup(self, msg=""):
        messagebox.showerror(title=None, message=msg)

    # function to display user text when
    # button is clicked
    def clicked(self):
        sfonText = self.sfonText.get()
        lineNumText = self.lineNumText.get(),
        opNameText = self.opNameCombo.get()

        fname = "operators.json"
        op_list = []
        if os.path.exists(fname):
            with open(fname) as f:
                load_data = json.load(f)
                op_list = load_data["operator_names"]
                op_list.append(opNameText)
                load_data["last_operator"] = opNameText
                load_data["operator_names"] = op_list
        else:
            op_list.append(opNameText)
            load_data = {
                "last_operator": opNameText,
                "operator_names": op_list,
            }

        with open(fname, "w") as f:
            json.dump(load_data, f)

        print(int(sfonText), int(lineNumText), opNameText)
        # self.sql.insert_data(int(sfonText), int(lineNumText), opNameText,
        # [i for i in range(22)],
        # [i for i in range(22)],
        # [i for i in range(22)])

    def data_callbak(self,data):
        x = list(map(float, data.split(",")))
        diameter = x[:len(x)//3]
        freq = x[len(x)//3:len(x)//3*2]
        amp = x[len(x)//3*2:]
        self.spec_color(diameter, self.diameterTextbox, 0.5, 0.3)
        self.spec_color(freq, self.frequncyTextbox, 0.5, 0.3)
        self.spec_color(amp, self.ampTextbox, 0.5, 0.3)


class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

class Graph():
    def __init__(self, master):
        self.master = master
        self.frame = Frame(master)

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
        #print (diameter_df_new)

        freq_df = zip(all_freq_dates, freq_avgs)
        freq_df_new = pd.DataFrame(freq_df, columns=('date', 'avg'))
        freq_df_new['num'] = freq_df_new.reset_index().index + 1
        freq_df_new['USL']=freq_USL
        freq_df_new['LSL']=freq_LSL
        freq_df_new['NOM']=freq_NOM
        freq_df_new = freq_df_new.head(15)
        #print (freq_df_new)

        amp_df = zip(all_amp_dates, amp_avgs)
        amp_df_new = pd.DataFrame(amp_df, columns=('date', 'avg'))
        amp_df_new['num'] = amp_df_new.reset_index().index + 1
        amp_df_new['USL']=amp_USL
        amp_df_new['LSL']=amp_LSL
        amp_df_new['NOM']=amp_NOM
        amp_df_new = amp_df_new.head(15)
        #print (amp_df_new)

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


def main():
    # create CTk window 
    root = customtkinter.CTk()
    root.title("User Interface")
    # Setting Widow width and Height 
    root.geometry("820x700")
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()


