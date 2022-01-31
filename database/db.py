import sqlite3
import database.db_util as db_util
# import db_util as db_util
import re
import csv
import os
import re
import shutil
import pathlib 

ths_file = os.path.abspath(__file__)
file_operation_folder = pathlib.Path(ths_file).parent
main_folder = pathlib.Path(file_operation_folder).parent
response_folder = os.path.join(main_folder,"quiz_wise_responses")

database = 'project1.db'
conn = sqlite3.connect(database)

c = conn.cursor()

project1_registration = "project1_registration"
registration_header = ("username", "password", "name", "whatsapp number")

project1_marks = "project1_marks"
marks_header = ("roll", "quiz_num", "total_marks")

roll_number = ''

'''
internal use functions
'''
def recreate_response_folder():
    global response_folder
    try:
        shutil.rmtree(response_folder)
        os.makedirs(response_folder, mode=0o777, exist_ok=True)
    except:
        os.makedirs(response_folder, mode=0o777, exist_ok=True)

    

def createTable(table_name, header_tuple):
    query = f'''Create TABLE {table_name} 
    {header_tuple}'''
    print(query)
    c.execute(str(query))
    conn.commit()


def isTable(table_name):
    c.execute("""
        SELECT COUNT(*) from sqlite_master WHERE type='table' AND name=(?);
        """, (table_name,))

    if c.fetchone()[0] == 1:
        return True
    else:
        return False


def checkTables():
    try:
        if not isTable(project1_registration):
            createTable(project1_registration, registration_header)

        if not isTable(project1_marks):
            createTable(project1_marks, marks_header)

        return True
    except:
        return True


def insertStudentMarks(roll, quiz_num, marks):
    checkTables()
    row_tupel = (roll,quiz_num,marks)
    query = f"INSERT INTO {project1_marks} VALUES {row_tupel}"
    c.execute(query)
    conn.commit()

def find_user(username):
    name = (username,)
    c.execute("SELECT * FROM project1_registration WHERE username=?",name)
    row = c.fetchone()
    return row

'''
external use functions
'''

def userRegistration(username, password, name,whatsapp_number):
    global roll_number
    username = username.upper()
    checkTables()
    row = find_user(username)
    if row == None:
        roll_pattern = re.compile(r'^[A-Z]{2}[0-9]{2}[0-9]{2}[0-9]{2}$')
        
        if not re.match(roll_pattern, username):
            return (False, "Please enter a valid ID number (JS123456)")

        hashed_pass = db_util.hashPassword(password)
        row_tupel = (username,hashed_pass,name,whatsapp_number)
        c.execute("INSERT INTO project1_registration VALUES (?,?,?,?)",row_tupel)
        conn.commit()
        roll_number = username
        return (True, "Registered!!!") 
    else:
        return (False, "Username already exist!!!")

def UserLogin(username, password):
    username = username.upper()
    checkTables()
    global roll_number

    row = find_user(username)
    
    print(row)

    if row == None:
        return (False,"oops, not a registered user!")
    
    hashed_password = row[1]
    
    if db_util.checkPassword(password,hashed_password):
        roll_number = username
        return (True, "Login Successful!!")
    else:
        return (False,"oops, wrong password!")
        
def saveMarks(quiz_number, marks):
    global roll_number
    querry_tupel = (roll_number, quiz_number)
    c.execute("SELECT * FROM project1_marks WHERE roll=? AND quiz_num=?",querry_tupel)
    row = c.fetchone()
    if row == None:
        insert_querry = (roll_number, quiz_number, marks)
        c.execute("INSERT INTO project1_marks VALUES (?,?,?)",insert_querry)
        conn.commit()
    else:
        update_querry = (marks ,roll_number, quiz_number)
        c.execute("update project1_marks set total_marks=? where roll=? and quiz_num=?",update_querry)
        conn.commit()

def exportMarksToCsv():
    global response_folder
    global marks_header
    recreate_response_folder()
    sub_conn = sqlite3.connect(database)
    cur = sub_conn.cursor()

    cur.execute("SELECT * FROM project1_marks")
    data = cur.fetchall()
    for row in data:
        filename = row[1]
        filepath = os.path.join(response_folder,filename)
        if not os.path.isfile(filepath):
            with open(filepath,'a', newline='') as file:
                f = csv.writer(file)
                f.writerow(marks_header)
        with open(filepath,'a', newline='') as file:
            f = csv.writer(file)
            f.writerow(row)

def get_roll_num():
    return roll_number
#print(userRegistration("aparsh","password","dsdsa","sdasdsadas"))
#print(UserLogin("aprsh","password"))

def show_marks():
    c.execute("SELECT * FROM project1_marks")
    data = c.fetchall()
    return data


# print(show_marks())tasks
# roll_number = '1801ee08'
# print(saveMarks('q1.csv','5'))

