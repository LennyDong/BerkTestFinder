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
		self.tbpPage = html.fromstring(tbpPage.content)

		self.semesters = self.getHKNSemesters()

	# Gets all the semesters available for this course from HKN, and 
	# returns a list of Semester objects
	def getHKNSemesters(self):
		table = self.hknTree.xpath('//table[@id = "exams"]')[0] # Gets the table element from the HKN page
		rows = table.xpath('tr')
		semesters = []
		for row in rows:
			if len(row.xpath('td[2]/text()')) == 0: continue
			semesters.append(Semester(row))
		return semesters

	# 'Downloads' the desired exam from the given semester.
	# Since this will be used on a web app, this methdo will just 
	# return the the correct download link for now. The name will
	# probably have to change to reflect its functionality more
	# accurately
	def download(self, semester, exam):
		right_semester = None
		for sem in self.semesters:
			if sem.check(semester):
				right_semester = sem
		return right_semester.getTest(exam).test_link