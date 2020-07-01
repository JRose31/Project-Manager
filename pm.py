import sqlite3
import tkinter as tk
from tkinter.ttk import *
from datetime import datetime
from functools import partial



blue = '#93bbfa'
grey = "#e3e3e3"
all_tasks = []

#create database
def addProject():
    global all_tasks

    task_entries = createProject.f3.winfo_children()
    for itask in task_entries:
        if itask.winfo_class() == 'Entry':
            task_text = itask.get()
            all_tasks.append(task_text)

    print(all_tasks)
    try:
        edd = createProject.edd
        epn = createProject.epn
        edesc = createProject.edesc
        cdate = str(datetime.now().strftime("%Y:%m:%d"))
        ddate = edd.get()
        pname = epn.get()
        desc = edesc.get("1.0",'end-1c')
        sqltasks = str(all_tasks).replace("' ", "").replace("'", "").replace("[", "").replace("]", "")
        sqliteConnection = sqlite3.connect('projectManage.db')
        sqlite_create_table_query = '''CREATE TABLE project_one (
                                        createDate TEXT,
                                        dueDate TEXT,
                                        projectName TEXT,
                                        projectDescription,
                                        tasks TEXT);'''

        cursor = sqliteConnection.cursor()
        print("Successfully connected to SQLite!")

        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created!")

        sqlite_insert_with_param = '''
        INSERT INTO 'project_one'
        ('createDate', 'dueDate', 'projectName', 'projectDescription', 'tasks')
        VALUES (?, ?, ?, ?, ?);'''

        data_tuple = (cdate, ddate, pname, desc, sqltasks)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Project '" + pname + "' created!")

        query = cursor.execute("SELECT * FROM project_one")
        print(query.fetchall())

        createProject.win.destroy()
        openProject(pname)

    except:
        cdate = str(datetime.now().strftime("%Y:%m:%d"))
        ddate = edd.get()
        pname = epn.get()
        desc = edesc.get("1.0",'end-1c')
        sqltasks = str(all_tasks).replace("'", "").replace("[", "").replace("]", "")
        print("Table already exists...moving on...")

        sqlite_insert_with_param = '''
        INSERT INTO 'project_one'
        ('createDate', 'dueDate', 'projectName', 'projectDescription', 'tasks')
        VALUES (?, ?, ?, ?, ?);'''

        data_tuple = (cdate, ddate, pname, desc, sqltasks)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()

        query = cursor.execute("SELECT * FROM project_one")
        print(query.fetchall())

        createProject.win.destroy()
        openProject(pname)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

def insert_task():

    next_entry = tk.Entry(createProject.f3)
    next_entry.grid(row=createProject.gridCount, column=0)
    getEntry = next_entry.get()
    #all_tasks.append(getEntry)
    next_button = tk.Button(createProject.f3, text='+', fg=blue, command=insert_task).grid(row=createProject.gridCount, column=1)
    createProject.gridCount += 1

tasks = {}
def deleteTask(task):
    global tasks
    deleteTask.project = openProject.currentProject
    deleteTask.delTask = tasks[task.widget]
    print(deleteTask.delTask)
    print(deleteTask.project)

    deleteTask.win = tk.Tk()
    deleteTask.win.title("Attention!")
    attention = tk.Label(deleteTask.win, text="Delete task?")
    attention.pack()
    ops = tk.Frame(deleteTask.win)
    ops.pack()
    yes = tk.Button(ops, text="Yes", command=confirmDeletion)
    yes.grid(row=0, column=0)
    no = tk.Button(ops, text="No", command=nayDeletion)
    no.grid(row=0, column=1)
    deleteTask.win.mainloop()

def nayDeletion():
    deleteTask.win.destroy()

def confirmDeletion():
    print("Deletetion confirmed")
    print("Delete task at index: ",deleteTask.delTask)
    print("From project: ", deleteTask.project)
    sqliteConnection = sqlite3.connect("projectManage.db")
    cursor = sqliteConnection.cursor()
    query = "SELECT tasks FROM project_one WHERE projectName = ?"
    getTask = cursor.execute(query, (deleteTask.project,))
    task_tup = list(i for i in getTask)[0]
    task_string = task_tup[0]
    new_list = task_string.split(",")
    print(new_list)
    del new_list[deleteTask.delTask]
    print(new_list)
    sqltasks = str(new_list).replace("' ", "").replace("'", "").replace("[", "").replace("]", "")
    updateQuery = "UPDATE project_one SET tasks = ? WHERE projectName = ?"
    commitUpdate = cursor.execute(updateQuery, (sqltasks, deleteTask.project))
    sqliteConnection.commit()

def createProject():
    entryWindow.win.destroy()
    createProject.win = tk.Tk()
    createProject.win.title('Project Manager Creater')

    f0 = tk.Frame(createProject.win)
    f0.pack()
    back = tk.Button(f0, text="Go back", fg='red', command=entryWindow)
    back.pack(side='left')

    ftitle = tk.Frame(createProject.win)
    ftitle.pack()
    spacer0 = tk.Label(ftitle)
    spacer0.pack()
    title = tk.Label(ftitle, text='Create New Project', font='Helvetica 16 bold')
    title.pack()

    f1 = tk.Frame(createProject.win)
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

    fd = tk.Frame(createProject.win)
    fd.pack()
    ldesc = tk.Label(fd, text="Project Description", font='Helvetica 12 bold')
    ldesc.pack()
    createProject.edesc = tk.Text(fd, width=35, height=5)
    createProject.edesc.pack()

    f2 = tk.Frame(createProject.win)
    f2.pack()
    tl = tk.Label(f2, text='Tasks', font='Helvetica 11 bold').grid(row=0)



    createProject.f3 = tk.Frame(createProject.win)
    createProject.f3.pack()
    createProject.et1 = tk.Entry(createProject.f3)
    createProject.et1.grid(row=0, column=0)
    getEntry = createProject.et1.get()
    #all_tasks.append(getEntry)
    bt1 = tk.Button(createProject.f3, text='+', fg=blue, command=insert_task).grid(row=0, column=1)
    createProject.gridCount = 1

    f4 = tk.Frame(createProject.win)
    f4.pack()
    create = tk.Button(f4, text='Create', fg=blue, command=addProject)
    create.pack()

    createProject.win.mainloop()

def showProjects():
    win = tk.Tk()
    win.title('Projects')

    f1 = tk.Frame(win)
    f1.pack()
    back = tk.Button(f1, text="Go back", fg='red', command=entryWindow)
    back.pack(side='left')

    f2 = tk.Frame(win)
    f2.pack()
    welcome = tk.Label(f2, text="Your Projects", font='Helvetica 14 bold').grid(row=0)
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
        tk.Button(f2, text=i[0], command=partial(openProject, i[0])).grid(row=counter)
        counter += 1

    entryWindow.win.destroy()
    openProject.win.destroy()
    win.mainloop()

def openProject(projectName):
    global tasks
    openProject.currentProject = projectName
    openProject.win = tk.Tk()
    openProject.win.title(projectName)

    f1 = tk.Frame(openProject.win)
    f1.pack()
    back = tk.Button(f1, text="Go back", fg='red', command=showProjects)
    back.pack(side='left')


    title = tk.Label(f1, text=projectName, font='Helvetica 12 bold')
    title.pack()
    sqliteConnection = sqlite3.connect('projectManage.db')
    cursor = sqliteConnection.cursor()
    Query = "SELECT tasks FROM project_one WHERE projectName = ?"
    taskQuery = cursor.execute(Query, (projectName,))
    Querylist = list(i for i in taskQuery)
    individualTask = (Querylist[0][0]).split(",")
    print(individualTask)

    f2 = tk.Frame(openProject.win)
    f2.pack()
    counter = 0
    for i in individualTask:
        task = tk.Button(f2, text=i)
        tasks[task] = counter
        task.bind("<Button-1>", deleteTask)
        task.grid(row=counter)
        tk.Checkbutton(f2, onvalue = 1, offvalue = 0).grid(row=counter, column=1)
        counter += 1
    f3 = tk.Frame(openProject.win)
    f3.pack()
    complete = tk.Button(f3, text="Complete", fg=blue)
    complete.pack()

    openProject.win.mainloop()


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
