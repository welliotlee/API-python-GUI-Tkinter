from tkinter import *
#from mos_util import *
#import mixed_requests
from inspect import signature, _empty

class data_object:
	def __init__(self):
		self.info = {}

	def show(self):
		info_window('Header Info', self.info, 'text')

def build_param_list(call_function):
	param_list = [x for x, p in signature(call_function).parameters.items() if p.default == _empty]
	return param_list

def add_menu(window):
	menu = Menu(window)
	window.config(menu=menu)
	filemenu = Menu(menu)
	menu.add_cascade(label="Options", menu=filemenu)
	filemenu.add_command(label="Close Current Window", command=window.destroy)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=close_caller)

def remove_header_fields(parameter_list):
	e_exists = 0
	h_exists = 0
	for i in parameter_list:
		if i == 'environment':
			e_exists = 1
		if i == 'headers':
			h_exists = 1
	if e_exists:
		parameter_list.remove('environment')
	if h_exists:
		parameter_list.remove('headers')

def entry_screen(data, func):
	window = Toplevel()
	window.title(func.__name__)
	param_list = build_param_list(func)
	remove_header_fields(param_list)
	entry_list = {}
	r = 0
	for field in param_list:
		description = Label(window, text=field, relief=RIDGE, width=15)
		description.grid(row=r, column=0, padx=20, pady=5)
		value = Entry(window, relief=SUNKEN, width=30)
		value.grid(row=r, column=1, padx=20, pady=5)
		entry_list[field] = value
		r = r + 1
	Button(window, text="Cancel", command=window.destroy, width=15, height=3).grid(row=r, column=2, padx=20, pady=30)
	Button(window, text="Submit", command=lambda: execute_call(window, data, func, entry_list), width=15, height=3).grid(row=r, column=1, padx=20, pady=30)
	add_menu(window)

def execute_call(window, data, func, entry_list):
	if data.info['environment'] == None or data.info['headers'] == None:
		info_window('Authentication / Environment Issue', 'Please authenticate!', 'label')
		return
	call_values = []
	call_values.append(data.info['environment'])
	call_values.append(data.info['headers'])
	for val in entry_list:
		call_values.append(entry_list[val].get())
	call_response = func(*call_values)
	if call_response['statuscode'] == 200:
		info_window('Successful ' + str(func.__name__) + ' call', 'Call successful!', 'label')
	else:
		info_window('Failed ' + str(func.__name__) + ' call', call_response['error'], 'text')

def authorize(data):
	login = Toplevel()
	add_menu(login)
	parameter_list = build_param_list(mos_auth.grab_token)
	entry_list = {}
	r = 0
	for field in parameter_list:
		description = Label(login, text=field, relief=RIDGE, width=15)
		description.grid(row=r, column=0, padx=20, pady=5)
		value = Entry(login, relief=SUNKEN, width=30)
		value.grid(row=r, column=1, padx=20, pady=5)
		entry_list[field] = value
		r = r + 1
	Button(login, text="Cancel", command=login.destroy, width=15, height=3).grid(row=r, column=2, padx=20, pady=30)
	Button(login, text="Submit", command=lambda: save_header_data(login, data, entry_list), width=15, height=3).grid(row=r, column=1, padx=20, pady=30)

def save_header_data(window, data, entry_list):
	login_values = []
	token = None
	for val in entry_list:
		login_values.append(entry_list[val].get())
	if login_values[0][-1:] != '/':
		login_values[0] = login_values[0] + '/'
	token = mos_auth.grab_token(*login_values)
	if token != None:
		data.info['environment'] = login_values[0]
		data.info['headers'] = { 'Authorization' : token }
		window.destroy()
	else:
		info_window('Authorization Error', 'Failed to authenticate your login\nCheck your Environment, Name or Password', 'label')

def api_button(window, data, func, r, col):
	Button(window, text=func.__name__, width = 60, command=lambda: entry_screen(data, func), height=2).grid(row=r, column=col, padx=20, pady=5)

def close_caller():
	print('Bye bye!')
	exit()

def info_window(title, message, etype):
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


def landing_window():
	root = Tk()
	root.title('Api Caller')
	
	call_list = []
	
	data = data_object()
	data.info['environment'] = None
	data.info['headers'] = None
	Button(root, text='Authorize Token', command=lambda: authorize(data), width=60, height=2).grid(row=0, column=0, padx=20, pady=20)
	Button(root, text='Show Info', command=data.show, width=60, height=2).grid(row=1, column=0, padx=20, pady=5)
	r = 2
	for api_call in call_list:
		api_button(root, data, api_call, r, 0)
		r = r + 1
	Button(root, text='Exit', command=close_caller, width=15, height=3).grid(row=r, column=0, padx=40, pady=40)
	add_menu(root)
	mainloop()


print("Starting API caller...")
landing_window()