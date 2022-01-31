import database.db as db
from tkinter import *
import fileOperations.read as reader

def userLoginOrRegistration():
    print("Welcome to HAQMate!!!")
    while True:
        print("You have following options:")
        print("To Register -> press 1")
        print("To Login -> press 2")
        choice = input("please enter your choice: ")
        if(choice == '1'):
            username = input("Enter your username(ID number): ")
            password = input("Enter your password: ")
            name = input("Enter your name: ")
            watsapp_number = input("Enter your Mobile number: ")
            regis_res = db.userRegistration(username,password,name,watsapp_number)
            print(regis_res[1])
            if regis_res[0]:
                return True
        if(choice == '2'):
            username = input("Enter your username(ID number): ")
            password = input("Enter your password: ")
            login_res = db.UserLogin(username,password)
            print(login_res[1])
            if(login_res[0]):
                return True
        else:
            print("Please select a valid choice!")


def main_account_screen():
    global main_screen
    try:
        login_screen.destroy()
    except:
        print("GENERIC ERROR")
    try:
        reg_screen.destroy()
    except:
        print("GENERIC ERROR")

    main_screen = Tk()   # create a GUI window 
    main_screen.geometry("300x250") # set the configuration of GUI window 

    main_screen.title("Account Login") # set the title of GUI window
    
    # create a Form label 
    Label(text="Welcome To HAQMAte", bg="blue",fg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack() 
    
    # create Login Button 
    Button(text="Login", height="2", width="30", command= login).pack() 
    Label(text="").pack() 
    
    # create a register button
    Button(text="Register", height="2", width="30", command=register).pack()

    main_screen.mainloop()
    

def login():
    global login_screen 
    global username
    global password
    global username_entry
    global password_entry
    global err_label
    
    # login_screen = Toplevel(main_screen) 
    main_screen.destroy()
    login_screen = Tk()
    login_screen.title("Login")
    login_screen.geometry("300x250")
    
# Set text variables
    username = StringVar()
    password = StringVar()
 
# Set label for user's instruction
    Label(login_screen, text="Please enter details below", bg="blue",fg="white").pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Home", width=10, height=1, bg="blue",fg="white",command=main_account_screen).pack()
    
# Set username label
    username_lable = Label(login_screen, text="Username(ID number)")
    username_lable.pack()
 
# Set username entry
# The Entry widget is a standard Tkinter widget used to enter or display a single line of text.
    
    username_entry = Entry(login_screen, textvariable=username)
    username_entry.pack()
   
# Set password label
    password_lable = Label(login_screen, text="Password")
    password_lable.pack()
    
# Set password entry
    password_entry = Entry(login_screen, textvariable=password, show='*')
    password_entry.pack()
    
    Label(login_screen, text="").pack()
    
# Set register button
    Button(login_screen, text="Login", width=10, height=1, bg="blue",fg="white",command= login_user).pack()
    err_label = Label(login_screen, text="", fg="red", font=("calibri", 11))
    err_label.pack()
    login_screen.mainloop()


def login_user():
    # get username and password
    username_info = username.get()
    password_info = password.get()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    login_res = db.UserLogin(username_info,password_info)
    if login_res[0]:
        err_label.config(text=login_res[1],fg="green")
        err_label.update_idletasks()
        login_screen.destroy()
        reader.select_screen()
    else:
        err_label.config(text=login_res[1],fg="red")
        err_label.update_idletasks()

def register():
    global reg_screen 
    global reg_username
    global reg_password
    global reg_name
    global reg_watsapp
    global reg_username_entry
    global reg_password_entry
    global reg_name_entry
    global reg_watsapp_entry
    global reg_err_label
    # login_screen = Toplevel(main_screen) 
    main_screen.destroy()
    reg_screen = Tk()
    reg_screen.title("Register")
    reg_screen.geometry("300x350")
    
# Set text variables
    reg_name = StringVar()
    reg_username = StringVar()
    reg_watsapp = StringVar()
    reg_password = StringVar()
 
# Set label for user's instruction
    Label(reg_screen, text="Please enter details below", bg="blue",fg="white").pack()
    Label(reg_screen, text="").pack()
    Button(reg_screen, text="Home", width=10, height=1, bg="blue",fg="white",command=main_account_screen).pack()
    
# Set username label
    username_lable = Label(reg_screen, text="ID number")
    username_lable.pack()
 
# Set username entry
# The Entry widget is a standard Tkinter widget used to enter or display a single line of text.
    
    reg_username_entry = Entry(reg_screen, textvariable=reg_username)
    reg_username_entry.pack()
   
# Set password label
    password_lable = Label(reg_screen, text="Password")
    password_lable.pack()
    
# Set password entry
    reg_password_entry = Entry(reg_screen, textvariable=reg_password, show='*')
    reg_password_entry.pack()
# Set username label
    name_label = Label(reg_screen, text="Name")
    name_label.pack()
 
# Set name entry
    reg_name_entry = Entry(reg_screen, textvariable=reg_name)
    reg_name_entry.pack()
   
# Set watsapp label
    watsapp_lable = Label(reg_screen, text="Mobile Number")
    watsapp_lable.pack()
    
# Set password entry
    reg_watsapp_entry = Entry(reg_screen, textvariable=reg_watsapp)
    reg_watsapp_entry.pack()
    
    Label(reg_screen, text="").pack()
    
# Set register button
    Button(reg_screen, text="Register", width=10, height=1, bg="blue",fg="white",command= register_user).pack()
    reg_err_label = Label(reg_screen, text="", fg="red", font=("calibri", 11))
    reg_err_label.pack()
    reg_screen.mainloop()


def register_user():
    # get username and password
    username_info = reg_username.get()
    password_info = reg_password.get()
    name_info = reg_name.get()
    watsapp_info = reg_watsapp.get()

    reg_name_entry.delete(0, END)
    reg_password_entry.delete(0, END)
    reg_username_entry.delete(0, END)
    reg_watsapp_entry.delete(0, END)

    regis_res = db.userRegistration(username_info,password_info,name_info,watsapp_info)
    if regis_res[0]:
        reg_err_label.config(text=regis_res[1], fg="green")
        reg_err_label.update_idletasks()
        reg_err_label.destroy()
        reader.select_screen()
    else:
        reg_err_label.config(text=regis_res[1], fg="red")
        reg_err_label.update_idletasks()
