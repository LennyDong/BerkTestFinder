from lxml import html
from Exam import *
import re

# A Semester object holds all the tests from a specific semester for 
# specific course
class Semester:
	# When a semester object is declared, a row element is passed into it.
	# The constructor then parses the information in that row.
	def __init__(self, row):
		name = row.xpath('td[1]/text()')[0].strip()
		match = re.search("\d", name)
		start = match.start()
		self.season = name[:start-1]
		self.year = name[start:]

		self.instructor = row.xpath('td[2]/text()')
		self.midterm_1 = Exam(row.xpath('td[3]/a[1]/@href'), # Link for the test PDF
							  row.xpath('td[3]/a[2]/@href')) # Link for the sol'n PDF
		self.midterm_2 = Exam(row.xpath('td[4]/a[1]/@href'),
							  row.xpath('td[4]/a[2]/@href'))
		self.final = Exam(row.xpath('td[5]/a[1]/@href'),
						  row.xpath('td[5]/a[2]/@href'))

	# Check if SEM matches the current semester
	def check(self, sem):
		if sem.lower() == '{0} {1}'.format(self.season, self.year).lower():
			return True
		else:
			return False

	# Returns the desired test
	def getTest(self, test):
		test = test.lower()
		if test == 'midterm 1':
			return self.midterm_1
		elif test == 'midterm 2':
			return self.midterm_2
		elif test == 'final':
			return self.final
		return None