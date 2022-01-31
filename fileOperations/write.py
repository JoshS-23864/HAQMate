import csv
import os
import re
import shutil
import pathlib 

ths_file = os.path.abspath(__file__)
file_operation_folder = pathlib.Path(ths_file).parent
main_folder = pathlib.Path(file_operation_folder).parent
ind_response_folder = os.path.join(main_folder,"individual_responses")
response_folder = os.path.join(main_folder,"quiz_wise_responses")
question_folder = os.path.join(main_folder,"quiz_wise_questions")

ind_file_header = ("ques_no","question","option1","option2","option3","option4","correct_option","marks_correct_ans","marks_wrong_ans","compulsory","marked_choice","Total","Legend")
resp_file_header = ()

def write_ind_file(roll_num, quiz_number, data):
    q_roll = re.split('\.',quiz_number)[0]+"_"+roll_num+".csv"
    file_name = os.path.join(ind_response_folder,q_roll)

    with open(file_name,"w",newline='') as file:
        f = csv.writer(file)
        f.writerow(ind_file_header)
        f.writerows(data)



