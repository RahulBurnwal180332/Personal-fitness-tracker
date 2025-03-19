print("Script started!")
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Fitness Tracker")

        self.username = None
        self.fitness_data = {}  # {username: [{date: "YYYY-MM-DD", activity: "...", duration: ..., calories: ...}, ...]}
        self.data_file = "fitness_data.json"
        self.load_data()

        self.create_login_signup_page()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    self.fitness_data = json.load(f)
            except json.JSONDecodeError:
                self.fitness_data = {}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.fitness_data, f, indent=4)

    def create_login_signup_page(self):
        self.clear_frame()

        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(padx=20, pady=20)

        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="w")
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="w")
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.login_frame, text="Signup", command=self.signup).grid(row=3, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.fitness_data and self.fitness_data[username].get("password") == password:
            self.username = username
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.fitness_data:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.fitness_data[username] = {"password": password, "activities": []}
            self.save_data()
            messagebox.showinfo("Success", "Signup successful. Please login.")

    def show_dashboard(self):
        self.clear_frame()

        self.dashboard_frame = ttk.Frame(self.root)
        self.dashboard_frame.pack(padx=20, pady=20)

        ttk.Label(self.dashboard_frame, text=f"Welcome, {self.username}!").pack()
        ttk.Button(self.dashboard_frame, text="Add Activity", command=self.add_activity).pack(pady=10)
        ttk.Button(self.dashboard_frame, text="Logout", command=self.logout).pack()

        self.activity_tree = ttk.Treeview(self.dashboard_frame, columns=("Date", "Activity", "Duration", "Calories"), show="headings")
        self.activity_tree.heading("Date", text="Date")
        self.activity_tree.heading("Activity", text="Activity")
        self.activity_tree.heading("Duration", text="Duration")
        self.activity_tree.heading("Calories", text="Calories")
        self.activity_tree.pack(fill="both", expand=True)

        self.update_activity_list()

    def add_activity(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Activity")

        ttk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        date_entry = ttk.Entry(add_window)
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        date_entry.insert(0,datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(add_window, text="Activity:").grid(row=1, column=0, sticky="w")
        activity_entry = ttk.Entry(add_window)
        activity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Duration (minutes):").grid(row=2, column=0, sticky="w")
        duration_entry = ttk.Entry(add_window)
        duration_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Calories Burned:").grid(row=3, column=0, sticky="w")
        calories_entry = ttk.Entry(add_window)
        calories_entry.grid(row=3, column=1, padx=5, pady=5)

        def save_activity():
            date = date_entry.get()
            activity = activity_entry.get()
            duration = duration_entry.get()
            calories = calories_entry.get()
            if not all([date, activity, duration, calories]):
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                duration = int(duration)
                calories = int(calories)
            except ValueError:
                messagebox.showerror("Error", "Duration and calories must be numbers.")
                return

            self.fitness_data[self.username]["activities"].append({
                "date": date,
                "activity": activity,
                "duration": duration,
                "calories": calories,
            })
            self.save_data()
            self.update_activity_list()
            add_window.destroy()

        ttk.Button(add_window, text="Save", command=save_activity).grid(row=4, column=0, columnspan=2, pady=10)

    def update_activity_list(self):
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)

        for activity in self.fitness_data[self.username]["activities"]:
            self.activity_tree.insert("", "end", values=(activity["date"], activity["activity"], activity["duration"], activity["calories"]))

    def logout(self):
        self.username = None
        self.create_login_signup_page()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()