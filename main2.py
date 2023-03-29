import tkinter as tk
import tkinter.messagebox
import sqlite3
import os
import subprocess


class LoginScreen(tk.Frame):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.master = master
        self.on_login = on_login

        # create the username and password entry fields
        self.username_label = tk.Label(self, text="Username:")
        self.username_entry = tk.Entry(self)

        self.password_label = tk.Label(self, text="Password:")
        self.password_entry = tk.Entry(self, show="*")

        # create the login button
        # self.login_button = tk.Button(self, text="Login", command=self.login)
        # self.register_button = tk.Button(self, text="Register", command=self.register)

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.register_button = tk.Button(self, text="Register", command=self.show_registration_screen)


        # add the widgets to the screen
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()
        self.register_button.pack()

    def login(self):
        # check if the username and password are correct
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (self.username_entry.get(), self.password_entry.get()))

        if c.fetchone():
            # if correct, call the on_login function passed to this class
            self.on_login()
        else:
            # if incorrect, show an error message
            tk.messagebox.showerror("Error", "Incorrect username or password")

        conn.close()

    def show_registration_screen(self):
        self.pack_forget()
        self.master.registration_screen.pack()




    


class RegistrationScreen(tk.Frame):
    def __init__(self, master, on_register):
        super().__init__(master)
        self.master = master
        self.on_register = on_register

        # create the username and password entry fields
        self.username_label = tk.Label(self, text="Username:")
        self.username_entry = tk.Entry(self)

        self.password_label = tk.Label(self, text="Password:")
        self.password_entry = tk.Entry(self, show="*")

        self.password_label2 = tk.Label(self, text="Password Again")
        self.password_entry2 = tk.Entry(self, show="*")

        # create the register button
        self.register_button = tk.Button(self, text="Register", command=self.register)

        # add the widgets to the screen
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()

        self.password_label2.pack()
        self.password_entry2.pack()
        self.register_button.pack()

    def register(self):
        # check if the database file exists
        if not os.path.exists('users.db'):
            # create the database and the users table
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE users
                        (username text, password text)''')
            conn.commit()
            conn.close()

        # insert the username and password into the users table
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("INSERT INTO users VALUES (?, ?)", (self.username_entry.get(), self.password_entry.get()))

        conn.commit()
        conn.close()

        # call the on_register function passed to this class
        self.on_register()

        # show a success or failure message
        if self.on_register_success is not None:
            if self.validate_inputs():
                self.on_register_success()
                tk.messagebox.showinfo("Registration", "Registration successful!")
            else:
                tk.messagebox.showerror("Registration Error", "Registration failed. Please enter a valid username and password.")
        else:
            tk.messagebox.showerror("Registration Error", "Registration failed.")

    def validate_inputs(self):
        # check that both username and password fields have input
        if not self.username_entry.get() or not self.password_entry.get():
            return False

        # check that both password fields match
        if self.password_entry.get() != self.password_entry2.get():
            return False

        return True
        
class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # create the login and registration screens
        self.login_screen = LoginScreen(self, on_login=self.show_application)
        self.registration_screen = RegistrationScreen(self, on_register=self.show_login_screen)
        
        # show the login screen by default
        self.show_login_screen()
        
    def show_login_screen(self):
        self.registration_screen.pack_forget()
        self.login_screen.pack()
        
    def show_application(self):
        # show the application screen after successful login
       subprocess.run(["python", "main.py"])


root = tk.Tk()
root.geometry("600x500")
app = Application(root)
app.pack()
root.mainloop()
