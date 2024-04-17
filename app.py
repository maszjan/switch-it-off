import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import time


shutdown_time = ""
shutdown_seconds = 0
countdown_label = None
shutdown_thread = None
running = False


def time_to_seconds(time_str):
    try:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60
    except ValueError:
        return -1


def update_countdown_label():
    global shutdown_seconds, countdown_label, running

    while running and shutdown_seconds > 0:
        hours, remainder = divmod(shutdown_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        countdown_label.config(text=f"Shutdown in: {hours:02}:{minutes:02}:{seconds:02}")

        shutdown_seconds -= 1
        time.sleep(1)

    if running:
        if shutdown_seconds <= 0:
            os.system('shutdown /s /f /t 1 /c "Computer will go to sleep"')
        countdown_label.config(text="Shutdown complete")


def start_shutdown_countdown():
    global shutdown_time, shutdown_seconds, shutdown_thread, running

    shutdown_time = entry_time.get().strip()

    if not shutdown_time:
        messagebox.showerror("Error", "Please enter a valid time (HH:MM)")
        return

    seconds = time_to_seconds(shutdown_time)
    if seconds == -1:
        messagebox.showerror("Error", "Invalid time format. Please use HH:MM format")
        return

    shutdown_seconds = seconds
    countdown_label.config(text=f"Shutdown in: {shutdown_time}")

    running = True
    shutdown_thread = threading.Thread(target=update_countdown_label)
    shutdown_thread.daemon = True
    shutdown_thread.start()


def stop_shutdown_countdown():
    global running
    running = False
    if shutdown_thread and shutdown_thread.is_alive():
        shutdown_thread.join()
    countdown_label.config(text="Shutdown cancelled")

# Create main window
root = tk.Tk()
root.title("Computer Sleep Scheduler")
root.configure(bg='#f0f0f0')

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', foreground='black', background='#a1dbcd', font=('Helvetica', 12), width=15)
style.configure('TLabel', foreground='black', background='#f0f0f0', font=('Helvetica', 14))

label_time = ttk.Label(root, text="Specify sleep time (HH:MM):", style='TLabel')
entry_time = ttk.Entry(root, font=('Helvetica', 12), width=15)

button_schedule = ttk.Button(root, text="Schedule Sleep", command=start_shutdown_countdown, style='TButton')

countdown_label = ttk.Label(root, text="", style='TLabel')

button_cancel = ttk.Button(root, text="Cancel", command=stop_shutdown_countdown, style='TButton')


label_time.grid(row=0, column=0, padx=20, pady=10, sticky="e")
entry_time.grid(row=0, column=1, padx=20, pady=10)

button_schedule.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

countdown_label.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

button_cancel.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

root.mainloop()
