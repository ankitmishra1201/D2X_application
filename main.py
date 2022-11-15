from tkinter import *
from tkinter import messagebox
from functional import Database
        
def driverCode(fileName, option):
    fileName = fileName.strip()
    db = Database(fileName)
    if(option==1):
        try:
            if(db.df is None):
                raise Exception
            db.createDatabase()
        except:
            print("Table cannot be created.")
    elif(option==2):
        try:
            if(db.df is None):
                raise Exception
            db.updateDatabase()
        except:
            print("Table cannot be updated.")
    elif(option==3):
        try:
            if(db.df is None):
                raise Exception
            db.sqlToExcel()
        except:
            print("Database cannot be converted to Excel.")

def SecondWindow():
    d2x = Tk()
    d2x.geometry("1300x300")
    d2x.title("D2X Application")
    title = Label(d2x, text = "Welcome to D2X", fg = "#FFFFFF", font = ("Arial", 24))
    subtitle = Label(d2x, text = "Please select the operation:", fg = "#808080", font = ("Arial", 24))
    file_label = Label(d2x, text = "Enter Excel file name:", bg = '#333333', fg = "#FFFFFF", font = ("Arial", 16))
    file_entry = Text(d2x, font = ("Arial", 16))
    file_entry.configure(height=2)
    sqltoexcel = Button(d2x, text = "Sync to Excel file from database", bg = "#CC8899", fg = "#FFFFFF", font = ("Arial", 24), command = lambda: driverCode(file_entry.get('1.0', END), 3))
    exceltosql0 = Button(d2x, text = "Create Database from Excel file", bg = "#CC8899", fg = "#FFFFFF", font = ("Arial", 24), command = lambda: driverCode(file_entry.get('1.0', END), 1))
    exceltosql1 = Button(d2x, text = "Sync to Database from Excel file", bg = "#CC8899", fg = "#FFFFFF", font = ("Arial", 24), command = lambda: driverCode(file_entry.get('1.0', END), 2))
    warning = Label(d2x, text = "NOTE: Any operations cannot be undone!", bg = '#333333', fg = "#808080", font = ("Arial", 14))
    title.grid(row = 0, column = 1)
    subtitle.grid(row = 1, column = 1)
    file_label.grid(row = 3, column = 0)
    file_entry.grid(row = 3, column = 1, padx = 25, columnspan = 3)
    sqltoexcel.grid(row = 5, column = 2, rowspan = 2, columnspan = 1, padx = 25, pady = 25)
    exceltosql0.grid(row = 5, column = 0, rowspan = 2, columnspan = 1, padx = 25, pady = 25)
    exceltosql1.grid(row = 5, column = 1, rowspan = 2, columnspan = 1, padx = 25, pady = 25)
    warning.grid(row = 7, column = 1)

def validateLogin():
    if(username_entry.get()=="admin"and password_entry.get()=="admin"):
       SecondWindow()
       loginWindow.withdraw()
    else:
      messagebox.showerror("Login error!", "Please enter the correct credentials!")
    
loginWindow = Tk()
loginWindow.geometry('440x440')
loginWindow.title('D2X application')
frame = Frame(bg = '#333333')
login_label = Label(frame, text = "LOGIN", bg = '#333333', fg = "#FFFFFF", font = ("Arial", 30))
username_label = Label(frame, text = "Username", bg='#333333', fg="#FFFFFF", font = ("Arial", 16))
username_entry = Entry(frame, font = ("Arial", 16))
password_entry = Entry(frame, show = "*", font = ("Arial", 16))
password_label = Label(frame, text = "Password", bg = '#333333', fg = "#FFFFFF", font = ("Arial", 16))
login_button = Button(frame, text = "LOGIN", bg = "#CC8899", fg = "#FFFFFF", font = ("Arial", 24), command = validateLogin)
login_label.grid(row = 0, column = 0, columnspan = 2, pady = 40)
username_label.grid(row = 1, column = 0)
username_entry.grid(row = 1, column = 4, pady = 20)
password_label.grid(row = 2, column = 0)
password_entry.grid(row = 2, column = 4, pady = 20)
login_button.grid(row = 4, column = 4, rowspan = 4, columnspan = 2, pady = 50)
frame.pack()
loginWindow.mainloop()