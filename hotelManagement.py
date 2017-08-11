import sqlite3
import os

import sys

databaseexisted = os.path.isfile('cronhoteldb.db')
dbcon = sqlite3.connect('cronhoteldb.db')
cursor = dbcon.cursor()


def main(args):
    config = args[1]
    create_tables()
    fill_tables(config)
    close()


def close():
    dbcon.commit()
    dbcon.close()


def create_tables():
    with dbcon:
        cursor.execute("CREATE TABLE TaskTimes(TaskId integer PRIMARY KEY NOT NULL,"
                       "DoEvery integer NOT NULL, "
                       "NumTimes integer NOT NULL)")

        cursor.execute("CREATE TABLE Tasks("
                       "TaskId integer NOT NULL REFERENCES TaskTimes(TaskId),"
                       "TaskName text NOT NULL,"
                       "Parameter integer)")

        cursor.execute("CREATE TABLE Rooms(RoomNumber integer PRIMARY KEY NOT NULL)")

        cursor.execute("CREATE TABLE Residents("
                       "RoomNumber integer NOT NULL REFERENCES Rooms(RoomNumber),"
                       "FirstName text NOT NULL,"
                       "LastName text NOT NULL)")


def fill_tables(config):
    counter = 0
    file = open(config, 'r')
    for line in file:
        words = line.strip('\n').split(',')
        if words[0] == "room":
            cursor.execute("INSERT INTO Rooms VALUES(?)", (words[1],))
            dbcon.commit()
            if len(words) > 2:
                cursor.execute("INSERT INTO Residents VALUES(?,?,?)", (words[1], words[2], words[3],))
        elif words[0] == "clean":
            cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (counter, words[0], 0,))
            cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (counter, words[1], words[2],))
            counter += 1
        else:
            cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (counter, words[0], words[2],))
            cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (counter, words[1], words[3],))
            counter += 1

if __name__ == '__main__' and not databaseexisted:
    main(sys.argv)
