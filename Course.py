from bs4 import BeautifulSoup
from Semester import *
import lxml
import re
from urllib import request

HKN = 'https://hkn.eecs.berkeley.edu/exams/course/'
TBP = 'https://tbp.berkeley.edu/courses/'

# Course is a object that is intended to hold the access to
# past tests/miderms archive from both HKN and TBP.
# As of 5:40AM PST 5/15/2016, this has not added access to TBP,
# once the functionality has been completed with access to HKN
# test archive, TBP will be added as well
class Course:

	# A course object takes in a courseName, that indicates which course
	# the user intends to find past tests for
	def __init__(self, courseName):
		match = re.search("\d", courseName)
		start = match.start() # First index of a number
		self.department = courseName[:start]
		self.courseName = courseName[start:]

		hknPage = request.urlopen(HKN + '{0}/{1}'.format(self.department, self.courseName)).read()
		tbpPage = request.urlopen(TBP + '{0}/{1}'.format(self.department, self.courseName)).read()

		self.hknSoup = BeautifulSoup(hknPage, "lxml")
		self.tbpSoup = BeautifulSoup(tbpPage, "lxml")

		self.semesters = self.getHKNSemesters()

	# Gets all the semesters available for this course from HKN, and
	# returns a dictionary of Semester objects
	def getHKNSemesters(self):
		table = self.hknSoup.find("table", id="exams") # Gets the table element from the HKN page
		rows = table.find_all("tr")
		semesters = {} # Use dictionary so it is easy to look up a specific semester
		i = 0;
		for row in rows:
			if (i == 0):
				i = i + 1
				continue
			cells = row.find_all("td")
			name = cells[0].string.strip()
			match = re.search("\d", name)
			start = match.start()
			season = name[:start-1]
			year = name[start:]
			instructor = cells[1].find("a").string.strip()
			sem = Semester(season, year, instructor)
			Course.addHKNTests(sem, row)
			semesters['{0} {1}'.format(season, year)] = sem

			i = i + 1
		return semesters

	# Returns a specific semester object matched by SEM
	def getSemester(self, sem):
		return semesters[sem.lower()]

	# Adds all of tests available from HKN for this course, during the specified SEM
	def addHKNTests(sem, row):
		cells = row.find_all("td")
		pdf, solution = Course.getHKNPair(cells[2]) # Gets the midterm 1 cell
		sem.addMidterm_1(pdf, solution)

		pdf, solution = Course.getHKNPair(cells[3]) # Gets the midterm 2 cell
		sem.addMidterm_2(pdf, solution)

		pdf, solution = Course.getHKNPair(cells[4]) # Gets the midterm 2 cell
		sem.addMidterm_3(pdf, solution)

		pdf, solution = Course.getHKNPair(cells[5]) # Gets the final cell
		sem.addFinal(pdf, solution)

	# Gets the pdf & solution pair from the specified CELL. Assumes that the right cell is passed in
	# Returns both the link for the pdf and the solution
	def getHKNPair(cell):
		pdf = cell.find_all("a", string="[pdf]") # Gets the element that has '[pdf]' as text
		if len(pdf) == 1:
			pdf = '{0}{1}'.format(HKN, pdf[0].get("href"))
		else:
			pdf = ''

		solution = cell.find_all("a", string="[solution]") # Gets the element that has '[solution]' as text
		if len(solution) == 1:
			solution = '{0}{1}'.format(HKN, solution[0].get("href"))
		else:
			solution = ''

		return pdf, solution


	# 'Downloads' the desired exam from the given semester.
	# Since this will be used on a web app, this method will just
	# return the the correct download link for now. The name will
	# probably have to change to reflect its functionality more
	# accurately
	def download(self, semester, exam):
		right_semester = None
		for sem in self.semesters:
			if sem.check(semester):
				right_semester = sem
		return right_semester.getTest(exam).test_link
