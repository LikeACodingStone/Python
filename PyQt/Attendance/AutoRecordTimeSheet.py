import win32evtlog
import datetime
import subprocess
import re
import csv

def get_wake_events():
    server = 'localhost'
    log_type = 'System'
    wake_event_id = 1
    events = []
    try:
        hand = win32evtlog.OpenEventLog(server, log_type)
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        while True:
            records = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)
            if not records:
                break

            for record in records:
                if record.EventID == wake_event_id:
                    event_time = record.TimeGenerated
                    events.append(event_time)

    except Exception as e:
        print(f"Error accessing event log: {e}")
    finally:
        win32evtlog.CloseEventLog(hand)
    return events


def splitTimeList(dateTime):
    formatTm = dateTime.strftime("%Y-%m-%d-%H-%M-%S")
    tmList = formatTm.split("-")
    return tmList

def getWakeUpMonthData(monthMap):
    mothDataMapNew = {}
    for keyDate, keyTime in monthMap.items():
        sizeTime = len(keyTime)
        if sizeTime == 1:
            mothDataMapNew[keyDate] = keyTime
            print(keyTime)
        else:
            minMiniutes = 66666
            for tmVale in keyTime:
                tmMinutes = int(tmVale[3]) *60 + int(tmVale[4])
                if int(tmVale[3]) > 8 and int(tmVale[3]) < 15:
                    if tmMinutes < minMiniutes:
                        minMiniutes = tmMinutes
                        mothDataMapNew[keyDate] = tmVale
                    break
    return mothDataMapNew


def getWakeUpAllData():
    wakeEvents = get_wake_events()
    curTime = datetime.datetime.now()
    curTmList = splitTimeList(curTime)
    monthMapData = {}
    for event in wakeEvents:
        eventTmList = splitTimeList(event)
        if int(curTmList[0]) == int(eventTmList[0])   \
            and int(curTmList[1]) == int(eventTmList[1]):
                if eventTmList[2] in monthMapData:
                    monthMapData[eventTmList[2]].append(eventTmList)
                else:
                    monthMapData[eventTmList[2]] = []
                    monthMapData[eventTmList[2]].append(eventTmList)
            
    newMonthData = getWakeUpMonthData(monthMapData)
    return newMonthData


# Bellow is the shutdown and lock screen data

def getShouDownData():
    command = "Get-WinEvent -LogName System | Where-Object { $_.Id -eq 1074 -or $_.Id -eq 6006 -or $_.Id -eq 6008 }"
    process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    if process.returncode == 0:
        pattern = r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})"
        matchs = re.findall(pattern, output)
        return matchs
    
def getShutDownMonthList():
    matchList = getShouDownData()
    curTime = datetime.datetime.now()
    curTmList = splitTimeList(curTime)
    shutDownList = []
    for times in matchList:
        dateTmList = []
        dateListFirst = times.split(" ")
        dateListHead = dateListFirst[0].split("/")
        dateListTail = dateListFirst[1].split(":")
        if int(curTmList[0]) == int(dateListHead[2]) and int(curTmList[1]) == int(dateListHead[1]):
            dateTmList.append(dateListHead[2])
            dateTmList.append(dateListHead[1])
            dateTmList.append(dateListHead[0])
            dateTmList.append(dateListTail[0])
            dateTmList.append(dateListTail[1])
            dateTmList.append(dateListTail[2])
            shutDownList.append(dateTmList)

    return shutDownList


def getLockSceecnList():
    curTime = datetime.datetime.now()
    curTmList = splitTimeList(curTime)
    lockScreenList = []
    with open("C:\\Users\\a1294.zhou\\WorkingFiles\\NotePad_Files\\Log_shutdown\\winL_Log.txt", "r") as f:
        readLines = f.readlines()
        for lineCont in readLines:
            dateContList = lineCont.split(":::")[1].split("-")
            if int(dateContList[0]) == int(curTmList[0]) and int(dateContList[1]) == int(curTmList[1]):
                lockScreenList.append(dateContList)
    return lockScreenList

def getLatestMonthList():
    lockScreenList = getLockSceecnList()
    shutDownList = getShutDownMonthList()
    for lockTime in lockScreenList:
        print(lockTime)
        #shutDownList.append(lockTime)
    mapLatest = {}
    for tmList in shutDownList:
        if tmList[2] in mapLatest:
            mapLatest[tmList[2]].append(tmList)
        else:
            mapLatest[tmList[2]] = []
            mapLatest[tmList[2]].append(tmList)
    
    
    mothDataMapLateNew = {}
    for keyDate, keyTime in mapLatest.items():
        sizeTime = len(keyTime)
        if sizeTime == 1:
            mothDataMapLateNew[keyDate] = keyTime
        else:
            maxTmMiniutes = 0
            for tmVale in keyTime:
                tmMinutes = int(tmVale[3]) *60 + int(tmVale[4])
                if int(tmVale[3]) > 15 and int(tmVale[3]) < 21:
                    if tmMinutes > maxTmMiniutes:
                        maxTmMiniutes = tmMinutes
                        mothDataMapLateNew[keyDate] = tmVale
    return mothDataMapLateNew
                  


def ControlManage():
    wakeUpMap = getWakeUpAllData() 
    mothDataMapLateNew = getLatestMonthList()
    sortedLateMonthData = dict(sorted(mothDataMapLateNew.items()))
  
    csvListTitle = [["Date", "PCWakeUp_Time", "PC_DeadTime"]]
    for date, fullList in wakeUpMap.items():
        insertList = []
        if isinstance(fullList, bool):
            print("bool full ", fullList)
            continue
        if isinstance(fullList, list) and len(fullList) == 1:
            fullList = fullList[0]
        wakeupDate = fullList[0] + "/" + fullList[1]  + "/" + fullList[2]
        wakeupTime = fullList[3] + ":" + fullList[4]
        insertList.append(wakeupDate)
        insertList.append(wakeupTime)
        if date in sortedLateMonthData:
            deadTmList = sortedLateMonthData[date]
            deadTime = deadTmList[3] + ":" + deadTmList[4]          
            insertList.append(deadTime)   
            del sortedLateMonthData[date]
        else:
            insertList.append("Dead")
        csvListTitle.append(insertList)

    for date, fullList in sortedLateMonthData.items():
        insertList = []
        deadDate = fullList[0] + "/" + fullList[1]  + "/" + fullList[2]
        deadTime = fullList[3] + ":" + fullList[4]
        insertList.append(deadDate)
        insertList.append("NoneWakeup")
        insertList.append(deadTime)
        csvListTitle.append(insertList)
    
    curTime = datetime.datetime.now()
    formatTm = curTime.strftime("%m_%d_%H_%M")
    fileName = "JIMIPAGE_" + formatTm + ".csv"
    with open(fileName, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csvListTitle)
        file.close()
    return fileName
