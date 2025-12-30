import os



def alarm(Query):
    timehere = open("Database\Alarmtext.txt","a")
    timehere.write(Query)
    timehere.close()
    os.startfile("Alarm.py")
    