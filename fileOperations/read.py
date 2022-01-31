import csv
import os
import re
import shutil
import pathlib 
import fileOperations.takeQuiz as takeQuiz
# import takeQuiz as takeQuiz
from tkinter import *

ths_file = os.path.abspath(__file__)
file_operation_folder = pathlib.Path(ths_file).parent
main_folder = pathlib.Path(file_operation_folder).parent
response_folder = os.path.join(main_folder,"quiz_wise_responses")
question_folder = os.path.join(main_folder,"quiz_wise_questions")

def select_screen():
    global main_screen
    global quiz_list
    global quiz_choice
    global err_label
    global quiz_enter

    quiz_list = os.listdir(question_folder)
    main_screen = Tk()   # create a GUI window 

    main_screen.title("Select Quiz") # set the title of GUI window
    main_screen.configure(bg="white")
    main_screen.geometry("300x350")
    # create a Form label 
    Label(text="Choose a Quiz Mate!", bg="gray",fg="white", width="300", height="2", font=("Calibri", 13)).pack()

    scrollbar = Scrollbar(main_screen)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(main_screen, yscrollcommand=scrollbar.set, width=300)
    num=1
    for quiz in quiz_list:
        listbox.insert(END,str(num) + ". " + re.split('\.',quiz)[0])
        num+=1
    
    # listbox.pack(side=LEFT, fill=BOTH)
    listbox.pack()

    scrollbar.config(command=listbox.yview)
    Label(main_screen, text="Please enter the quiz number (1-3)", bg="gray",fg="white").pack()
    quiz_choice = StringVar()
    quiz_enter = Entry(main_screen, textvariable=quiz_choice)
    quiz_enter.pack()
    err_label = Label(main_screen, text="", bg="white",fg="red", font=("calibri", 11))
    err_label.pack()
    Button(text="Start Quiz", height="2", width="30",command=start_quiz).pack()
    main_screen.mainloop()

def start_quiz():
    quiz_num = len(quiz_list)
    choice = int(quiz_choice.get())
    if choice>quiz_num or choice<1:
        err_label.config(text="invalid choice")
        err_label.update_idletasks()
    else:
        main_screen.destroy()
        takeQuiz.start_quiz_screen(quiz_list[choice-1])

'''
def select_quiz():
    while True:
        print("Select the quiz...")
        quzzis = os.listdir(question_folder)
        num = 1
        for quiz in quzzis:
            print(num," - ", re.split('\.',quiz)[0])
            num+=1
        num-=1
        choice = int(input("Enter Your choice: "))
        if choice>num or choice<1:
            print("enter a valid choice")
        else:
            takeQuiz.start_quiz(quzzis[choice-1])
            break



def read_quiz_questiions(quiz_name):
    quiz_file = os.path.join(question_folder,quiz_name)
    if(os.path.exists(quiz_file)):
        header=[]
        questions=[]
        with open(quiz_file) as file:
            data = csv.reader(file)
            is_header = True
            for row in data:
                if(is_header):
                    header = row
                    header = False
                    continue
                else:
                    questions.append(row)
            
        resp = (True,"quiz found!!!",header,questions)
        return resp
    else:
        resp = (False,"quiz not found!!!")
        return resp
    pass


'''