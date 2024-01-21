import tkinter as tk
from tkinter import *
import subprocess
import threading

root = tk.Tk()
url = ""
user_id = ""

def run_bash_script():
    def execute_script():
        try:
            global url, user_id
            process = subprocess.Popen(
                ["./scripts/init.sh", url, user_id],
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
    thread = threading.Thread(target=execute_script())
    thread.start()

def logout():
    # Revert to login screen
    root.destroy()

# Set GUI title
root.title("HomeCloud v0.1 - Dashboard")

# Set fixed window size
root.geometry("820x360")
root.resizable(False, False)  # Disable window resizing

# Icon styling
# icon = PhotoImage(file="images/icon.png")
# root.iconphoto(True, icon)

# Custom title label simulating a larger header
custom_font = ("Bahnschrift", 18)
custom_title = Label(root, text="HomeCloud User Terminal", font=custom_font)
custom_title.grid(row=0, column=3, columnspan=3, padx=20, pady=10)

text_font = ("Bahnschrift", 12)

# Styling for welcome message
welcome_message = """==============================================
                                    HomeCloud - version 0.1 (ALPHA)
==============================================\n"""
terminal_output = tk.Text(root, height=14, width=60, font=text_font, bd=2, relief=tk.SOLID)
terminal_output.grid(row=1, column=3, columnspan=2, rowspan=2, sticky='nse',  padx=20, pady=(0, 20))
terminal_output.insert(tk.END, welcome_message)
terminal_output.tag_add("blue", "1.0", "4.0")
terminal_output.tag_config("blue", foreground="blue")
terminal_output.tag_add("gray", "4.0", "end")
terminal_output.tag_config("gray", foreground="#333333") 

# Vertical scrollbar
scrollbar = tk.Scrollbar(root,command=terminal_output.yview)
scrollbar.grid(row=1, column=4, rowspan=2, sticky='nse')
terminal_output.config(yscrollcommand=scrollbar.set)

# Create the navbar frame
left_frame = tk.Frame(root, bg="#F2FEFF")

# Pack the frame into the grid and add a border
left_frame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="nsew")
left_frame.config(borderwidth=2, relief="solid", highlightbackground="red") 
tk.Label(left_frame).pack()

# Set a title for the navbar
navbar_title = Label(root, text="HomeCloud", font=custom_font, bg="#F2FEFF", padx=10, pady= 10)
navbar_title.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

# Create and style the navbar buttons
button_style = {"font": text_font, "padx": 10, "pady": 5, "bd": 3, "relief": tk.RAISED, "bg": "#D2FCFF", "activebackground": "#B3F1F5", "fg": "#333333", "borderwidth": 3, "highlightthickness": 0}
run_button = tk.Button(root, text="Emit MQTT data", command=run_bash_script, **button_style)
run_button.grid(row=1, column=0, columnspan=2, padx=20, pady=80)
logout_button = tk.Button(root, text="Log out", command=logout, **button_style)

logout_button.grid(row=2, column=1, columnspan=1, rowspan=2, padx=20, pady=10)

def run(param_url, user_name, param_id):

    global url, user_id
    url = param_url
    user_id = param_id

    # Display the username in the navbar
    user_font = ("Bahnschrift", 13)
    user_title = Label(root, text=user_name, font=user_font, bg="#F2FEFF", padx=10, pady=10)
    user_title.grid(row=2, column=0, columnspan=1, padx=20, pady=10)
    
    root.mainloop()

if __name__ == '__main__':
   print("Please log in first!")

