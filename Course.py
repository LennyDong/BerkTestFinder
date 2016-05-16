from lxml import html
from Semester import *
import requests
import re

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

		hknPage = requests.get(HKN + '{0}/{1}'.format(self.department, self.courseName))
		tbpPage = requests.get(TBP + '{0}/{1}'.format(self.department, self.courseName))

		self.hknTree = html.fromstring(hknPage.content)
		self.tbpTree = html.fromstring(tbpPage.content)

		self.semesters = self.getHKNSemesters()

	# Gets all the semesters available for this course from HKN, and 
	# returns a list of Semester objects
	def getHKNSemesters(self):
		table = self.hknTree.xpath('//table[@id = "exams"]')[0] # Gets the table element from the HKN page
		rows = table.xpath('tr')
		semesters = []
		for row in rows:
			if len(row.xpath('td[2]/text()')) == 0: continue

			name = row.xpath('td[1]/text()')[0].strip()
			match = re.search("\d", name)
			start = match.start()
			season = name[:start-1]
			year = name[start:]
			instructor = row.xpath('td[2]/text()')[0]

			sem = Semester(season, year, instructor)
			Course.addHKNTests(sem, row)
			semesters.append(sem)
		return semesters

	def addHKNTests(sem, row):
		pdf, solution = Course.getHKNPair(row.xpath('td[3]')[0])
		sem.addMidterm_1(pdf, solution)

		pdf, solution = Course.getHKNPair(row.xpath('td[4]')[0])
		sem.addMidterm_2(pdf, solution)

		pdf, solution = Course.getHKNPair(row.xpath('td[5]')[0])
		sem.addFinal(pdf, solution)

	def getHKNPair(cell):
		pdf = cell.xpath('a[text()="[pdf]"]/@href')
		if len(pdf) == 1:
			pdf = pdf[0]
		else:
			pdf = ''
		solution = cell.xpath('a[text()="[solution]"]/@href')
		if len(solution) == 1:
			solution = solution[0]
		else:
			solution = ''
		if pdf != '':
			pdf = '{0}{1}'.format(HKN, pdf)
		if solution != '':
			solution = '{0}{1}'.format(HKN, solution)
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