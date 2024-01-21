import tkinter as tk
from tkinter import messagebox
from tkinter import *
import requests
# import main

def login():
   username_value = username.get()
   password_value = password.get()
   try:
    response = requests.post("https://main.iothomecloud.com/login-client", json={"email": username_value, "password": password_value})
    if response.status_code == 200: 
        url = response.json()["url"]
        user_name = response.json()["user_name"]
        user_id = response.json()["user_id"]

        import main
        root.withdraw()
        main.run(url, user_name, user_id)
    else:
        messagebox.showinfo("Login Failed", "Incorrect username or password", icon="error")
        username.delete(0, tk.END)
        password.delete(0, tk.END)
   except Exception as e:
        print(e)
        messagebox.showinfo("Login Failed", "Please check you internet connection", icon="error")
        username.delete(0, tk.END)
        password.delete(0, tk.END)
   
   

def toggle_password():
   if password["show"] == "*":
      password["show"] = ""
   else:  
      password["show"] = "*"

root = tk.Tk()
root.title("HomeCloud v0.1 - Login")

# Icon styling
# icon = PhotoImage(file="images/icon.jpg")
# root.iconphoto(True, icon)


# Set fixed window size
root.geometry("465x300")
root.resizable(False, False)  # Disable window resizing

# Custom title label simulating a larger header
custom_font = ("Bahnschrift", 22)
custom_title = Label(root, text="Please enter your credentials", font=custom_font)

text_font = ("Bahnschrift", 16)
login_font = ("Bahnschrift", 20)
icon_font = ("Bahnschrift", 14)

username = tk.Entry(root, width=30, font=text_font, bd=2, relief=tk.SOLID) 
password = tk.Entry(root, show="*", width=30, font=text_font, bd=2, relief=tk.SOLID) 
toggle_style = {"font": icon_font, "bd": 2,  "bg": "white smoke", "fg": "#333333", "borderwidth": 3, "highlightthickness": 0}
toggle_button = tk.Button(root, text="👁", command=toggle_password, **toggle_style)

# Button styling
login_style = {"font": text_font, "bd": 2,  "bg": "white smoke", "fg": "#333333", "borderwidth": 3, "highlightthickness": 0}
login_button = tk.Button(root, text="Login", command=login, **login_style)

custom_title.grid(row=0, column=0, columnspan=2, padx=20, pady=10)
username.grid(row=1, column=0, columnspan=1, padx=20, pady=10)
password.grid(row=2, column=0, columnspan=1, padx=20, pady=10)  
toggle_button.grid(row=2, column=1, columnspan=1)
login_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

root.mainloop()

def run():
   root.mainloop() and root.deiconify()

if __name__ == '__main__':
   run()