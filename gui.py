# Importing Libraries 
from tkinter import * 
import customtkinter
from configuration import Config
from sql_connection import SQLConnection


# create CTk window like you do with the Tk window 
root = customtkinter.CTk()
root.title("User Interface")

# Setting Widow width and Height 
root.geometry("500x500")

opNameLabel = customtkinter.CTkLabel(root, text = "Enter operator name: ")
opNameLabel.grid(column =0, row =1, pady=10)
 
# adding Entry Field
opNameText = Entry(root, width=20)
opNameText.insert(0, "Enter your name!")
opNameText.grid(column =1, row =1, pady=10)

sfonLabel = customtkinter.CTkLabel(root, text = "Enter shop floor order number: ")
sfonLabel.grid(column =0, row =2, pady=10)

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
sfonText.grid(column =1, row =2, pady=10)

# adding Entry validation
sfonText.config(validate="key", validatecommand =(sfonReg, '%P'))


lineNumLabel = customtkinter.CTkLabel(root, text = "Enter line number: ")
lineNumLabel.grid(column =0, row =3, pady=10)
 
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
lineNumText.grid(column =1, row =3, pady=10)

# adding Entry validation
lineNumText.config(validate="key", validatecommand =(lineNumReg, '%P'))

# function to display user text when
# button is clicked
def clicked():
    config = Config()
    sql = SQLConnection(config)
    sql.insert_data(sfonText.get(), lineNumText.get(), opNameText.get(), [i for i in range(22)], [i for i in range(22)], [i for i in range(22)])
 
# button widget 
saveButton = customtkinter.CTkButton(master=root, text="Save Information", command=clicked)
# Set Button Grid
saveButton.grid(column=0, row=4, pady = 10)

# Running the app 
root.mainloop()
