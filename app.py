import streamlit as st
import pandas as pd
import json
# from Utils import *

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

def convert24(str1):
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]

    elif str1[-2:] == "AM":
        return str1[:-2]

    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]

    else:
        return str(int(str1[:2]) + 12) + str1[2:8]


def formatAMPM(startI, endI, m):
    if len(startI) < 5:
        startI = "0" + startI
    if len(endI) < 5:
        endI = "0" + endI

    start, end = startI + ":00 " + m, endI + ":00 " + m

    start24, end24 = convert24(start), convert24(end)
    startH, endH = start24.split(":")[0], end24.split(":")[0]

    if startH <= endH:
        return int(start24.strip().replace(":", "")), int(end24.strip().replace(":", ""))

    else:
        start, end = startI + ":00" + " AM", endI + ":00 " + m
        start24, end24 = convert24(start), convert24(end)

        return int(start24.strip().replace(":", "")), int(end24.strip().replace(":", ""))


def convertTimetoInt(timeList):
    timeDict = {}
    for cTime in timeList:
        if cTime == "TBA":
            continue
        cols = cTime.split(" ")
        start, end, m = cols[0], cols[2], cols[3]
        start24, end24 = formatAMPM(start, end, m)

        timeDict[start24] = {
            "End": end24,
            "Original": cTime
        }

    return timeDict
    pass


def getCurrTime():
    curr = time.localtime()
    curr24 = int(time.strftime("%H%M%S", curr))
    currDay = time.strftime("%A", curr)
    if currDay == "Thursday":
        currDay = "R"
    elif currDay == "Sunday":
        currDay = "Sunday"
    else:
        currDay = currDay[0]

    return curr24, currDay


def checkAvailibilty(current, hallDict, inUse=False):
    emptyRooms = []
    inUse = []

    for room in hallDict:
        roomMT = True
        startingTimes = sorted(list(hallDict[room].keys()))

        for index, startTime in enumerate(startingTimes):
            if startTime <= current <= hallDict[room][startTime]["End"]:
                inUse.append((room,hallDict[room][startTime]["Original"] ))
                roomMT = False

        if roomMT:
            emptyRooms.append(room)

    return emptyRooms, inUse


def getNext(current, AvailableRooms, hallInfo, hallName, currDay):
    global SCHEDULE

    nextClass = {}

    for MT_Room in AvailableRooms:
        next = None
        sched = hallInfo[MT_Room]

        for start in sched:
            if current < start:
                next = start
                break

        if next:
            nextStart = hallInfo[MT_Room][next]["Original"]
            nextName = SCHEDULE[hallName][MT_Room][currDay][nextStart]
        else:
            nextStart = "No Classes Left Today"
            nextName = "None"

        nextClass[MT_Room] = {
            "Start": nextStart,
            "Name": nextName
        }

    return nextClass


def getCurr(current, AvailableRooms, hallInfo, hallName, currDay):
    global SCHEDULE

    CurrentClasses = {}

    for (room, original) in AvailableRooms:
        sched = hallInfo[room]
        ongoingClassTime = None

        schedList = list(sched.keys())

        
        if ongoingClassTime == None:
            ongoingClass = SCHEDULE[hallName][room][currDay][original]

            CurrentClasses[room] = {
                "Name" : ongoingClass,
                "Timing": original
            }

    return CurrentClasses


def check_time(command):
    print(command.text)
    if "time:" in command.text.lower():
        selectedTime = command.text.lower()[5:]
        if "reset" in selectedTime:
            return True
        hrs, mins = selectedTime.split(":")[0].strip(), selectedTime.split(":")[1].strip()

        print(hrs, mins)

        return True


def get_info(selectedHall, cDay="Curr", cTime="Curr"):
    print(cDay, cTime)
    # return
    roomScheduleInfo = {}

    current, currDay = getCurrTime()
    if cDay != "Curr":

        if cDay == "Thursday":
            cDay = "R"
        elif cDay == "Sunday":
            cDay = "Sunday"
        else:
            cDay = currDay[0]

        currDay = cDay

    if cTime != "Curr":
        current = cTime
    
    print(current, currDay)
    
    if currDay == "Sunday":
    
        return "Weekend", {}

    for room in SCHEDULE[selectedHall]:
        todaysSchedule = (SCHEDULE[selectedHall][room][currDay])

        classTimes = list(todaysSchedule.keys())
        roomScheduleInfo[room] = convertTimetoInt(classTimes)

    emptyRooms, inUse = checkAvailibilty(current, roomScheduleInfo)

    nextList = getNext(current, emptyRooms, roomScheduleInfo, selectedHall, currDay)
    CurrList = getCurr(current, inUse, roomScheduleInfo, selectedHall, currDay)
    

    return makeList(nextList, CurrList)



def makeList(nextDict, CurrDict):
    NextClassList, CurrList = [], []

    for room in nextDict:
        NextClassList.append([room, nextDict[room]["Name"], nextDict[room]["Start"]])

    for room in CurrDict:
        CurrList.append([room, CurrDict[room]["Name"], CurrDict[room]["Timing"]])
        
    return (NextClassList, CurrList)



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
