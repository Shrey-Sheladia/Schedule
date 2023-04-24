import pprint
import json

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

 
data = {"40120": {
        "Course Code": "ECN 101 A01",
        "Name": "Intermed Macro Theory",
        "Instructors": [
            "Paul Bergin"
        ],
        "Total": 40,
        "Filled": 40,
        "Walker Hall 1310": {
            "Day": "TR",
            "Time": "10:30 - 11:50 AM"
        },
        "Teaching and Learning Complex 3213": {
            "Day": "T",
            "Time": "6:10 - 7:00 PM"
        }
    },
    "40121": {
        "Course Code": "ECN 101 A02",
        "Name": "Intermed Macro Theory",
        "Instructors": [
            "Paul Bergin"
        ],
        "Total": 40,
        "Filled": 40,
        "Walker Hall 1310": {
            "Day": "TR",
            "Time": "10:30 - 11:50 AM"
        },
        "Teaching and Learning Complex 1214": {
            "Day": "T",
            "Time": "7:10 - 8:00 PM"
        }
    },
    "40122": {
        "Course Code": "ECN 101 A03",
        "Name": "Intermed Macro Theory",
        "Instructors": [
            "Paul Bergin"
        ],
        "Total": 40,
        "Filled": 40,
        "Walker Hall 1310": {
            "Day": "TR",
            "Time": "10:30 - 11:50 AM"
        },
        "Wellman Hall 207": {
            "Day": "W",
            "Time": "6:10 - 7:00 PM"
        }
    },
    "40123": {
        "Course Code": "ECN 101 A04",
        "Name": "Intermed Macro Theory",
        "Instructors": [
            "Paul Bergin"
        ],
        "Total": 40,
        "Filled": 40,
        "Walker Hall 1310": {
            "Day": "TR",
            "Time": "10:30 - 11:50 AM"
        },
        "Wellman Hall 207": {
            "Day": "W",
            "Time": "7:10 - 8:00 PM"
        }
    },
    "40124": {
        "Course Code": "ECN 101 B01",
        "Name": "Intermed Macro Theory",
        "Instructors": [
            "Paul Bergin"
        ],
        "Total": 40,
        "Filled": 40,
        "Hunt 100": {
            "Day": "TR",
            "Time": "1:40 - 3:00 PM"
        },
        "Teaching and Learning Complex 1218": {
            "Day": "T",
            "Time": "6:10 - 7:00 PM"
        }
    },
    "40125": {
        "Course Code": "ECN 101 B02",
        "Name": "Intermed Macro Theory",
        "Instructors": [
            "Paul Bergin"
        ],
        "Total": 40,
        "Filled": 40,
        "Hunt 100": {
            "Day": "TR",
            "Time": "1:40 - 3:00 PM"
        },
        "Teaching and Learning Complex 3213": {
            "Day": "T",
            "Time": "7:10 - 8:00 PM"
        }
    },
    "40126": {
        "Course Code": "ECN 101 B03",
        "Name": "Intermed Macro Theory",
        "Instructors": [
            "Paul Bergin"
        ],
        "Total": 40,
        "Filled": 40,
        "Hunt 100": {
            "Day": "TR",
            "Time": "1:40 - 3:00 PM"
        },
        "Teaching and Learning Complex 3212": {
            "Day": "W",
            "Time": "6:10 - 7:00 PM"
        }
    },
    "40127": {
        "Course Code": "ECN 101 B04",
        "Name": "Intermed Macro Theory",
        "Instructors": [
            "Paul Bergin"
        ],
        "Total": 40,
        "Filled": 39,
        "Hunt 100": {
            "Day": "TR",
            "Time": "1:40 - 3:00 PM"
        },
        "Teaching and Learning Complex 3211": {
            "Day": "W",
            "Time": "7:10 - 8:00 PM"
        }
    },
    "40128": {
        "Course Code": "ECN 101 C01",
        "Name": "Intermed Macro Theory",
        "Instructors": [
            "Emile Marin"
        ],
        "Total": 40,
        "Filled": 11,
        "Hart Hall 1150": {
            "Day": "TR",
            "Time": "1:40 - 3:00 PM"
        },
        "Olson Hall 223": {
            "Day": "T",
            "Time": "6:10 - 7:00 PM"
        }
    },
    "40129": {
        "Course Code": "ECN 101 C02",
        "Name": "Intermed Macro Theory",
        "Instructors": [
            "Emile Marin"
        ],
        "Total": 39,
        "Filled": 3,
        "Hart Hall 1150": {
            "Day": "TR",
            "Time": "1:40 - 3:00 PM"
        },
        "Olson Hall 261": {
            "Day": "T",
            "Time": "7:10 - 8:00 PM"
        }
    }}


data = {
    "35410": {
        "Course Code": "CHE 002B A01",
        "Name": "General Chemistry",
        "Instructors": [
            "Whitney Duim"
        ],
        "Total": 24,
        "Filled": 19,
        "Sciences Lecture Hall 123": {
            "Day": "MWF",
            "Time": "1:10 - 2:00 PM"
        },
        "Wellman Hall 127": {
            "Day": "T",
            "Time": "8:00 - 8:50 AM"
        },
        "Sciences Lab Building 2051": {
            "Day": "T",
            "Time": "9:00 - 11:50 AM"
        }
    },
    "35411": {
        "Course Code": "CHE 002B A02",
        "Name": "General Chemistry",
        "Instructors": [
            "Whitney Duim"
        ],
        "Total": 24,
        "Filled": 23,
        "Sciences Lecture Hall 123": {
            "Day": "MWF",
            "Time": "1:10 - 2:00 PM"
        },
        "Wellman Hall 123": {
            "Day": "T",
            "Time": "8:00 - 8:50 AM"
        },
        "Sciences Lab Building 2059": {
            "Day": "T",
            "Time": "9:00 - 11:50 AM"
        }
    },
    "35412": {
        "Course Code": "CHE 002B A03",
        "Name": "General Chemistry",
        "Instructors": [
            "Whitney Duim"
        ],
        "Total": 24,
        "Filled": 23,
        "Sciences Lecture Hall 123": {
            "Day": "MWF",
            "Time": "1:10 - 2:00 PM"
        },
        "Sciences Lab Building 2051": {
            "Day": "M",
            "Time": "4:10 - 7:00 PM"
        },
        "Hunt 110": {
            "Day": "R",
            "Time": "8:00 - 8:50 AM"
        }
    },
    "35413": {
        "Course Code": "CHE 002B A04",
        "Name": "General Chemistry",
        "Instructors": [
            "Whitney Duim"
        ],
        "Total": 24,
        "Filled": 23,
        "Sciences Lecture Hall 123": {
            "Day": "MWF",
            "Time": "1:10 - 2:00 PM"
        },
        "Sciences Lab Building 2059": {
            "Day": "M",
            "Time": "4:10 - 7:00 PM"
        },
        "Wellman Hall 203": {
            "Day": "R",
            "Time": "8:00 - 8:50 AM"
        }
    }
}


data1 = {"40498": {
        "Course Code": "ECS 032A A01",
        "Name": "Intro to Programming",
        "Instructors": [
            "Edwin Solares"
        ],
        "Total": 75,
        "Filled": 75,
        "Max Kleiber Hall 3": {
            "Day": "MWF",
            "Time": "8:00 - 8:50 AM"
        },
        "Olson Hall 146": {
            "Day": "M",
            "Time": "9:00 - 9:50 AM"
        }
    },
    "40499": {
        "Course Code": "ECS 032A A02",
        "Name": "Intro to Programming",
        "Instructors": [
            "Edwin Solares"
        ],
        "Total": 75,
        "Filled": 75,
        "Max Kleiber Hall 3": {
            "Day": "MWF",
            "Time": "8:00 - 8:50 AM"
        },
        "Olson Hall 146": {
            "Day": "W",
            "Time": "9:00 - 9:50 AM"
        }
    },
    "40500": {
        "Course Code": "ECS 032A A03",
        "Name": "Intro to Programming",
        "Instructors": [
            "Edwin Solares"
        ],
        "Total": 75,
        "Filled": 75,
        "Max Kleiber Hall 3": {
            "Day": "MWF",
            "Time": "8:00 - 8:50 AM"
        },
        "Olson Hall 146": {
            "Day": "F",
            "Time": "9:00 - 9:50 AM"
        }
    },
    "40504": {
        "Course Code": "ECS 032A B01",
        "Name": "Intro to Programming",
        "Instructors": [
            "Kristian Stevens"
        ],
        "Total": 97,
        "Filled": 96,
        "Peter A Rock Hall 194": {
            "Day": "TR",
            "Time": "1:40 - 3:00 PM"
        },
        "Wellman Hall 26": {
            "Day": "T",
            "Time": "3:10 - 4:00 PM"
        }
    },
    "40505": {
        "Course Code": "ECS 032A B02",
        "Name": "Intro to Programming",
        "Instructors": [
            "Kristian Stevens"
        ],
        "Total": 97,
        "Filled": 97,
        "Peter A Rock Hall 194": {
            "Day": "TR",
            "Time": "1:40 - 3:00 PM"
        },
        "Wellman Hall 26": {
            "Day": "R",
            "Time": "3:10 - 4:00 PM"
        }
    },
    "40506": {
        "Course Code": "ECS 032A B03",
        "Name": "Intro to Programming",
        "Instructors": [
            "Kristian Stevens"
        ],
        "Total": 96,
        "Filled": 96,
        "Peter A Rock Hall 194": {
            "Day": "TR",
            "Time": "1:40 - 3:00 PM"
        },
        "Wellman Hall 226": {
            "Day": "R",
            "Time": "4:10 - 5:00 PM"
        }
    }}



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
                if f"{key}: {d}, {t}" not in hDict:
                    hDict[f"{key}: {d}, {t}"] = [CRN]
                else:
                    hDict[f"{key}: {d}, {t}"].append(CRN)

    sorted_dict = dict(sorted(hDict.items(), key=lambda x: len(x[1]), reverse=True))
    for i in sorted_dict:
        print(i, sorted_dict[i])

    for loc in sorted_dict:
        for crn in sorted_dict[loc]:
            if crn not in lecs:
                lecs[crn] = loc
            elif crn not in dis:
                dis[crn] = loc
            else:
                lab[crn] = loc

    groups = group_keys_by_values(lecs)

    return groups, lecs, dis, lab


import pandas as pd

def getCourseInfo(selected_course=None):
    if selected_course:
        classData = {}
        dataFrames, LecInfo = [], []

        crns = courses_list[selected_course]
        for crn in crns:
            classData[crn] = total_data[crn]
    else:
        classData = data
    groups, lecs, diss, lab = (group_courses(classData))

    print(len(groups))


    # print(groups)
    # print("_"*20)
    # pp.pprint(lecs)
    # print("_"*20)
    # pp.pprint(diss)
    # print("_"*20)


    for loc in groups:
        infoDict = {"Course Code": [],
                    "Locations": [],
                    "Instructors": [],
                    "Filled/Total": []
                    }
        f, l = classData[groups[loc][0]]["Course Code"], classData[groups[loc][-1]]["Course Code"]
        # if len(f.split()) == 3:
        seq = f + f"-{l.split()[-1]}"
        LecInfo.append((seq, loc))

        
        for crn in groups[loc]:
            tf = f'{classData[crn]["Filled"]}/{classData[crn]["Total"]}'
            infoDict["Course Code"].append(classData[crn]["Course Code"])
            infoDict["Locations"].append(diss[crn])
            if crn in lab:
                infoDict["Locations"].append(lab[crn])

            infoDict["Instructors"].append(" ".join(classData[crn]["Instructors"]))
            infoDict["Filled/Total"].append(tf)

        dataFrames.append(pd.DataFrame(infoDict))

    return dataFrames, LecInfo
    pp.pprint(dataFrames)

    pp.pprint(LecInfo)




    


getCourseInfo()

