import sqlite3
import time

dbcon = sqlite3.connect('cronhoteldb.db')
cursor = dbcon.cursor()


def dohoteltask(taskname, parameter):
    timer = time.time()

    with dbcon:
        # task_id = cursor.execute("SELECT TaskId FROM Tasks WHERE TaskName=(?)", (taskname,)).fetchone()
        # do_every = cursor.execute("SELECT DoEvery FROM TaskTimes WHERE TaskId=(?)", (0,)).fetchone()
        if taskname[0] == "wakeup" or taskname[0] == "breakfast":
            first_name = cursor.execute("SELECT FirstName From Residents WHERE RoomNumber=(?)", parameter).fetchone()
            last_name = cursor.execute("SELECT LastName From Residents WHERE RoomNumber=(?)", parameter).fetchone()
            if taskname[0] == "breakfast":
                print(str(first_name[0]) + " " + str(last_name[0]) + " in room " + str(parameter[0])
                      + " has been served breakfast at " + str(time.time()))
            else:
                print(str(first_name[0]) + " " + str(last_name[0]) + " in room " + str(
                    parameter[0]) + " received a wakeup call at "
                      + str(time.time()))
        else:
            rooms = cursor.execute("SELECT Room1.RoomNumber FROM Rooms Room1 LEFT JOIN Residents Room2 ON "
                                   "Room2.RoomNumber= "
                                   "Room1.RoomNumber WHERE Room2.RoomNumber IS NULL ").fetchall()
            output = "Rooms "
            for room in rooms:
                output = output + str(room[0]) + ", "
            output = output[:-2]
            print(output + " were cleaned at " + str(timer))
    return timer
