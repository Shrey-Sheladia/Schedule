import os
import json
import time
import time
import pprint
import uuid
import pandas as pd
import streamlit as st
from datetime import datetime
from itertools import groupby
from operator import itemgetter

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass


pp = pprint.PrettyPrinter(indent=2)

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


        return True


def get_info(selectedHall, cDay="Curr", cTime="Curr"):
    # return
    roomScheduleInfo = {}

    current, currDay = getCurrTime()
    if cDay != "Curr":

        if cDay == "Thursday":
            cDay = "R"
        elif cDay == "Sunday":
            cDay = "Sunday"
        else:
            cDay = cDay[0]

        currDay = cDay

    if cTime != "Curr":
        current = cTime
    
    
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

def get_time(s):
    start_time, am_pm = s.split(" - ")[0], s.split(" - ")[1].split(" ")[1]
    if am_pm == "PM" and start_time.split(":")[0] != "12":
        start_time = str(int(start_time.split(":")[0]) + 12) + ":" + start_time.split(":")[1]
    elif am_pm == "AM" and start_time.split(":")[0] == "12":
        start_time = "00:" + start_time.split(":")[1]
    dt = datetime.strptime(start_time, "%H:%M")
    return dt.time()


def createDataFrame(data):
    time_slots = sorted(set([time for day in data.values() for time in day]))
    time_slots = sorted(time_slots, key=get_time)
    schedule_df = pd.DataFrame(index=time_slots, columns=data.keys())
    for day, classes in data.items():
        for time, class_info in classes.items():
            schedule_df.at[time, day] = class_info

    return schedule_df

def sort_rooms(rooms):
    numeric_rooms = []
    non_numeric_rooms = []
    for room in rooms:
        if room.isnumeric():
            numeric_rooms.append(int(room))
        else:
            non_numeric_rooms.append(room)
    sorted_numeric_rooms = sorted(numeric_rooms)
    sorted_rooms = non_numeric_rooms + [str(room) for room in sorted_numeric_rooms] 
    return sorted_rooms


def group_keys_by_values(d):
    grouped = {}
    for key, value in d.items():
        if value not in grouped:
            grouped[value] = []
        grouped[value].append(key)

    return grouped


def group_courses(course_dict):

    hDict = {}
    lecs, dis, lab = {}, {}, {}

    for CRN in course_dict:
        for key in course_dict[CRN]:
            if key not in ["Course Code", "Name", "Instructors", "Total", "Filled"]:
                d, t = course_dict[CRN][key]["Day"], course_dict[CRN][key]["Time"]
                if f"{key}:-   {d} : {t}" not in hDict:
                    hDict[f"{key}:-   {d} : {t}"] = [CRN]
                else:
                    hDict[f"{key}:-   {d} : {t}"].append(CRN)

    sorted_dict = dict(sorted(hDict.items(), key=lambda x: len(x[1]), reverse=True))
    

    for loc in sorted_dict:
        for crn in sorted_dict[loc]:
            if crn not in lecs:
                lecs[crn] = loc
            elif crn not in dis:
                print(1)
                dis[crn] = loc
            else:
                print(2)
                lab[crn] = loc

    groups = group_keys_by_values(lecs)

    if dis == {}:
        dis = lecs

    return groups, lecs, dis, lab


def getCourseInfo(selected_course):
    classData = {}
    dataFrames, LecInfo = [], []
    Name = None

    crns = courses_list[selected_course]
    for crn in crns:
        classData[crn] = total_data[crn]

    groups, lecs, diss, lab = (group_courses(classData))
    



    for loc in groups:
        infoDict = {"Course Code": [],
                    "Locations": [],
                    "Instructors": [],
                    "Filled/Total": []
                    }
        f, l = classData[groups[loc][0]]["Course Code"], classData[groups[loc][-1]]["Course Code"]
        if f != l:
            seq = f + f"-{l.split()[-1]}"
        else:
            seq = f

        

        TotalSize = 0

        
        for crn in groups[loc]:
            if not Name:
                Name = total_data[crn]["Name"]
            tf = f'{classData[crn]["Filled"]}/{classData[crn]["Total"]}'
            TotalSize += int(classData[crn]["Total"])
            infoDict["Course Code"].append(classData[crn]["Course Code"])
            try:
                
                loc = (diss[crn])
                if "TBA" in loc: loc = "--"
            except:
                loc = (" ")
            if crn in lab:
                if loc != "--":
                    infoDict["Locations"].append(f"{loc}\n; \n{lab[crn]}")
                else:
                    infoDict["Locations"].append(f"{lab[crn]}")
            else:
                infoDict["Locations"].append(loc)
            infoDict["Instructors"].append(" ".join(classData[crn]["Instructors"]))
            infoDict["Filled/Total"].append(tf)

        try:
            dataFrames.append(pd.DataFrame(infoDict))
        except:
            print("_"*200)
        LecInfo.append((seq, loc, TotalSize))

    return dataFrames, LecInfo, Name


def sendMessage(bot, CHAT_ID, text=None):
    if text:
        message = f"Website Being Used: {text}"
    else:
        message = "Website Being Used"
    bot.send_message(CHAT_ID, message)
    print(message)
    pass

def log_action(option_selected, session_id):
    with open("log.txt", "a") as log_file:
        now = datetime.now()
        log_entry = f"{now.strftime('%Y-%m-%d - %H:%M:%S')} | {session_id} | Option selected: {option_selected}\n"
        log_file.write(log_entry)
        print(log_entry, 1)

def get_session_id():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

if __name__ == "__main__":
    sendMessage()


