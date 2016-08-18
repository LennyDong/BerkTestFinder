# An exam object holds the links to the test and the sol'n PDF
class Exam:
	def __init__(self, test, solution):
		self.test_link = test
		self.solution_link = solution
	def __str__(self):
		pdf = 'pdf: {0}'.format(self.test_link)
		solution = 'sol: {0}'.format(self.solution_link)
		return '{0}\n{1}'.format(pdf, solution)
