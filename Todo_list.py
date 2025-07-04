import datetime
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# --- Setup Root Window ---
root = Tk()
root.title("To-Do List")
root.geometry("400x650+400+100")
root.resizable(False, False)
root.configure(bg="#2C3E50")
root.option_add("*Font", ("Segoe UI", 12))

# --- Global Task List ---
task_list = []

# --- Utility Functions ---
def format_task_text(task, done):
    return f"[{'✓' if done else ' '}] {task}"

def addTask():
    task = task_entry.get().strip()
    task_entry.delete(0, END)

    if task:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        formatted_task = f"{task} ({timestamp})"
        task_list.append((formatted_task, False))
        save_tasks()
        listbox.insert(END, format_task_text(formatted_task, False))
    else:
        messagebox.showwarning("Empty Task", "You must enter a task before adding!")

def save_tasks():
    try:
        with open("task.txt", "w") as file:
            for task, done in task_list:
                file.write(f"{task}|{done}\n")
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save tasks:\n{e}")

def deleteTask():
    global task_list
    selected = listbox.curselection()
    if not selected:
        return
    for index in reversed(selected):
        task_text = listbox.get(index)[4:]  # Remove status prefix
        task_list = [t for t in task_list if t[0] != task_text]
        listbox.delete(index)
    save_tasks()

def toggle_done(event=None):
    global task_list
    selected = listbox.curselection()
    for index in selected:
        task_text = listbox.get(index)[4:]
        for i, (t, done) in enumerate(task_list):
            if t == task_text:
                task_list[i] = (t, not done)
                listbox.delete(index)
                listbox.insert(index, format_task_text(t, not done))
                break
    save_tasks()

def openTaskFile():
    if not os.path.exists("task.txt"):
        open("task.txt", "w").close()

    try:
        task_list.clear()
        listbox.delete(0, END)
        with open("task.txt", "r") as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split("|")
                    task = parts[0]
                    done = parts[1].lower() == "true" if len(parts) > 1 else False
                    task_list.append((task, done))
                    listbox.insert(END, format_task_text(task, done))
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load tasks:\n{e}")

# --- GUI Components ---

# Heading
Label(root, text="My Tasks", font=("Helvetica", 24, "bold"), bg="#2C3E50", fg="white").pack(pady=(20, 10))

# List Frame
frame1 = Frame(root, bg="#2C3E50")
frame1.pack(pady=10)

listbox = Listbox(frame1, width=40, height=15, bg="#2A2A3A", fg="white",
                  selectbackground="#5A5AFF", selectforeground="white", bd=0, highlightthickness=0)
listbox.pack(side=LEFT, fill=BOTH)

scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Entry & Add Button
frame2 = Frame(root, bg="#2C3E50")
frame2.pack(pady=(0, 10))

task_entry = Entry(frame2, width=28, font=("Segoe UI", 16), bd=0, bg="#3B3B4F",
                   fg="white", insertbackground="white", relief=FLAT)
task_entry.grid(row=0, column=0, ipady=8, padx=(0, 10))
task_entry.focus()

add_button = Button(frame2, text="Add", font=("Segoe UI", 12, "bold"), bg="#00C853",
                    fg="white", bd=0, padx=20, pady=10, activebackground="#00B347", command=addTask)
add_button.grid(row=0, column=1)

# Delete Button
frame3 = Frame(root, bg="#2C3E50")
frame3.pack(pady=(10, 20))

try:
    delete_img = Image.open("Task1/delete.png").resize((50, 60), Image.LANCZOS)
    Delete_icon = ImageTk.PhotoImage(delete_img)
    delete_button = Button(frame3, image=Delete_icon, bd=0, bg="#2C3E50",
                           activebackground="#2C3E50", command=deleteTask)
    delete_button.pack()
except:
    delete_button = Button(frame3, text="Delete", font=("Segoe UI", 12, "bold"), bg="#E53935",
                           fg="white", padx=20, pady=10, command=deleteTask)
    delete_button.pack()

# Double click to toggle done status
listbox.bind("<Double-Button-1>", toggle_done)

# Load saved tasks
openTaskFile()

# --- Start App ---
root.mainloop()
