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
    next_button = tk.Button(createProject.f3, text='+', fg=blue, command=insert_task).grid(row=createProject.gridCount, column=1)
    createProject.gridCount += 1

def insert_task_existing():

    next_entry = tk.Entry(openProject.f3)
    next_entry.grid(row=openProject.gridCount, column=0)
    next_button = tk.Button(openProject.f3, text='+', fg=blue, command=insert_task_existing).grid(row=openProject.gridCount, column=1)
    openProject.gridCount += 1

def add_task_db(projectName):
    localTasks = []
    counter = 0
    task_entries = openProject.f3.winfo_children()
    for itask in task_entries:
        if itask.winfo_class() == 'Entry':
            if len(itask.get()) > 1:
                counter +=1


    if counter > 0:
        sqliteConnection = sqlite3.connect("projectManage.db")
        cursor = sqliteConnection.cursor()

        task_entries = openProject.f3.winfo_children()
        for itask in task_entries:
            if itask.winfo_class() == 'Entry':
                task_text = itask.get()
                localTasks.append(task_text)
        print(localTasks)
        sqltasks = ", " + str(localTasks).replace("' ", "").replace("'", "").replace("[", "").replace("]", "")
        update_tasks = "UPDATE project_one SET tasks = tasks || ? WHERE projectName = ?"
        cursor.execute(update_tasks, (sqltasks, projectName))
        sqliteConnection.commit()


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
    no = tk.Button(ops, text="No", command=nayTaskDeletion)
    no.grid(row=0, column=1)
    deleteTask.win.mainloop()

def nayTaskDeletion():
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
    deleteTask.win.destroy()
    openProject(deleteTask.project, refresh=True)


def createProject():

    createProject.win = tk.Tk()
    createProject.win.title('Project Manager Creater')

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
    bt1 = tk.Button(createProject.f3, text='+', fg=blue, command=insert_task).grid(row=0, column=1)
    createProject.gridCount = 1

    f4 = tk.Frame(createProject.win)
    f4.pack()
    create = tk.Button(f4, text='Create', fg=blue, command=addProject)
    create.pack()

    createProject.win.mainloop()

def projectOptions(projectName):
    projectOptions.win = tk.Tk()
    projectOptions.win.title("Project Options")
    f1 = tk.Frame(projectOptions.win)
    f1.pack()
    title = tk.Label(f1, text=projectName).pack()
    f2 = tk.Frame(projectOptions.win)
    f2.pack()
    delete = tk.Button(f2, text="Delete Project", command=lambda: deleteConfirm(projectName))
    delete.grid(row=0, column=0)
    duedate = tk.Button(f2, text="Change Due Date", command=lambda: enterDueDate(projectName))
    duedate.grid(row=0, column=1)
    projectOptions.win.mainloop()

def enterDueDate(projectName):
    enterDueDate.win = tk.Tk()
    title = tk.Label(enterDueDate.win, text="New Due Date", font="Helvetica 12 bold")
    title.pack()

    f1 = tk.Frame(enterDueDate.win)
    f1.pack()
    enterDueDate.newDate = tk.Entry(f1)
    enterDueDate.newDate.insert(0, 'YYYY/MM/DD')
    enterDueDate.newDate.grid(row=0)
    submit = tk.Button(f1, text="Confirm", fg='green', command=lambda: changeDueDate(projectName))
    submit.grid(row=0, column=1)

    enterDueDate.win.mainloop()

def changeDueDate(projectName):
    newDueDate = enterDueDate.newDate.get()
    print(newDueDate)
    sqliteConnection = sqlite3.connect("projectManage.db")
    cursor = sqliteConnection.cursor()
    Query = "UPDATE project_one SET dueDate = ? WHERE projectName = ? "
    cursor.execute(Query, (newDueDate, projectName))
    sqliteConnection.commit()
    sqliteConnection.close()
    enterDueDate.win.destroy()
    projectOptions.win.destroy()
    showProjects.win.destroy()
    showProjects()

def deleteConfirm(projectName):
    deleteConfirm.win= tk.Tk()
    deleteConfirm.win.title("Confirm Project Deletion")
    f0 = tk.Frame(deleteConfirm.win)
    f0.pack()
    tk.Label(f0, text=("Delete project:")).grid(row=0)
    tk.Label(f0, text=projectName, font='Helvetica 12 bold').grid(row=0, column=1)
    f1 = tk.Frame(deleteConfirm.win)
    f1.pack()
    yes = tk.Button(f1, text="Yes", fg='green', command=lambda: confirmProjectDeletion(projectName))
    yes.grid(row=0)
    no = tk.Button(f1, text="No", fg='red', command=nayProjectDeletion)
    no.grid(row=0, column=1)
    deleteConfirm.win.mainloop()

def nayProjectDeletion():
    deleteConfirm.win.destroy()

def confirmProjectDeletion(projectName):
    sqliteConnection = sqlite3.connect("projectManage.db")
    cursor = sqliteConnection.cursor()
    deleteQuery = "DELETE FROM project_one WHERE projectName = ?"
    cursor.execute(deleteQuery, (projectName,))
    sqliteConnection.commit()
    deleteConfirm.win.destroy()
    projectOptions.win.destroy()
    showProjects()


showProjectsOpen = False
def showProjects():
    global showProjectsOpen
    '''if showProjectsOpen == True:
        showProjects.win.destroy()'''
    showProjectsOpen = True
    showProjects.win = tk.Tk()
    showProjects.win.geometry("350x250")
    showProjects.win.title('Projects')

    f1 = tk.Frame(showProjects.win)
    f1.pack(anchor='nw')
    tk.Label(f1).pack()

    f2 = tk.Frame(showProjects.win)
    f2.pack()
    welcome = tk.Label(f2, text="Your Projects", font='Helvetica 14 bold').grid(row=0)
    dds = tk.Label(f2, text="Due Date", font='Helvetica 14 bold').grid(row=0, column=1)
    sqliteConnection = sqlite3.connect('projectManage.db')
    cursor = sqliteConnection.cursor()
    Query = "SELECT projectName FROM project_one"
    projectQuery = cursor.execute(Query)
    projects = list(i for i in projectQuery)
    sqliteConnection.close()
    sqliteConnection = sqlite3.connect('projectManage.db')
    cursor = sqliteConnection.cursor()
    Query = "SELECT dueDate FROM project_one"
    ddQuery = cursor.execute(Query)
    duedates = list(i for i in ddQuery)
    counter = 1
    print(projects)
    for i, n in zip(projects, duedates):
        projectName = i[0]
        print(projectName)
        tk.Button(f2, text=i[0], command=partial(openProject, i[0])).grid(row=counter)
        tk.Label(f2, text=n[0]).grid(row=counter, column=1)
        tk.Button(f2, text="...", command=partial(projectOptions, i[0])).grid(row=counter, column=2)
        counter += 1
    global openProjectOpen

    if openProjectOpen == True:
        openProject.win.destroy()
    showProjects.win.mainloop()

openProjectOpen = False

def openProject(projectName, refresh=False):
    if refresh == True:
        add_task_db(projectName)
        openProject.win.destroy()
    global openProjectOpen
    openProjectOpen = True
    global tasks
    openProject.currentProject = projectName
    openProject.win = tk.Tk()
    openProject.win.geometry("350x300")
    openProject.win.title(projectName)

    f0 = tk.Frame(openProject.win)
    f0.pack(anchor='nw')
    back = tk.Button(f0, text="Go back", fg='red', borderwidth=1, relief="solid", command=showProjects)
    back.pack()
    tk.Label(f0).pack()

    f0 = tk.Frame(openProject.win)
    f0.pack()
    title = tk.Label(f0, text=projectName, font='Helvetica 15 bold')
    title.pack()
    sqliteConnection = sqlite3.connect("projectManage.db")
    cursor = sqliteConnection.cursor()
    Query = "SELECT projectDescription FROM project_one WHERE projectName = ?"
    descQuery = cursor.execute(Query,(projectName,))
    description = list(i for i in descQuery)[0][0]
    desc = tk.Label(f0, text=description)
    desc.pack()
    sqliteConnection.close()

    f1 = tk.Frame(openProject.win)
    f1.pack()
    sqliteConnection = sqlite3.connect("projectManage.db")
    cursor = sqliteConnection.cursor()
    Query = "SELECT dueDate FROM project_one WHERE projectName = ?"
    ddQuery = cursor.execute(Query,(projectName,))
    dd = list(i for i in ddQuery)[0][0]
    ddlabel = tk.Label(f1, text="Due Date:", font="Helvetica 12 bold").grid(row=0)
    ddset = tk.Label(f1, text=dd).grid(row=0, column=1)
    tk.Label(f1).grid(row=1)
    sqliteConnection.close()

    sqliteConnection = sqlite3.connect('projectManage.db')
    cursor = sqliteConnection.cursor()
    Query = "SELECT tasks FROM project_one WHERE projectName = ?"
    taskQuery = cursor.execute(Query, (projectName,))
    Querylist = list(i for i in taskQuery)
    individualTask = (Querylist[0][0]).split(",")
    print(individualTask)

    f2 = tk.Frame(openProject.win)
    f2.pack()
    tk.Label(f2, text="Current Tasks", font="Helvetica 13 bold").pack()
    counter = 0
    for i in individualTask:
        task = tk.Button(f2, text=i)
        tasks[task] = counter
        task.bind("<Button-1>", deleteTask)
        task.pack(anchor='w')
        counter += 1
    tk.Label(f2).pack()
    addTasks = tk.Label(f2, text="Add Tasks", font="Helvetica 13 bold")
    addTasks.pack()

    openProject.f3 = tk.Frame(openProject.win)
    openProject.f3.pack()
    openProject.et1 = tk.Entry(openProject.f3)
    openProject.et1.grid(row=0, column=0)
    bt1 = tk.Button(openProject.f3, text='+', fg=blue, command=insert_task_existing).grid(row=0, column=1)
    openProject.gridCount = 1

    f4 = tk.Frame(openProject.win)
    f4.pack()
    refresh = tk.Button(f4, text="Refresh", fg=blue, command=lambda: openProject(projectName, refresh=True))
    refresh.pack()

    openProject.win.mainloop()


def entryWindow():

    entryWindow.win = tk.Tk()
    entryWindow.win.geometry("300x250")
    entryWindow.win.title("Project Manager (1.0)")
    tk.Label(entryWindow.win).pack()
    welcome = tk.Label(entryWindow.win, text='Welcome to \n Project Manager 1.0!', font='Helvetica 14 bold')
    welcome.pack()
    tk.Label(entryWindow.win).pack()

    f1 = tk.Frame(entryWindow.win)
    f1.pack()
    existing = tk.Button(f1, text="Existing Projects", command=showProjects)
    existing.grid(row=0)
    createNew = tk.Button(f1, text="Create New Project", fg=blue, command=createProject)
    createNew.grid(row=1)

    f2 = tk.Frame(entryWindow.win)
    f2.pack(side="bottom")
    tk.Label(f2, text="Created by Jamaine D Roseborough Jr \n github.com/JRose31").pack()

    entryWindow.win.mainloop()

entryWindow()
