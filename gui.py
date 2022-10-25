# Importing Libraries 
from tkinter import *

import customtkinter

from configuration import Config
from sql_connection import SQLConnection

# Save the operators that have been used before
# Last user when opening up the application again is automatically set
# Dropdown option for the operators
# Class structuring

# create CTk window like you do with the Tk window 
root = customtkinter.CTk()
root.title("User Interface")
# Setting Widow width and Height 
root.geometry("820x700")

inputLabel = customtkinter.CTkLabel(root, text="Input information", text_font=(None, 18), text_color = "#4f95c0")
inputLabel.grid(column=1, row=0, pady = 20)

opNameLabel = customtkinter.CTkLabel(root, text="Enter operator name: ")
opNameLabel.grid(column=0, row=1, pady=10)

# adding Entry Field
opNameText = Entry(root, width=20)
opNameText.insert(0, "Enter your name!")
opNameText.grid(column=1, row=1, pady=10)

sfonLabel = customtkinter.CTkLabel(root, text="Enter shop floor order number: ")
sfonLabel.grid(column=0, row=2, pady=10, padx = 5)


# function to validate that sfon is a 8 digit number
def sfonValidation(sfonInput):
    if sfonInput.isdigit() and len(sfonInput) <= 8:
        return True
    elif sfonInput == "":
        return True
    else:
        return False


# adding Entry Field
sfonReg = root.register(sfonValidation)
sfonText = Entry(root, width=20)
sfonText.insert(0, "Enter a 8-digit number!")
sfonText.grid(column=1, row=2, pady=10)

# adding Entry validation
sfonText.config(validate="key", validatecommand=(sfonReg, '%P'))

lineNumLabel = customtkinter.CTkLabel(root, text="Enter line number: ")
lineNumLabel.grid(column=0, row=3, pady=10)


# function to validate that line number is a 1 digit number
def lineNumValidation(sfonInput):
    if sfonInput.isdigit() and len(sfonInput) <= 1:
        return True
    elif sfonInput == "":
        return True
    else:
        return False


# adding Entry Field
lineNumReg = root.register(lineNumValidation)
lineNumText = Entry(root, width=20)
lineNumText.insert(0, "Enter a 1-digit number!")
lineNumText.grid(column=1, row=3, pady=10)

# adding Entry validation
lineNumText.config(validate="key", validatecommand=(lineNumReg, '%P'))


# function to display user text when
# button is clicked
def clicked():
    config = Config()
    sql = SQLConnection(config)
    sql.insert_data(int(sfonText.get()), int(lineNumText.get()), opNameText.get(),
                    [i for i in range(22)],
                    [i for i in range(22)],
                    [i for i in range(22)])


# button widget 
saveButton = customtkinter.CTkButton(master=root, text="Save Information", command=clicked)
# Set Button Grid
saveButton.grid(column=0, row=4, pady=15)

measurementLabel = customtkinter.CTkLabel(root, text="Measurement output from the Keyence sensor", text_font=(None, 18), text_color = "#4f95c0")
measurementLabel.grid(column=1, row=5, pady=20)

diameterLabel = customtkinter.CTkLabel(root, text="Diameter")
diameterLabel.grid(column=0, row=6, pady=10)

diameterTextbox = customtkinter.CTkTextbox(root)
diameterTextbox.grid(row=7, column=0, padx=15)

frequencyLabel = customtkinter.CTkLabel(root, text="Frequency")
frequencyLabel.grid(column=1, row=6, pady=10)

frequncyTextbox = customtkinter.CTkTextbox(root)
frequncyTextbox.grid(row=7, column=1)

ampLabel = customtkinter.CTkLabel(root, text="Amplitude")
ampLabel.grid(column=2, row=6, pady=10)

ampTextbox = customtkinter.CTkTextbox(root)
ampTextbox.grid(row=7, column=2)

# button widget 
vizButton = customtkinter.CTkButton(master=root, text="Data visualization", command=clicked, width=200)
# Set Button Grid
vizButton.grid(column=1, row=8, pady=25)

# Running the app 
root.mainloop()
