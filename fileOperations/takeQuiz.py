import csv
import os
import time
import re
import shutil
import time
import pathlib
import utilities.timer as timer
from pynput import keyboard
import database.db as db
import fileOperations.write as writer
import threading
from tkinter import *

ths_file = os.path.abspath(__file__)
file_operation_folder = pathlib.Path(ths_file).parent
main_folder = pathlib.Path(file_operation_folder).parent
response_folder = os.path.join(main_folder, "quiz_wise_responses")
question_folder = os.path.join(main_folder, "quiz_wise_questions")

current = set()
ans_data = []
unattempted_questions = []
question_index=1
questions = []
attempted_question_index = []
marks_obt = 0
max_marks = 0
quiz_file = ''
quiz_num = ''
timer_th = ''
quiz_runnig = True


# The key combination to check
COMBINATIONS = [
    {keyboard.Key.alt, keyboard.Key.ctrl,keyboard.KeyCode(char='u')},
    {keyboard.Key.alt, keyboard.Key.ctrl,keyboard.KeyCode(char='g')}
]

def print_question(question):
    print("Q.", question[0], " ", question[1])
    print("option 1: ", question[2])
    print("option 2: ", question[3])
    print("option 3: ", question[4])
    print("option 4: ", question[5])
    print("Correct mrks ", question[7])
    print("Incorrect mrks ", question[8])
    print("cumpulsory : ", question[9])

def valid_ans(ans):
    if ans in ('1','2','3','4','s'):
        return True
    else: 
        return False


def sort_by_col(data):
    l = len(data)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (data[j][0] > data[j + 1][0]):
                tempo = data[j]
                data[j] = data[j + 1]
                data[j + 1] = tempo
    return data


def submit_quiz():
    global marks_obt
    global ans_data
    global attempted_question_index
    global quiz_file
    global quiz_num
    global timer_th
    global questions
    global quiz_runnig
    quiz_runnig = False
    timer.closeTimer()
    correct_questions = 0
    wrong__questions = 0
    questions_attempted = 0
    marks_obt = 0
    print(ans_data)
    for i in range(1,len(questions)):
        print(ans_data[i][11])
        marks_obt += int(ans_data[i][11])
        if ans_data[i][10] is not '':
            questions_attempted += 1
            if int(ans_data[i][11]) == int(questions[i][7]):
                correct_questions += 1
            else:
                wrong__questions += 1

    marks_got = str(marks_obt)+'/'+str(max_marks)
    
    summary_screen = Tk()   # create a GUI window 
    summary_screen.geometry("350x300") # set the configuration of GUI window 
    summary_screen.title("Quiz")
    summary_screen.config(bg="white")
    
    Label(text="Quiz Ended!!", width="300", height="2", font=("Calibri", 13),bg="blue",fg="white").pack()
    Label(text="Total Quiz Questions: " + str(len(questions)-1), width="300", height="2", font=("Calibri", 13),bg="white").pack()
    Label(text="Total Quiz Questions Attempted: " + str(questions_attempted), width="300", height="2", font=("Calibri", 13),bg="white").pack()
    Label(text="Total Correct Question: " + str(correct_questions), width="300", height="2", font=("Calibri", 13),bg="white").pack()
    Label(text="Total Wrong Questions: " + str(wrong__questions), width="300", height="2", font=("Calibri", 13),bg="white").pack()
    Label(text="Total Marks: " + str(marks_got), width="300", height="2", font=("Calibri", 13),bg="white").pack()
    
    summary_screen.mainloop()
    ans_data.pop(0)
    db.saveMarks(quiz_num,marks_obt)
    ans_data.append(['','','','','','','','','','','',marks_obt,"Marks Obtained"])
    ans_data.append(['','','','','','','','','','','',max_marks,"Total Quiz Marks"])
    writer.write_ind_file(db.get_roll_num(),quiz_num, ans_data)

def submitQuizonTime():
    while True:
        if timer.t is 0:
            submit_quiz()
            return
def delete_all_screens():
    try:
        unattempted_screen.destroy()
    except:
        print("")
    try:
        goto_screen.destroy()
    except:
        print("")

def show_unattempted():
    global unattempted_questions
    global unattempted_screen
    delete_all_screens()
    unattempted_screen = Tk()   # create a G
    unattempted_screen.title("Unattempted questions") # set the title of GUI window
    unattempted_screen.configure(bg="white")
    if len(unattempted_questions) is 0:
        unattempted_screen.geometry("300x250")
        Label(unattempted_screen, text="No unattempted questions!! XD", bg="green",fg="white", width="300", height="2").pack()
    else:
        unattempted_screen.geometry("300x400")
        Label(unattempted_screen,text="Unttempted Questions", bg="blue",fg="white", width="300", height="2", font=("Calibri", 13)).pack() 
        scrollbar = Scrollbar(unattempted_screen)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(unattempted_screen, yscrollcommand=scrollbar.set, width=300)

        for ques in unattempted_questions:
            listbox.insert(END,"Q"+str(ques[0])+". "+str(ques[1]))

        # listbox.pack(side=LEFT, fill=BOTH)
        listbox.pack()

        scrollbar.config(command=listbox.yview)
    
    Label(unattempted_screen,text=" ",bg="white").pack()
    Button(unattempted_screen,text="Back to quiz", height="2", width="30",command=back_to_quiz).pack()
    Label(unattempted_screen,text=" ",bg="white").pack()
    Button(unattempted_screen,text="Goto", height="2", width="30",command=go_to_screen).pack()
    
    unattempted_screen.mainloop()
    
def back_to_quiz():
    unattempted_screen.destroy()
    update_question()

def go_to_screen():
    unattempted_screen.destroy()    
    goto_question()

def goto_question():
    global question_index
    global questions
    global goto_screen
    global goto_err_label
    global goto_err_label
    global question_choice
    global question_choice_entry
    delete_all_screens()
    
    max_ques_num = len(questions) - 1 
    goto_screen = Tk()   # create a GUI window 
    goto_screen.winfo_toplevel()
    goto_screen.title("Goto screen") # set the title of GUI window
    goto_screen.configure(bg="white")
    goto_screen.geometry("400x250")
    
    Label(goto_screen,text="Enater a question number between 1 and "+str(max_ques_num), bg="white", width="400", height="2", font=("Calibri", 13)).pack() 
    question_choice = IntVar()
    question_choice_entry = Entry(goto_screen, textvariable=question_choice)
    question_choice_entry.pack()
    goto_err_label = Label(goto_screen, text="" ,bg="white" ,fg="red" ,font=("calibri", 11))
    goto_err_label.pack()
    Button(goto_screen,text="Goto", height="2", width="30",command=goto_question_check).pack()
    
    goto_screen.mainloop()

def goto_question_check():
    global question_index
    selected_ques = question_choice_entry.get()
    print(selected_ques)
    selected_ques = int(selected_ques)
    if selected_ques>0 and selected_ques<len(questions):
        question_index = selected_ques
        goto_screen.destroy()
        update_question()
    else:
        goto_err_label.config(text="Please select a valid choice!!")
        goto_err_label.update_idletasks()

def on_press(key):
    if quiz_runnig and any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if check_and_update_ans():
            if all(k in current for k in list(COMBINATIONS[0])):
                show_unattempted()
            if all(k in current for k in list(COMBINATIONS[1])):
                goto_question()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)
def hotkeys_ug():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def make_answersheet():
    global questions
    global ans_data
    global max_marks
    ans_data = questions.copy()
    for i in range(0,len(ans_data)):
        if i is not 0:
            max_marks+=int(ans_data[i][7])
            # ans_data[i].append('')
            ans_data[i].append(0)
            ans_data[i].append('Unattempted')


#TODO: make sroppable thread
#WORKAROUND: destroyed the timer window
'''
DESCRIPTION: Used if quiz is taken in console
def start_quiz(quiz_name):
    global quiz_num
    global marks_obt
    global ans_data
    global unattempted_questions
    global attempted_question_index
    global quiz_file
    global timer_th
    global question_index
    global questions
    global quiz_runnig

    quiz_num = quiz_name
    quiz_file = os.path.join(question_folder, quiz_name)
    with open(quiz_file, "r") as file:
        data = csv.reader(file)
        ques = list(data)
        max_ques = len(ques)
        questions = ques.copy()
        make_answersheet()
        submit_th = threading.Thread(target=submitQuizonTime)
        submit_th.start()
        submit_th = threading.Thread(target=submitQuizonTime)
        submit_th.start()
        unattempted_th = threading.Thread(target=hotkeys_ug)
        unattempted_th.start()
        question_index=0
        while quiz_runnig: 
            row = questions[question_index]
            if question_index is 0:
                quiz_time = re.findall(r'[0-9]+',row[10])[0]
                timer_th = threading.Thread(target=timer.countdown,args=(int(quiz_time)*60,))
                timer_th.start()
            elif question_index < max_ques:
                print_question(row)
                correct_choice = row[6]
                marked_choice = 0
                total_pt = 1
                legend = 'Wrong Choices'
                while True:
                    marked_choice=input("Enter your answer 1,2,3,4,s(skip): ")
                    if valid_ans(marked_choice):
                        if marked_choice is 's':
                            if row[9] is 'y':
                              print("you cannot skip this question")   
                            else:
                                break
                        else:
                            if marked_choice is correct_choice:
                                total_pt = row[7]
                                legend = 'Correct Choices'
                            else:
                                total_pt = row[8]
                            break
                    else:
                        print("please enter a valid choice!!") 

                if marked_choice is not 's':
                    if row in unattempted_questions:
                        unattempted_questions.remove(row)
                    marks_obt+=(int(total_pt) - ans_data[question_index][11])
                    ans_data[question_index][10] = marked_choice
                    ans_data[question_index][11] = total_pt
                    ans_data[question_index][12] = legend
                    attempted_question_index.append(question_index)
                elif (ans_data[question_index][10]==''):
                    unattempted_questions.append(row)
            else:
                #submit quix when reach the end, can restart from ques 1 also
                submit_quiz()
            question_index+=1
            question_index%=max_ques

'''

def start_quiz_screen(quiz_name):
    global quiz_num
    global marks_obt
    global ans_data
    global unattempted_questions
    global attempted_question_index
    global quiz_file
    global timer_th
    global question_index
    global questions
    global quiz_runnig
    global quiz_time

    unattempted_questions = []
    quiz_num = quiz_name
    quiz_file = os.path.join(question_folder, quiz_name)
    with open(quiz_file, "r") as file:
        data = csv.reader(file)
        ques = list(data)
        max_ques = len(ques)
        questions = ques.copy()
        make_answersheet()
        question_index=1
        quiz_time = re.findall(r'[0-9]+',questions[0][10])[0]
        timer_th = threading.Thread(target=countdown,args=(int(quiz_time)*60,))
        timer_th.start()
        unattempted_th = threading.Thread(target=hotkeys_ug)
        unattempted_th.start()
        question_window()

def question_window():
    global question_screen
    global err_label
    global marked_ans
    global question_label
    global option1_lable
    global option2_lable
    global option3_lable
    global option4_lable
    global correct_marks_lable
    global incorrect_marks_lable
    global compulsory_lable
    global timer_label


    question_screen = Tk()   # create a GUI window 
    question_screen.geometry("550x600") # set the configuration of GUI window 
    question_screen.title("Quiz")
    
    timer_label = Label(text="", width="500", height="2", font=("Calibri", 13))
    timer_label.pack()

    Label(text=quiz_num, bg="blue",fg="white", width="500", height="2", font=("Calibri", 13)).pack() 
    Label(text="").pack() 
 
    question_label = Label(text="",bg="white", font=("Calibri", 13),width="500",anchor='w')
    question_label.pack(fill="both")
    
    option1_lable = Label(text="",bg="white", font=("Calibri", 13),width="500",anchor='w')
    option1_lable.pack(fill="both")
    
    option2_lable = Label(text="",bg="white", font=("Calibri", 13),width="500",anchor='w')
    option2_lable.pack(fill="both")
    
    option3_lable = Label(text="",bg="white", font=("Calibri", 13),width="500",anchor='w')
    option3_lable.pack(fill="both")
    
    option4_lable = Label(text="",bg="white", font=("Calibri", 13),width="500",anchor='w')
    option4_lable.pack(fill="both")
    
    correct_marks_lable = Label(text="",bg="white", font=("Calibri", 13),width="500",anchor='w')
    correct_marks_lable.pack(fill="both")
    
    incorrect_marks_lable = Label(text="",bg="white", font=("Calibri", 13),width="500",anchor='w')
    incorrect_marks_lable.pack(fill="both")
    
    compulsory_lable = Label(text="",bg="white", font=("Calibri", 13),width="500",anchor='w')
    compulsory_lable.pack(fill="both")

    Label(text="Enter the correct option number").pack()
    marked_ans = StringVar()
    marked_ans_entry = Entry(question_screen, textvariable=marked_ans)
    marked_ans_entry.pack()

    err_label = Label(question_screen, text="", fg="red", font=("calibri", 11))
    err_label.pack()

    update_question()

    Button(text="Next Question", height="2", width="30", command= next_question).pack() 
    Label(text="").pack() 
    Button(text="Previous Question", height="2", width="30", command= prev_question).pack() 
    Label(text="").pack() 
    Button(text="End quiz", height="2", width="30", bg="red", fg="white", command= end_quiz).pack() 
    question_screen.mainloop()

def countdown(quiz_time):

    while quiz_time>0:
        try:
            mins, secs = divmod(quiz_time, 60)
            new_time = '{:02d}:{:02d}'.format(mins, secs)
            # print(new_time)
            if quiz_time<61:
                timer_label.config(text=new_time,bg="red",fg="white")
            else:    
                timer_label.config(text=new_time)

            timer_label.update_idletasks()
            quiz_time-=1
        except:
            quiz_time-=1
        time.sleep(1)    
    
    submit_quiz()

def update_question():
    global marked_ans

    question_txt = "Q"+str(questions[question_index][0])+". "+str(questions[question_index][1])
    question_label.config(text=question_txt)
    question_label.update_idletasks()

    question_txt = "option 1: "+str(questions[question_index][2])
    option1_lable.config(text=question_txt)
    option1_lable.update_idletasks()
    
    question_txt = "option 2: "+str(questions[question_index][3])
    option2_lable.config(text=question_txt)
    option2_lable.update_idletasks()
    
    question_txt = "option 3: "+str(questions[question_index][4])
    option3_lable.config(text=question_txt)
    option3_lable.update_idletasks()
    
    question_txt = "option 4: "+str(questions[question_index][5])
    option4_lable.config(text=question_txt)
    option4_lable.update_idletasks()
    
    question_txt = "Correct Marks: "+str(questions[question_index][7])
    correct_marks_lable.config(text=question_txt)
    correct_marks_lable.update_idletasks()
    
    question_txt = "Incorrect Marks: "+str(questions[question_index][8])
    incorrect_marks_lable.config(text=question_txt)
    incorrect_marks_lable.update_idletasks()
    
    question_txt = "Compylsory: "+str(questions[question_index][9])
    compulsory_lable.config(text=question_txt)
    compulsory_lable.update_idletasks()

    marked_ans.set(ans_data[question_index][10])
    
    err_label.config(text="")
    err_label.update_idletasks()

def check_and_update_ans():
    ans_entered = marked_ans.get()
    if ans_entered not in ('1','2','3','4',''):
        err_label.config(text="invalid choice! ")
        err_label.update_idletasks()
        return False
    if ans_entered is '' and questions[question_index][9] is 'y':
        err_label.config(text="Its a compylsory, question")
        err_label.update_idletasks()
        return False

    row = questions[question_index]
    if (row in unattempted_questions) and (ans_entered in ('1','2','3','4')):
        unattempted_questions.remove(row)
    elif (row not in unattempted_questions) and (ans_entered is ''):
        unattempted_questions.append(row)

    ans_data[question_index][10] = ans_entered
    if ans_entered is questions[question_index][6]:
        ans_data[question_index][11] = int(questions[question_index][7])
        ans_data[question_index][12] = 'Correct Choices'
    elif ans_entered is '':
        ans_data[question_index][11] = 0
        ans_data[question_index][12] = 'Unattempted'
    else:
        ans_data[question_index][11] = int(questions[question_index][8])
        ans_data[question_index][12] = 'Wrong Choices'

    return True 

def next_question():
    global question_index
    if check_and_update_ans() and question_index<len(questions)-1:
        question_index+=1
        update_question()
    
def prev_question():
    global question_index
    if check_and_update_ans() and question_index>1:
        question_index-=1
        update_question()

def end_quiz():
    check_and_update_ans()
    question_screen.destroy()
    submit_quiz()