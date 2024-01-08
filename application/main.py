import tkinter as tk
from tkinter import *
import subprocess
import threading

def run_bash_script():
    def execute_script():
        try:
            process = subprocess.Popen(
                ["../init.sh"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True
            )
            # Read output line by line and display in the GUI
            for line in iter(process.stdout.readline, ''):
                terminal_output.insert(tk.END, line)
                terminal_output.see(tk.END)  # Scrolls to the end
            process.stdout.close()
            process.wait()
        except subprocess.CalledProcessError as e:
            terminal_output.insert(tk.END, f"Error: {e.output}\n")

    # Run the script in a separate thread to prevent freezing the GUI
    thread = threading.Thread(target=execute_script)
    thread.start()

root = tk.Tk()
root.title("HomeCloud v0.1")

# Set fixed window size
root.geometry("870x400")
root.resizable(False, False)  # Disable window resizing

# Custom title label simulating a larger header
custom_font = ("Bahnschrift", 18)
custom_title = Label(root, text="HomeCloud User Terminal", font=custom_font)
custom_title.grid(row=0, column=0, columnspan=5, padx=20, pady=10)

text_font = ("Bahnschrift", 12)

# Styling for welcome message
welcome_message = """==============================================
                                     HomeCloud - version 0.1 (ALPHA)
==============================================\n"""
terminal_output = tk.Text(root, height=16, width=60, font=text_font, bd=2, relief=tk.SOLID)
terminal_output.grid(row=1, column=3, columnspan=2, padx=20, pady=(0, 20))

# Vertical scrollbar
scrollbar = tk.Scrollbar(root, command=terminal_output.yview)
scrollbar.grid(row=1, column=4, sticky='nse')
terminal_output.config(yscrollcommand=scrollbar.set)

terminal_output.insert(tk.END, welcome_message)
terminal_output.tag_add("blue", "1.0", "4.0")
terminal_output.tag_config("blue", foreground="blue")
terminal_output.tag_add("gray", "4.0", "end")
terminal_output.tag_config("gray", foreground="#333333") 

# Button styling
button_style = {"font": text_font, "padx": 10, "pady": 5, "bd": 3, "relief": tk.RAISED, "bg": "white smoke", "fg": "#333333", "borderwidth": 3, "highlightthickness": 0}
run_button = tk.Button(root, text="Execute application", command=run_bash_script, **button_style)
run_button.grid(row=1, column=1, columnspan=2, padx=20, pady=20)

# Icon styling
icon = PhotoImage(file="images/icon.png")
root.iconphoto(True, icon)

root.mainloop()
