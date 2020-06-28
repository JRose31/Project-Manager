import sqlite3
from tkinter import *
from datetime import datetime

#create database
def createProject(cdate, ddate, pname, tasks):
    try:
        sqliteConnection = sqlite3.connect('projectManage.db')
        sqlite_create_table_query = '''CREATE TABLE project_one (
                                        createDate TEXT,
                                        dueDate TEXT,
                                        projectName TEXT,
                                        tasks TEXT);'''

        cursor = sqliteConnection.cursor()
        print("Successfully connected to SQLite!")

        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created!")

        sqlite_insert_with_param = '''
        INSERT INTO 'project_one'
        ('createDate', 'dueDate', 'projectName', 'tasks')
        VALUES (?, ?, ?, ?);'''

        data_tuple = (cdate, ddate, pname, tasks)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Project '" + pname + "' created!")

        query = cursor.execute("SELECT * FROM project_one")
        print(query.fetchall())

    except:
        print("Table already exists...moving on...")

        query = cursor.execute("SELECT * FROM project_one")
        print(query.fetchall())

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

def insert_task():
    global gridCount
    global bt1

    Entry(f3).grid(row=gridCount, column=0)
    next_button = Button(f3, text='+', fg=blue, command=insert_task).grid(row=gridCount, column=1)
    gridCount += 1





blue = '#93bbfa'

win = Tk()
win.title('Project Manager')

ftitle = Frame(win)
ftitle.pack()
spacer0 = Label(ftitle)
spacer0.pack()
title = Label(ftitle, text='Create New Project', font='Helvetica 16 bold')
title.pack()

f1 = Frame(win)
f1.pack()
spacer1 = Label(f1).grid(row=0)
pn = Label(f1, text='Project Name', font='Helvetica 12 bold').grid(row=1)
dd = Label(f1, text='Due Date', font='Helvetica 12 bold').grid(row=2)
epn = Entry(f1).grid(row=1, column=1)
edd = Entry(f1)
edd.insert(0, 'YYYY/MM/DD')
edd.grid(row=2, column=1)
spacer2 = Label(f1).grid(row=3)

f2 = Frame(win)
f2.pack()
tl = Label(f2, text='Tasks', font='Helvetica 11 bold').grid(row=0)



f3 = Frame(win)
f3.pack()
et1 = Entry(f3).grid(row=0, column=0)
bt1 = Button(f3, text='+', fg=blue, command=insert_task).grid(row=0, column=1)
gridCount = 1

f4 = Frame(win)
f4.pack()
create = Button(f4, text='Create', fg=blue)
create.pack()

win.mainloop()
