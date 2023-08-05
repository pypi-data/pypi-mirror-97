"""tabular_log
"""
import os
import threading
from csv import DictWriter
from datetime import datetime as dt
import urllib.request

__author__ = "help@castellanidavide.it"
__version__ = "02.01 2021-3-3"

class tabular_log:
	def __init__ (
					self, 
					file="trace.log", 
					title="",
					fieldnames=['Title', 'PCName', 'ExecutionCode', 'Message', 'ProcessID', 'ThreadID', 'MessageTime', 'MessageTimeForUsers'], 
					message_style={'Title': '{title}', 'PCName': '{PCName}', 'ExecutionCode': '{start_time}', 'Message': '{message}', 'ProcessID': '{ProcessID}', 'ThreadID': '{ThreadID}', 'MessageTime': '{message_time}', 'MessageTimeForUsers': '{message_time_for_users}'},
					format_style={},
					serverlink="https://www.castellanidavide.it/other/log.php",
					verbose=False
				):
		"""Where it all begins
		"""
		# Init variabiles
		self.file = file
		self.title = title
		try:
			self.PCName = os.environ['COMPUTERNAME']
		except:
			self.PCName = "None"
		self.fieldnames = fieldnames
		self.message_style = message_style
		self.format_style = format_style
		self.start = int(dt.now().timestamp())
		self.serverlink = serverlink
		self.verbose = verbose

		# Setup functions
		self.header()
		
	def header(self):
		"""If not exist add header
		"""
		try:
			if open(self.file, 'r+').readline() == "":
				assert(False)
		except:
			open(self.file, 'w+').write(str(self.fieldnames)[1:-1].replace("'", "\"").replace("\", \"", "\",\"") + "\n")

	def print(self, message):
		"""Write one line
		I open every time the file, because with this method if there is a crash I can be sure that all previous line are into it
		"""
		# If verbose print on the screen
		if self.verbose: print(message)

		# Add my values to given format_style
		format_style = {**self.format_style, **{'title': f'{self.title}', 'PCName': f'{self.PCName}', 'start_time': f'{self.start}', 'message': f'{message}', 'ProcessID': f'{os.getpid()}', 'ThreadID': f'{threading.get_ident()}', 'message_time': f'{dt.now().timestamp()}', 'message_time_for_users': f'{dt.now().strftime("%c")}'}}

		# Format the message
		message_style = {}
		for key, value in self.message_style.items():
			message_style[key] = value.format(**format_style)

		# Prints message to file, this can take some time, so it will run into a Thread
		threading.Thread(target=self.add_to_the_file, args=(message_style,)).start()

		# Send to server, this can take some time, so it will run into a Thread
		threading.Thread(target=urllib.request.urlopen, args=(f"{self.serverlink}?Title={format_style['title']}&PCName={format_style['PCName']}&ExecutionCode={format_style['start_time']}&Message={format_style['message']}&ProcessID={format_style['ProcessID']}&ThreadID={format_style['ThreadID']}&MessageTime={format_style['message_time']}&MessageTimeForUsers={format_style['message_time_for_users']}".replace(" ", "%20"),)).start()
		
	def add_to_the_file(self, message_style):
		"""Add a log line into the file
		"""
		DictWriter(open(self.file, 'a+', newline=''), fieldnames=self.fieldnames, restval='').writerow(message_style)

	def prints(self, messages):
		"""Print lots of lines
		"""
		for message in messages:
			self.print(message)
		
if __name__ == "__main__":
	log = tabular_log(title="LocalTest")
	log.print("Test message")
	for i in range(100):
		threading.Thread(target=log.print, args=(f"Test message {i}",)).start()
