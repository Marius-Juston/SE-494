# Importing Libraries 
from tkinter import *
from tkinter import messagebox

import customtkinter

from configuration import Config
from sql_connection import SQLConnection

# Save the operators that have been used before
# Last user when opening up the application again is automatically set
# Dropdown option for the operators

class main_window:
    def __init__(self, master):
        self.master = master
        inputLabel = customtkinter.CTkLabel(self.master, text="Input information", text_font=(None, 18), text_color = "#4f95c0")
        inputLabel.grid(column=1, row=0, pady = 20)

        opNameLabel = customtkinter.CTkLabel(self.master, text="Enter operator name: ")
        opNameLabel.grid(column=0, row=1, pady=10)

        # adding Entry Field
        opNameText = EntryWithPlaceholder(self.master, "Enter your name!")
        opNameText.grid(column=1, row=1, pady=10)

        sfonLabel = customtkinter.CTkLabel(self.master, text="Enter shop floor order number: ")
        sfonLabel.grid(column=0, row=2, pady=10, padx = 5)

        # adding Entry Field with event callback
        sv = StringVar()
        sv.trace("w", self.callback(sv))
        sfonReg = self.master.register(self.sfonValidation)
        sfonText = EntryWithPlaceholder(self.master, "Enter a 8-digit number!")
        sfonText.bind('<Return>', (lambda _: self.callback(sfonText)))
        sfonText.grid(column=1, row=2, pady=10)

        # adding Entry validation
        sfonText.config(validate="key", validatecommand=(sfonReg, '%P'))

        lineNumLabel = customtkinter.CTkLabel(self.master, text="Enter line number: ")
        lineNumLabel.grid(column=0, row=3, pady=10)

        # adding Entry Field
        lineNumReg = self.master.register(self.lineNumValidation)
        lineNumText = EntryWithPlaceholder(self.master, "Enter a 1-digit number!")
        lineNumText.grid(column=1, row=3, pady=10)

        # adding Entry validation
        lineNumText.config(validate="key", validatecommand=(lineNumReg, '%P'))

        # button widget 
        saveButton = customtkinter.CTkButton(self.master, text="Save Information", command=self.clicked(sfonText.get(), lineNumText.get(), opNameText.get()))
        # Set Button Grid
        saveButton.grid(column=0, row=4, pady=15)

        measurementLabel = customtkinter.CTkLabel(self.master, text="Measurement output from the Keyence sensor", text_font=(None, 18), text_color = "#4f95c0")
        measurementLabel.grid(column=1, row=5, pady=20)

        diameterLabel = customtkinter.CTkLabel(self.master, text="Diameter")
        diameterLabel.grid(column=0, row=6, pady=10)

        diameterTextbox = customtkinter.CTkTextbox(self.master)
        diameterTextbox.grid(row=7, column=0, padx=15)

        frequencyLabel = customtkinter.CTkLabel(self.master, text="Frequency")
        frequencyLabel.grid(column=1, row=6, pady=10)

        frequncyTextbox = customtkinter.CTkTextbox(self.master)
        frequncyTextbox.grid(row=7, column=1)

        ampLabel = customtkinter.CTkLabel(self.master, text="Amplitude")
        ampLabel.grid(column=2, row=6, pady=10)

        ampTextbox = customtkinter.CTkTextbox(self.master)
        ampTextbox.grid(row=7, column=2)

        # button widget 
        vizButton = customtkinter.CTkButton(self.master, text="Data visualization", width=200)
        # Set Button Grid
        vizButton.grid(column=1, row=8, pady=25)
    
    def callback(self, sfonText):
        if sfonText.get().isdigit() and len(sfonText.get()) == 8:
            print(sfonText.get())
            #SQLConnection.collect_previous_data(sfonText.get())
            
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
    
    # function to display user text when
    # button is clicked
    def clicked(self, sfonText,lineNumText, opNameText):
        config = Config()
        #sql = SQLConnection(config)
        #sql.insert_data(int(sfonText), int(lineNumText), opNameText,
                        #[i for i in range(22)],
                        #[i for i in range(22)],
                        #[i for i in range(22)])
    
                        

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

        
def main(): 
    # create CTk window 
    root = customtkinter.CTk()
    root.title("User Interface")
    # Setting Widow width and Height 
    root.geometry("820x700")
    app = main_window(root)
    root.mainloop()

if __name__ == '__main__':
    main()
