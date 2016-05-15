from lxml import html
import requests
import webbrowser
import re

class Download:
	def getCourse(root, course):
		match = re.search("\d", course)
		start = match.start()
		department = course[:start]
		code = course[start:]
		webbrowser.open(root + '{0}/{1}'.format(department, code))