import streamlit as st
import threading
import pandas as pd
import json
import telebot
from Utils import *
import time

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

#! TELEGRAM START
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass


API_KEY = os.environ.get("telegrambotAPI_key")
CHAT_ID = os.environ.get("CHAT_ID")

bot1 = telebot.TeleBot(API_KEY)



try:
    with open('Final/Final_Sorted_Schedule.json') as json_file1:
        SCHEDULE = json.load(json_file1)
except:
    with open('Final_Sorted_Schedule.json') as json_file1:
        SCHEDULE = json.load(json_file1)

with open("CourseList.json", "r") as json_file2:
    courses_list = json.load(json_file2)

with open("total_data.json", "r") as json_file3:
    total_data = json.load(json_file3)

try:
    with open("Instructors.json", "r") as json_file4:
        InstructorDict = json.load(json_file4)
except:
    InstructorDict = {}

# Streamlit 
st.set_page_config(page_title="UC Davis Classroom Search", layout="wide", page_icon="ShreyIconS2.png")
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


menu = st.sidebar.selectbox("Mode", ["Current Classes", "Weekly Schedule", "Course Info"])

current_time = time.strftime("%I:%M:%S %p", time.localtime())
session_id = get_session_id()

if 'message_sent' not in st.session_state:
    st.session_state.message_sent = False

# If the message hasn't been sent yet, send the message and set the state to True
if not st.session_state.message_sent:
    try:
        sendMessage(bot1, CHAT_ID, current_time)
        st.session_state.message_sent = True

    except Exception as e:
        print("Failed to send message")
        print(e)



if menu == "Current Classes":
    P, Q, R = st.columns((1, 4, 1))
    Q.title("UC Davis Classroom Search")
    
    colA, colB, colC = st.columns((1, 4, 1))
    days = ["Today"] + ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    selected_day = colB.selectbox("Select Day", days)
    
    colz, col1, col2, zolx = st.columns((1, 2, 2, 1))
    
    hour_options = ["Current Time"] + [f"{hour:02d}" for hour in range(0, 24)]
    selected_hour = col1.selectbox("Select Hour", hour_options)
    
    if selected_hour == "Current Time":
        selected_time = "Curr"
        minute_options = ["Current"]
    else:
        minute_options = [f"{minute:02d}" for minute in range(0, 60, 10)]
    selected_minute = col2.selectbox("Select Minute", minute_options)
    
    if selected_day == "Today":
        selected_day = "Curr"
    
    if selected_hour != "Current Time":
        selected_time = int(selected_hour + selected_minute + "00")

    colX, colY, colZ = st.columns((1, 4, 1))
    halls = list(SCHEDULE.keys())
    selected_hall = colY.selectbox("Select Hall", halls)


    vacant_rooms_data, ongoing_classes_data = get_info(selected_hall, selected_day, selected_time)
    
    # Log Action:
    option_selected = f"Mode: {menu} | "
    option_selected += f"Hall: {selected_hall}"
    if selected_day != "Curr":
        option_selected += f" FOR Day: {selected_day}"
    if selected_hour != "Current Time":
        option_selected += f" and Time: {selected_hour}: {selected_minute}"
    log_action(option_selected, session_id)

    if vacant_rooms_data != "Weekend":
        colY.subheader("Vacant Classrooms")
        vacant_rooms_df = pd.DataFrame(vacant_rooms_data, columns=["Room", "Next Class", "Vacant Till"])
        colY.table(vacant_rooms_df)

        colY.subheader("Ongoing Classes")
        ongoing_classes_df = pd.DataFrame(ongoing_classes_data, columns=["Room", "Class", "In Use Till"])
        colY.table(ongoing_classes_df)
    else:
        colY.write("**Weekend...**")

elif menu == "Weekly Schedule":
    st.title("UC Davis Classroom Search")
    buildings = SCHEDULE.keys()
    col1, col2 = st.columns(2)
    selected_building = col1.selectbox("Select Building", buildings)

    rooms = SCHEDULE[selected_building].keys()
    rooms = sort_rooms(rooms)
    selected_room = col2.selectbox("Select Room", rooms)
    data = SCHEDULE[selected_building][selected_room]

    schedule_df = createDataFrame(data)
    st.subheader(f"Schedule for {selected_building}: {selected_room}")
    st.table(schedule_df.fillna(''))

    # Log action;
    option_selected = f"Mode: {menu} | "
    option_selected += f"Hall: {selected_building}, Room: {selected_room}"
    log_action(option_selected, session_id)

elif menu == "Course Info":
    P, Q, R = st.columns((1, 4, 1))
    Q.title("Course Info")
    courses = ["Select"] + sorted(courses_list.keys(), reverse=True) 
    courses = sorted(courses_list.keys(), reverse=True) 
    selected_course = Q.selectbox("Select Course", courses)

    if selected_course != "Select":
        dataframes, lecture_infos, Name = getCourseInfo(selected_course)
        Q.subheader(" ")
        Q.subheader(f"{Name}")
        Q.write("---")  # Optional: Add a separator between groups
        Q.write("")

        sorted_lecture_infos = sorted(lecture_infos, key=lambda x: x[0])
        sorted_dataframes = [df for _, df in sorted(zip(lecture_infos, dataframes), key=lambda x: x[0][1], reverse=True)]


        for (info2print, lecInfo) in zip(sorted_dataframes, sorted_lecture_infos):
            
            # Q.write(f"Course information for {lecInfo[0]}:")
            Q.write(f'<p style="font-size:24px;">Course information for {lecInfo[0]}:</p>', unsafe_allow_html=True)
            Q.write(f"**Lecture: {lecInfo[1]}**")
            Q.write("Discussion/lab sessions:")
            Q.table(info2print.fillna(''))
            Q.write(f"Maximum Class Size: {lecInfo[2]}")
            Q.write("---")  # Optional: Add a separator between groups

    # Log action;
    option_selected = f"Mode: {menu} | "
    option_selected += f"Course: {selected_course}"
    log_action(option_selected, session_id)
elif menu == "Instructor Schedule":

    st.title("Instructor Schedule")
    Instructors = sorted(list(InstructorDict.keys()))
    selected_instructor = st.selectbox("Select Instructor", Instructors)
    data = InstructorDict[selected_instructor]
    schedule_df = createDataFrame(data)
    st.subheader(f"Schedule for {selected_instructor}")
    st.table(schedule_df.fillna(''))









