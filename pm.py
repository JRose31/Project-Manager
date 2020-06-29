import sqlite3
import tkinter as tk
from tkinter.ttk import *
from datetime import datetime



blue = '#93bbfa'

#create database
def addProject():
    try:
        edd = createProject.edd
        epn = createProject.epn
        cdate = str(datetime.now().strftime("%Y:%m:%d"))
        ddate = edd.get()
        pname = epn.get()
        tasks = 'Test Task'
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
        cdate = str(datetime.now().strftime("%Y:%m:%d"))
        ddate = edd.get()
        pname = epn.get()
        tasks = 'Test Task'
        print("Table already exists...moving on...")

        sqlite_insert_with_param = '''
        INSERT INTO 'project_one'
        ('createDate', 'dueDate', 'projectName', 'tasks')
        VALUES (?, ?, ?, ?);'''

        data_tuple = (cdate, ddate, pname, tasks)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()

        query = cursor.execute("SELECT * FROM project_one")
        print(query.fetchall())

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

def insert_task():
    global gridCount
    global bt1

    next_entry = tk.Entry(f3)
    next_entry.grid(row=gridCount, column=0)
    next_button = tk.Button(f3, text='+', fg=blue, command=insert_task).grid(row=gridCount, column=1)
    gridCount += 1


def createProject():

    win = tk.Tk()
    win.title('Project Manager Creater')

    ftitle = tk.Frame(win)
    ftitle.pack()
    spacer0 = tk.Label(ftitle)
    spacer0.pack()
    title = tk.Label(ftitle, text='Create New Project', font='Helvetica 16 bold')
    title.pack()

    f1 = tk.Frame(win)
    f1.pack()
    spacer1 = tk.Label(f1).grid(row=0)
    pn = tk.Label(f1, text='Project Name', font='Helvetica 12 bold').grid(row=1)
    dd = tk.Label(f1, text='Due Date', font='Helvetica 12 bold')
    dd.grid(row=2)
    createProject.epn = tk.Entry(f1)
    createProject.epn.grid(row=1, column=1)
    createProject.edd = tk.Entry(f1)
    createProject.edd.insert(0, 'YYYY/MM/DD')
    createProject.edd.grid(row=2, column=1)
    spacer2 = tk.Label(f1).grid(row=3)

    f2 = tk.Frame(win)
    f2.pack()
    tl = tk.Label(f2, text='Tasks', font='Helvetica 11 bold').grid(row=0)



    f3 = tk.Frame(win)
    f3.pack()
    createProject.et1 = tk.Entry(f3)
    createProject.et1.grid(row=0, column=0)
    bt1 = tk.Button(f3, text='+', fg=blue, command=insert_task).grid(row=0, column=1)
    gridCount = 1

    f4 = tk.Frame(win)
    f4.pack()
    create = tk.Button(f4, text='Create', fg=blue, command=addProject)
    create.pack()

    win.mainloop()

def entryWindow():

    win = tk.Tk()
    win.title("Project Manager (1.0)")
    welcome = tk.Label(win, text='Welcome to Project Manager 1.0!', font='Helvetica 14 bold')
    welcome.pack()

    f1 = tk.Frame(win)
    f1.pack()
    existing = tk.Button(f1, text="Existing Project")
    existing.grid(row=0)
    createNew = tk.Button(f1, text="Create New Project", fg=blue, command=createProject)
    createNew.grid(row=1)

    win.mainloop()

entryWindow()
