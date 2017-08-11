import sqlite3
import os
import hotelWorker
import time

databaseexisted = os.path.isfile('cronhoteldb.db')
dbcon = sqlite3.connect('cronhoteldb.db')
cursor = dbcon.cursor()


def main():
    with dbcon:
        num_times = cursor.execute("SELECT NumTimes FROM TaskTimes ").fetchall()
        iteration = 0
        when_to_do_next = []

        while databaseexisted and num_times.count((0,)) != len(num_times):

            if iteration == 0:
                tasks = cursor.execute("SELECT* FROM Tasks").fetchall()
                for task in tasks:
                    task_id, taskname, parameter = task
                    timer = hotelWorker.dohoteltask((taskname,), (parameter,))
                    when_to_do_next.append(timer)
                    cursor.execute("UPDATE TaskTimes SET NumTimes=(NumTimes-1) WHERE TaskId = (?)", (task_id,))
                iteration = 1

            else:
                task_times = cursor.execute("SELECT * FROM TaskTimes").fetchall()
                for task_time in task_times:
                    task_id, do_every, numtimes = task_time
                    if int(time.time() - when_to_do_next[task_id]) == do_every and numtimes > 0:
                        taskname = cursor.execute("SELECT TaskName FROM Tasks WHERE TaskId=(?)", (task_id,)).fetchone()
                        parameter = cursor.execute("SELECT Parameter FROM Tasks WHERE TaskId=(?)",
                                                   (task_id,)).fetchone()
                        when_to_do_next[task_id] = hotelWorker.dohoteltask(taskname, parameter)
                        cursor.execute("UPDATE TaskTimes SET NumTimes=(NumTimes-1) WHERE TaskId=(?)", (task_id,))

            num_times = cursor.execute("SELECT NumTimes FROM TaskTimes WHERE NumTimes>0 ").fetchall()


if __name__ == '__main__':
    main()
