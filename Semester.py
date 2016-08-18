from Exam import *
import re

# A Semester object holds all the tests from a specific semester for
# specific course
class Semester:

	def __init__(self, season, year, instructor):
		# name = row.xpath('td[1]/text()')[0].strip()
		# match = re.search("\d", name)
		# start = match.start()
		# self.season = name[:start-1]
		# self.year = name[start:]
		self.season = season.lower()
		self.year = year
		self.instructor = instructor.lower()

		self.midterm_1 = None
		self.midterm_2 = None
		self.midterm_3 = None
		self.final = None

		# self.instructor = row.xpath('td[2]/text()')
		# self.midterm_1 = Exam(row.xpath('td[3]/a[1]/@href'), # Link for the test PDF
		# 					  row.xpath('td[3]/a[2]/@href')) # Link for the sol'n PDF
		# self.midterm_2 = Exam(row.xpath('td[4]/a[1]/@href'),
		# 					  row.xpath('td[4]/a[2]/@href'))
		# self.final = Exam(row.xpath('td[5]/a[1]/@href'),
		# 				  row.xpath('td[5]/a[2]/@href'))

	# Check if SEM matches the current semester
	def check(self, sem):
		if sem.lower() == '{0} {1}'.format(self.season, self.year).lower():
			return True
		else:
			return False

	def addMidterm_1(self, test, solution):
		self.midterm_1 = Exam(test, solution)

	def getMidterm_1(self):
		return self.midterm_1

	def addMidterm_2(self, test, solution):
		self.midterm_2 = Exam(test, solution)

	def getMidterm_2(self):
		return self.midterm_2

	def addMidterm_3(self, test, solution):
		self.midterm_3 = Exam(test, solution)

	def getMidterm_3(self):
		return self.midterm_3

	def addFinal(self, test, solution):
		self.final = Exam(test, solution)

	def getFinal(self):
		return self.final

	# Returns the desired test
	def getTest(self, test):
		test = test.lower()
		if test == 'midterm 1':
			return self.getMidterm_1()
		elif test == 'midterm 2':
			return self.getMidterm_2()
		elif test == 'final':
			return self.getFinal()
		return None

	def __eq__(self, other):
		if self.year == other.year and self.season == other.season:
			return True
		else:
			return False

	def __lt__(self, other):
		if self.year < other.year:
			return True
		elif self.year == other.year:
			if self.season == 'spring' and other.season == 'fall':
				return True
			else:
				return False
		else:
			return False

	def __repr__(self):
		return '{0} {1}'.format(self.season, self.year)
