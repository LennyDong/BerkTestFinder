# An exam object holds the links to the test and the sol'n PDF
class Exam:
	def __init__(self, test, solution):
		self.test_link = test
		self.solution_link = solution