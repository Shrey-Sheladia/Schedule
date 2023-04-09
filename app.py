import streamlit as st
import pandas as pd
import json
from Utils import *
import time

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """


try:
    with open('Final/Final_Sorted_Schedule.json') as json_file1:
        SCHEDULE = json.load(json_file1)
except:
    with open('Final_Sorted_Schedule.json') as json_file1:
        SCHEDULE = json.load(json_file1)


# Streamlit App
st.set_page_config(page_title="UC Davis Classroom Search", layout="wide", page_icon="ShreyIconS2.png")
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


menu = st.sidebar.selectbox("Mode", ["Current Classes", "Weekly Schedule"])


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


    if vacant_rooms_data != "Weekend":
        colY.subheader("Vacant Classrooms")
        vacant_rooms_df = pd.DataFrame(vacant_rooms_data, columns=["Room", "Vacant Till", "Next Class"])
        colY.table(vacant_rooms_df)

        colY.subheader("Ongoing Classes")
        ongoing_classes_df = pd.DataFrame(ongoing_classes_data, columns=["Room", "Class", "In Use Till"])
        colY.table(ongoing_classes_df)
    else:
        colY.subheader(vacant_rooms_data)

elif menu == "Weekly Schedule":
    st.title("UC Davis Classroom Search")
    buildings = SCHEDULE.keys()
    selected_building = st.selectbox("Select Building", buildings)

    rooms = SCHEDULE[selected_building].keys()
    rooms = sort_rooms(rooms)
    selected_room = st.selectbox("Select Room", rooms)
    data = SCHEDULE[selected_building][selected_room]

    schedule_df = createDataFram(data)

    st.subheader(f"Schedule for {selected_building}: {selected_room}")
    st.table(schedule_df.fillna(''))

