from tkinter import *
from inspect import signature, _empty

def example_function(meow, woof, bark):
	'''	
	The docstring goes into the comment area
	and it retains the formatting of the string
	'''
	return None

class session_data:
	# Placeholder data object to hold important information like the specific environment/access token etc.
	def __init__(self):
		self.info = {}
	def show_info(self):
		info_window('Session Information', self.info, 'text')

def build_argument_list(call_function):
	# Converts the names of a function's arguments to a list of strings (of those names)
	arg_list = [x for x, p in signature(call_function).parameters.items() if p.default == _empty]
	return arg_list

def entry_screen(session_data, func):
	# Builds an individual function screen
	window = Toplevel()
	add_menu(window)
	window.title(func.__name__)
	arg_list = build_argument_list(func)
	entry_list = {}
	r = 1
	for field in arg_list:
		description = Label(window, text=field, relief=RIDGE, width=15)
		description.grid(row=r, column=0, padx=20, pady=5)
		value = Entry(window, relief=SUNKEN, width=30)
		value.grid(row=r, column=1, padx=20, pady=5)
		entry_list[field] = value
		r = r + 1
	Button(window, text="Submit", command=lambda: execute_call(window, data, func, entry_list), width=15, height=3).grid(row=r, column=1, padx=20, pady=30)
	Button(window, text="Cancel", command=window.destroy, width=15, height=3).grid(row=r, column=2, padx=20, pady=30)
	info = Label(window, text=func.__doc__).grid(row=r, column=0, padx=20, pady=30)

def execute_call(window, data, func, entry_list):
	# Runs the function after all the information has been entered.
	call_values = {}
	for value in entry_list:
		call_values[value] = (entry_list[value].get())
	call_response = func(**call_values)

	# if call_response['statuscode'] == 200:
	#	info_window('Successful ' + str(func.__name__) + ' call', 'Call successful!', 'label')
	# else:
	#	info_window('Failed ' + str(func.__name__) + ' call', call_response['error'], 'text')


def api_button(window, data, func, r, col):
	# Creates the actual button.
	Button(window, text=func.__name__, width = 60, command=lambda: entry_screen(data, func), height=2).grid(row=r, column=col, padx=20, pady=5)

def info_window(title, message, etype):
	# Builds a window with a title, a message, and is defined as either 
	window = Toplevel()
	window.title(title)
	if etype == 'label':
		win_content = Label(window, width=40, height=5, text=message)
		win_content.grid(row=0, column=0, padx=20, pady=20)
		exit_button = Button(window, text="Ok", command=window.destroy, width=20, height=2).grid(row=1, column=0, padx=20, pady=10)
	else:
		win_content = Text(window, width=80, height=20)
		win_content.grid(row=0, column=0, padx=20, pady=20)
		win_content.insert(END, message)
		exit_button = Button(window, text="Ok", command=window.destroy, width=20, height=5).grid(row=1, column=0, padx=20, pady=10)

def add_menu(window):
	# Adds a top menu to close out.
	menu = Menu(window)
	window.config(menu=menu)
	filemenu = Menu(menu)
	menu.add_cascade(label="Options", menu=filemenu)
	filemenu.add_command(label="Close Current Window", command=window.destroy)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=close_caller)

def close_caller():
	print('Bye bye!')
	exit()

def landing_window():
	# Generates the primary menu window
	root = Tk()
	add_menu(root)
	root.title('API Caller')
	r = 0
	data = session_data()

	# Call_list defines which functions appear in the GUI
	call_list = [ example_function ]

	# Allows you to include an image to the top of the menu.
	header_logo = PhotoImage(file="banner_image.gif")
	banner = Label(root, image=header_logo)
	banner.grid(row=r, padx=10, pady=10)
	r = r + 1

	# Status box to include important information.
	# status_box = Text(root, width=60, height=3)
	# status_box.grid(row=r, column=0, padx=20, pady=20)
	# status_box.config(state=DISABLED)
	# r = r + 1
	
	for api_call in call_list:
		api_button(root, data, api_call, r, 0)
		r = r + 1
	Button(root, text='Exit', command=close_caller, width=15, height=3).grid(row=r+1, column=0, padx=40, pady=20)
	mainloop()

if __name__ == "__main__":
	print("Starting API caller...")
	landing_window()