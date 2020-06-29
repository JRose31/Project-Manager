import sqlite3
import tkinter as tk
from tkinter.ttk import *
from datetime import datetime
from functools import partial



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
    entryWindow.win.destroy()
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

def showProjects():
    entryWindow.win.destroy()
    win = tk.Tk()
    win.title('Projects')
    welcome = tk.Label(win, text="Your Projects", font='Helvetica 14 bold').grid(row=0)
    sqliteConnection = sqlite3.connect('projectManage.db')
    cursor = sqliteConnection.cursor()
    Query = "SELECT projectName FROM project_one"
    projectQuery = cursor.execute(Query)
    projects = list(i for i in projectQuery)
    counter = 1
    print(projects)
    for i in projects:
        projectName = i[0]
        print(projectName)
        tk.Button(win, text=i[0], command=partial(openProject, i[0])).grid(row=counter)
        counter += 1

    win.mainloop()

def openProject(projectName):
    win = tk.Tk()
    win.title(projectName)
    title = tk.Label(win, text=projectName, font='Helvetica 12 bold')
    title.pack()
    sqliteConnection = sqlite3.connect('projectManage.db')
    cursor = sqliteConnection.cursor()
    Query = "SELECT tasks FROM project_one WHERE projectName = ?"
    taskQuery = cursor.execute(Query, (projectName,))
    f1 = tk.Frame(win)
    f1.pack()
    counter = 0
    for i in taskQuery:
        tk.Label(f1, text=i[0]).grid(row=counter)
        counter += 1
    win.mainloop()


def entryWindow():

    entryWindow.win = tk.Tk()
    entryWindow.win.title("Project Manager (1.0)")
    welcome = tk.Label(entryWindow.win, text='Welcome to Project Manager 1.0!', font='Helvetica 14 bold')
    welcome.pack()

    f1 = tk.Frame(entryWindow.win)
    f1.pack()
    existing = tk.Button(f1, text="Existing Projects", command=showProjects)
    existing.grid(row=0)
    createNew = tk.Button(f1, text="Create New Project", fg=blue, command=createProject)
    createNew.grid(row=1)

    entryWindow.win.mainloop()

entryWindow()
