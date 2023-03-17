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




# if __name__ == "__main__":
#     nextList, inUse = get_info("Olson Hall")
#     pp.pprint(nextList)
#     print("_"*10)
#     pp.pprint(inUse)




schedule_data = {
    "Monday": ["Math", "Physics", "Chemistry", "Biology"],
    "Tuesday": ["Physics", "Chemistry", "Biology", "Math"],
    "Wednesday": ["Chemistry", "Biology", "Math", "Physics"],
    "Thursday": ["Biology", "Math", "Physics", "Chemistry"],
    "Friday": ["Math", "Physics", "Chemistry", "Biology"],
}

# Streamlit App
st.set_page_config(page_title="UC Davis Classroom Search", layout="centered")
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title("UC Davis Classroom Search")

menu = st.sidebar.selectbox("Mode", ["Current Classes", "Schedule"])


if menu == "Current Classes":
    
    
    days = ["Today"] + ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    selected_day = st.selectbox("Select Day", days)
    
    col1, col2 = st.columns(2)
    
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

    halls = list(SCHEDULE.keys())
    selected_hall = st.selectbox("Select Hall", halls)


    st.subheader("Vacant Classrooms")
    vacant_rooms_data, ongoing_classes_data = get_info(selected_hall, selected_day, selected_time)
    vacant_rooms_df = pd.DataFrame(vacant_rooms_data, columns=["Room", "Vacant Till", "Next Class"])
    st.table(vacant_rooms_df)

    st.subheader("Ongoing Classes")
    ongoing_classes_df = pd.DataFrame(ongoing_classes_data, columns=["Room", "Class", "In Use Till"])
    st.table(ongoing_classes_df)

elif menu == "Schedule":
    buildings = ["Building 1", "Building 2", "Building 3", "Building 4"]
    selected_building = st.selectbox("Select Building", buildings)

    rooms = ["Room 101", "Room 102", "Room 103", "Room 104"]
    selected_room = st.selectbox("Select Room", rooms)

    st.subheader(f"Schedule for {selected_room}")
    schedule_df = pd.DataFrame(schedule_data, index=["8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00"])
    st.table(schedule_df)
