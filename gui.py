# Importing Libraries 
import json
import logging
import os
import time
from threading import Thread
from tkinter import *
from tkinter import messagebox

import customtkinter
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
# Save the operators that have been used before
# Last user when opening up the application again is automatically set
# Dropdown option for the operators
import numpy as np
import pandas as pd
from matplotlib import ticker

from configuration import Config
from sql_connection import SQLConnection
from udp import SensorConnection


class MainWindow:
    def __init__(self, master):
        self.config = Config()

        self.data_indices: dict = self.config.DATA_INDICES

        self.max_data_values = 0

        for d in self.data_indices.values():
            self.max_data_values = max(self.max_data_values, max(d) + 1)

        self.diameter_data = []
        self.frequency_data = []
        self.amplitude_data = []

        self.diameter_USL, self.diameter_LSL = 0, 10
        self.frequency_USL, self.frequency_LSL = 0, 10
        self.amplitude_USL, self.amplitude_LSL = 0, 10

        self.loaded = False

        self.sql = SQLConnection(self.config)
        self.sensor_connection = None

        self.sensor_connection_thread = Thread(target=self.data_communication)
        self.sensor_connection_thread.start()

        self.master = master
        inputLabel = customtkinter.CTkLabel(self.master, text="Input information", text_font=(None, 18),
                                            text_color="#4f95c0")
        inputLabel.grid(column=1, row=0, pady=20)

        opNameLabel = customtkinter.CTkLabel(self.master, text="Enter operator name: ")
        opNameLabel.grid(column=0, row=1, pady=10)

        # get existing operators
        with open('operators.json', 'r') as f:
            self.op_data = json.load(f)
        # adding Entry Field
        self.opNameCombo = customtkinter.CTkComboBox(master=self.master,
                                                     values=self.op_data['operator_names'],
                                                     width=195, fg_color="#1e1e1e", border_color="#323232",
                                                     text_color="white")
        self.opNameCombo.set(self.op_data['last_operator'])
        self.opNameCombo.grid(column=1, row=1, pady=10)

        # old entry for operator name
        # self.opNameText = EntryWithPlaceholder(self.master, "Enter your name!")
        # self.opNameText.bind('<Return>', (lambda _: self.op_callback(self.opNameText)))

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

        self.diameterTextbox = customtkinter.CTkTextbox(self.master)
        self.diameterTextbox.grid(row=7, column=0, padx=15)

        self.diameter_USL_label = customtkinter.CTkLabel(self.master, text="LSL/USL")
        self.diameter_USL_label.grid(row=8, column=0, pady=0)

        frequencyLabel = customtkinter.CTkLabel(self.master, text="Frequency")
        frequencyLabel.grid(column=1, row=6, pady=10)

        self.frequncyTextbox = customtkinter.CTkTextbox(self.master)
        self.frequncyTextbox.grid(row=7, column=1)

        self.frequency_USL_label = customtkinter.CTkLabel(self.master, text="LSL/USL")
        self.frequency_USL_label.grid(row=8, column=1, pady=0)

        ampLabel = customtkinter.CTkLabel(self.master, text="Amplitude")
        ampLabel.grid(column=2, row=6, pady=10)

        self.ampTextbox = customtkinter.CTkTextbox(self.master)
        self.ampTextbox.grid(row=7, column=2)

        self.amp_USL_label = customtkinter.CTkLabel(self.master, text="LSL/USL")
        self.amp_USL_label.grid(row=8, column=2, pady=0)

        # button widget
        self.vizButton = customtkinter.CTkButton(self.master, text="Data visualization", width=200,
                                                 command=self.command)
        # Set Button Grid

        self.vizButton.grid(column=1, row=9, pady=25)
        # self.sql = SQLConnection(self.config)

    def data_communication(self):
        connected = False

        while not connected:
            try:
                self.sensor_connection = SensorConnection(self.config, self.data_callbak)
                logging.info("Sensor connected!")
                connected = True
            except OSError as e:
                logging.error("Unable to connect to the Keyence sensor: " + e.strerror)
                logging.error("Retrying in 5 seconds")
                time.sleep(5)
                connected = False

    # USL, LSL, Mean, std. dev, quartiles
    def spec_color(self, input_data, input_textbox, LSL, USL):
        # add clear textbox
        input_textbox.textbox.delete("1.0", "end")

        input_textbox.tag_config("red", foreground="red")
        input_textbox.tag_config("green", foreground="green")
        for i in input_data:
            if LSL <= i <= USL:
                input_textbox.insert(END, str(i) + '\n', "green")
            else:
                input_textbox.insert(END, str(i) + '\n', "red")

    def test_spec_color(self, list, textbox):
        textbox.tag_config("red", foreground="red")
        textbox.tag_config("green", foreground="green")
        for i in list:
            if i % 2 == 0:
                textbox.insert(END, str(i) + '\n', "green")
            else:
                textbox.insert(END, str(i) + '\n', "red")

    def command(self):
        self.app = Graph(self.master, self.sql, self.sfonText.get(), self.config.GRAPH_HISTORY_HOURS)

    # function to validate that sfon is a 8 digit number
    def sfonValidation(self, sfonInput):
        self.loaded = False

        if sfonInput.isdigit() and len(sfonInput) <= 6:
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

    def set_usl_lsl(self, label: customtkinter.CTkLabel, lsl, usl):
        label.set_text(f"LSL/USL: [{lsl}, {usl}]")

    def sfonClicked(self):
        sfonText: str = self.sfonText.get()
        if sfonText.isdigit() and len(sfonText) >= 6:
            output = self.sql.collect_usl_lsl_data(sfonText)

            if output is not None:
                self.diameter_USL, self.diameter_LSL, \
                    self.amplitude_USL, self.amplitude_LSL, \
                    self.frequency_USL, self.frequency_LSL = output

                self.set_usl_lsl(self.diameter_USL_label, self.diameter_LSL, self.diameter_USL)
                self.set_usl_lsl(self.frequency_USL_label, self.frequency_LSL, self.frequency_USL)
                self.set_usl_lsl(self.amp_USL_label, self.amplitude_LSL, self.amplitude_USL)

                self.refresh_tables()

                self.loaded = True
            else:
                self.popup("Order number " + sfonText + " is invalid")

                self.loaded = False
        else:
            self.loaded = False
            print("error")
            self.popup("Invalid shop floor order number")

    def popup(self, msg=""):
        messagebox.showerror(title=None, message=msg)

        # function to display user text when
        # button is clicked

    def clicked(self):
        if not self.loaded:
            self.popup("Please press the Load data button before saving information")
        else:
            diameter_data = self.diameter_data[:]
            freq_data = self.frequency_data[:]
            amplitude_data = self.amplitude_data[:]

            order_number = int(self.sfonText.get())

            try:
                line_number = int(self.lineNumText.get())
            except ValueError as e:
                self.popup(f"Invalid line number: `{self.lineNumText.get()}`")
                return

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
                load_data['operator_names'] = list(set(op_list))
                json.dump(load_data, f)

            print(order_number, line_number, opNameText, diameter_data, amplitude_data, freq_data)

            self.sql.insert_data(order_number, line_number, opNameText,
                                 diameter_data,
                                 amplitude_data,
                                 freq_data)

            messagebox.showinfo(title=None, message="Inputted data to database")

    def data_callbak(self, data):
        x_temp = np.array(list(map(float, data.split(",")))) 
        x_temp[x_temp == -9999.999] = 0.0

        x_temp /= 25.4

        x = np.zeros(self.max_data_values)
        x[:x_temp.shape[0]] = x_temp

        self.diameter_data = x[self.data_indices['diameter']]
        self.frequency_data = x[self.data_indices['frequency']]
        self.amplitude_data = x[self.data_indices['amplitude']]

        self.refresh_tables()

    def refresh_tables(self):
        self.spec_color(self.diameter_data, self.diameterTextbox, self.diameter_USL, self.diameter_LSL)
        self.spec_color(self.frequency_data, self.frequncyTextbox, self.frequency_USL, self.frequency_LSL)
        self.spec_color(self.amplitude_data, self.ampTextbox, self.amplitude_USL, self.amplitude_LSL)


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
    def __init__(self, master, sql_connection: SQLConnection, order_number, time_interval=5):
        self.master = master
        self.frame = Frame(master)

        load_data = sql_connection.collect_previous_data(order_number)

        print(load_data)

        entry_names = ["Diameter", "Frequency", "Aplitude"]
        plot_names = ["Diameter", "Frequency", "Amplitude"]

        fig, axs = plt.subplots(3, figsize=(9, 7))

        for i in range(len(entry_names)):
            entry = entry_names[i]
            plot_name = plot_names[i]

            if entry in load_data:
                diameter_USL = load_data[entry]["ULS"]
                diameter_LSL = load_data[entry]["LSL"]
                diameter_NOM = load_data[entry]["NOM"]
                diameter_dates = load_data[entry]["dates"]
                diameter_avgs = load_data[entry]["avgs"]

                all_diameter_dates = []

                for key in diameter_dates:
                    all_diameter_dates.append(key)

                diameter_df = zip(all_diameter_dates, diameter_avgs)
                diameter_df_new = pd.DataFrame(diameter_df, columns=['date', 'avg'])
                diameter_df_new['num'] = all_diameter_dates
                diameter_df_new['USL'] = diameter_USL
                diameter_df_new['LSL'] = diameter_LSL
                diameter_df_new['NOM'] = diameter_NOM
                diameter_df_new = diameter_df_new.head(15)

                end_time = diameter_df_new.head(1)['date'][0]
                start_time = end_time - pd.Timedelta(hours=time_interval)

                diameter_df_new = diameter_df_new.query("date >= @start_time and date <= @end_time")

                diameter_df_new.sort_values("date")

                print(diameter_df_new)

                # For diameter
                d_xpoints = diameter_df_new['num'].tolist()
                d_ypoints = diameter_df_new['avg'].tolist()
                axs[i].axhline(y=diameter_USL, color='r', linestyle='-')
                axs[i].axhline(y=diameter_LSL, color='r', linestyle='-')
                axs[i].plot(d_xpoints, d_ypoints)
                axs[i].set_xticks(d_xpoints)

            axs[i].set_xlabel("Data points")
            axs[i].set_ylabel(f"{plot_name} measurements")
            dy = ticker.MaxNLocator(4)

            hour_locator = mdates.HourLocator(interval=1)
            quarter_hour_locator = mdates.MinuteLocator(interval=15)

            hour_formatter = mdates.DateFormatter("%d %H:%M:%S")

            # axs[i].xaxis.set_minor_locator(quarter_hour_locator)
            # axs[i].xaxis.set_major_locator(hour_locator)  # Locator for major axis only.
            axs[i].xaxis.set_major_formatter(hour_formatter)

            axs[i].yaxis.set_major_locator(dy)
            axs[i].set_title(plot_name)

        fig.autofmt_xdate()

        # Combining all the operations and display
        plt.tight_layout()
        plt.show()


def main():
    # create CTk window 
    root = customtkinter.CTk()
    root.title("User Interface")
    # Setting Widow width and Height 
    root.geometry("960x700")
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
