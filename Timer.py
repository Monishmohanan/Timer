"""
A timer application for initiating the countdown time
Created on Jun 2020
"""

__author__ = "Monish Mohanan"
__version__ = "1.0"

try:
	import time
	import tkinter as tk
	from datetime import datetime, timedelta
	from tkinter import Tk, messagebox, ttk, Label
	from tkinter.ttk import Combobox, Button
except Exception as err:
	from tkinter import messagebox
	messagebox.showwarning(
		"Import Error", 
		"Modules not loaded. "+ str(err))

class Widget(object): 
	"""
	Main widget class of the timer

	Attributes:
	----------
		master : tkinter.Tk class
			Base class for the construction of the main window
	
	Method:
	------
		run_timer : Instantiates the Timer class and runs the timer

		rolling_up : Deiconfies the main window
	"""
	
	def __init__(self, master):
		
		"""
		Initializes the main window of the Timer application
		
		Parameters:
		----------
			master : tkinter.Tk class 
				Base class for the construction of the main window
		"""

		# Basic window configuration
		self.master = master
		self.master.title("Timer")
		self.master.geometry('200x135')
		self.master.resizable(0, 0)
		self.master.configure(background = "white")
		self.master.attributes("-topmost", True)

		# Defining input variable wrappers
		self.hours = tk.StringVar()
		self.minutes = tk.StringVar()

		# Dropdown inputs for setting up the time
		Combobox(
			self.master, 
			state = "readonly", 
			textvariable = self.hours, 
			values = [
			str(i)+" hours" for i in range(0, 10)
			]).place(x = 28, y = 25)
		Combobox(
			self.master, 
			state = "readonly", 
			textvariable = self.minutes,
			values = [
			str(i)+" minutes" for i in range(0, 60)
			]).place(x = 28, y = 60)

		Button(
			self.master, 
			text = "START", 
			command = self.run_timer).place(x = 60, y = 95)
		
	def run_timer(self):

		"""Initializes the Timer class based on input validation"""
		
		# Setting up the hours based on selection
		self.hour = (
			"0 hours" if self.hours.get() == "" else self.hours.get())

		# Setting up the minutes based on selection
		self.minute = (
			"0 minutes" if self.minutes.get() == "" else self.minutes.get())

		# Validation criteria
		self.validate = (
			self.hour != "0 hours" or self.minute != "0 minutes")

		# Instantiating Timer based on validation
		if self.validate:
			self.timer_run = tk.Toplevel(self.master)
			self.timer = Timer(self.timer_run, self.hour, self.minute)
			self.master.withdraw()
		else:
			messagebox.showinfo(
				"Incomplete details",
				"Please enter the minutes to start the timer")

	def rolling_up(self):
		
		"""Deiconifies the main window on pressing RESET"""
		
		self.master.deiconify()

class Timer(Widget):
	"""
	The Timer class that runs the countdown

	Attributes:
	----------
		master : tkinter.Tk class
			Base class for the construction of the Timer window

		hours : tkinter.StringVar
			Hours selected by the user in the application

		minutes : tkinter.StringVar
			Minutes selected by the user in the application

	Method:
	------
		restart : Restarts the timer based on preset time

		main_window : Rolls back the main window on pressing RESET
	"""
	
	def __init__(self, master, hours, minutes):
		
		"""Initializes the timer for running the countdown"""
		
		# Basic window configuration
		self.master = master
		self.master.title("TIMER")
		self.master.geometry('210x105')
		self.master.resizable(0, 0)
		self.master.attributes("-topmost", True)
		self.master.attributes("-alpha", 0.6)

		# Assigning required identifiers
		self.hours = hours
		self.minutes = minutes

		# Defining label parameters
		self.label = Label(
			self.master, 
			font = "times 30", 
			fg = "dark red")
		self.label.place(x = 22, y = 12)

		# Calculating final time with respect to current time
		self.seconds = (
			int(self.hours.split(" ")[0]) * 3600 
			+ int(self.minutes.split(" ")[0]) * 60)
		self.target = datetime.now() + timedelta(seconds = self.seconds)

		Button(
			self.master, 
			text = "RESET", 
			command = self.main_window).place(x = 25, y = 68)
		Button(
			self.master, 
			text = "RESTART", 
			command = self.restart).place(x = 110, y = 68)

		# Initilizing the identifiers
		self.hour, self.minute, self.second = 0, 0, 0
		time.sleep(0.0001)

		def update():

			"""A recursive function that updates the Timer window """
			
			diff = self.target - datetime.now()
			total_minute, second = divmod(diff.seconds, 60)
			hour, minute = divmod(total_minute, 60)
			self.hour, self.minute, self.second = hour, minute, second

			# Validation criteria
			validate = (
				bool(self.hour == 0) 
				and bool(self.minute == 0) 
				and bool(self.second == 0))

			# Displaying countdown
			if not validate:
				var = f"{self.hour} : {self.minute:02} : {self.second:02}"
				self.label.config(text = var)
				self.label.after(1000, update)
			else:
				self.label.config(text = "TIME UP")
		update()

	def restart(self):

		"""Restarts the timer based on the preset time"""

		self.target = datetime.now() + timedelta(seconds = self.seconds)
		Timer.__init__(self, self.master, self.hours, self.minutes)
		
	def main_window(self):
		
		"""Rolls back to the main window on pressing RESET"""
		
		self.master.destroy()
		Widget.rolling_up(self.master)

if __name__ == "__main__":      
	window = Tk()
	application = Widget(window)
	window.mainloop()




