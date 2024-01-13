import sqlite3
from tkinter import *
from tkinter import messagebox
import customtkinter as CTk

CTk.set_appearance_mode("System")
CTk.set_default_color_theme("dark-blue")

class TitleFrame(CTk.CTkFrame):
    def __init__(self, master, width: int, height: int):
        super().__init__(master, width, height)

        self.title = CTk.CTkLabel(self, text='Spend Wise', width=width, height=height, font=('Kameron', 40))
        self.title.grid(row=0, column=0, padx=20, pady=10)

class SubTitleFrame(CTk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title = CTk.CTkLabel(self, text='Login', width=320, height=50, font=('Kameron', 25))
        self.title.grid(row=0, column=0, padx=20, pady=0)

class LoginFormFrame(CTk.CTkFrame):
    def __init__(self, master, width=360, height=130):
        super().__init__(master, width, height)

        self.userNameVar = StringVar()
        self.passWordVar = StringVar()
        self.userIdVar = StringVar()

        self.userIDint = [0]
        self.userID = []

        self.showHidePassVar = IntVar()

        # User ID
        self.userId = CTk.CTkLabel(self, text='User ID:', fg_color='transparent', font=('Kameron', 20))
        self.userId.place(x=10, y=10)

        self.uidEnt = CTk.CTkComboBox(self, font=('Kameron', 20), width=150, values=self.userID, variable=self.userIdVar)
        self.uidEnt.place(x=130, y=10)

        # Username
        self.userName = CTk.CTkLabel(self, text='Username:', fg_color='transparent', font=('Kameron', 20))
        self.userName.place(x=10, y=50)

        self.uNameEnt = CTk.CTkEntry(self, placeholder_text='Username', font=('Kameron', 20), width=150, textvariable=self.userNameVar)
        self.uNameEnt.place(x=130, y=50)

        # Password
        self.passWord = CTk.CTkLabel(self, text='Password:', fg_color='transparent', font=('Kameron', 20))
        self.passWord.place(x=10, y=90)

        self.passWordEnt = CTk.CTkEntry(self, placeholder_text='Password', font=('Kameron', 20), width=150, show='*', textvariable=self.passWordVar)
        self.passWordEnt.place(x=130, y=90)

        # Show/Hide Password Button
        self.shButton = CTk.CTkButton(self, text='Show', width=65, font=('Kameron', 20), command=self.showHidePass)
        self.shButton.place(x=290, y=90)

        self.add_placeholder(self.uNameEnt, 'Username')
        self.add_placeholder(self.passWordEnt, 'Password')

        self.getUserIDs()

        # Bind the checkUserID function to KeyRelease event of the ComboBox
        self.uidEnt.bind("<KeyRelease>", lambda event: self.checkUserID())

    def showHidePass(self):
        currentStatus = self.showHidePassVar.get()

        # Show Password
        if currentStatus == 0:
            self.passWordEnt.configure(show='')
            self.showHidePassVar.set(1)
        # Hide Password
        else:
            self.passWordEnt.configure(show='*')
            self.showHidePassVar.set(0)

        new_text = 'Hide' if currentStatus == 0 else 'Show'
        self.shButton.configure(text=new_text)

    def add_placeholder(self, entry, placeholder=None):
        entry.configure(text_color="gray")
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, placeholder=placeholder: self.on_focus_in(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event, entry=entry, placeholder=placeholder: self.on_focus_out(event, entry, placeholder))

    def on_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, END)
            entry.configure(text_color=('black', 'white'))

    def on_focus_out(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(text_color="gray")

    def uidset(self):
        if self.uidEnt.get() == '':
            self.uidEnt.set('0')

    def checkUserID(self):
        entered_user_id = self.userIdVar.get()

        if not entered_user_id:
            messagebox.showerror("Error", "User ID cannot be empty.")
            return

        try:
            entered_user_id = int(entered_user_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid User ID. Please enter a valid number.")
            return

        if entered_user_id not in self.userIDint:
            messagebox.showerror("Error", "Invalid User ID. Please select a valid User ID.")
            self.uidEnt.set('0')

    def getUserIDs(self):
        try:
            conn = sqlite3.connect('spendwise.db')
            cursor = conn.cursor()

            cursor.execute('SELECT user_id FROM registration')

            user_ids = [row[0] for row in cursor.fetchall()]

            self.userIDint.extend(user_ids)
            self.userID = [str(x) for x in self.userIDint]
            self.uidEnt.configure(values=self.userID)

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            if conn:
                conn.close()

class LoginPage(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Spend Wise Login Page")
        self.geometry("400x350+50+50")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title = TitleFrame(self, 320, 50)
        self.title.place(x=20, y=20)

        self.subtitle = SubTitleFrame(master=self)
        self.subtitle.place(x=20, y=100)

        self.LoginFrame = LoginFormFrame(master=self)
        self.LoginFrame.place(x=20, y=160)

        self.shButton = CTk.CTkButton(self, text='Login', width=360, font=('Kameron', 20), command=self.login)
        self.shButton.place(x=20, y=300)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.destroy()
        self.quit()

    def login(self):
        try:
            conn = sqlite3.connect('spendwise.db')
            cursor = conn.cursor()

            user_id = self.LoginFrame.userIdVar.get()
            username = self.LoginFrame.userNameVar.get()
            password = self.LoginFrame.passWordVar.get()

            print(user_id, username, password)

            # Assuming 'registration' table has columns 'username' and 'password'
            query = f"SELECT user_id, first_name, last_name FROM registration WHERE user_id = ? AND username = ? AND password = ?;"
            cursor.execute(query, (user_id, username, password))

            user_data = cursor.fetchone()

            if user_id == "" or username == "" or password == "":
                messagebox.showerror("Fields Empty", "User ID/Username/Password field(s) are empty. Please fill the empty field.")
            elif user_data:
                user_id_result, first_name, last_name = user_data
                messagebox.showinfo("Login Successful", f"Welcome, {first_name} {last_name}!")
            else:
                messagebox.showerror("Login Failed", "Invalid user ID, username, or password.")

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            if conn:
                conn.close()


# if __name__ == '__main__':
#     app = LoginPage()
#     app.mainloop()
