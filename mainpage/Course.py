from bs4 import BeautifulSoup
from .Semester import Semester
import lxml
import re
from urllib import request

HKN = 'https://hkn.eecs.berkeley.edu'
TBP = 'https://tbp.berkeley.edu'

HKN_COURSES = HKN + '/exams'
TBP_COURSES = TBP + '/courses/cs'

# Course is a object that is intended to hold the access to
# past tests/miderms archive from both HKN and TBP.
# As of 5:40AM PST 5/15/2016, this has not added access to TBP,
# once the functionality has been completed with access to HKN
# test archive, TBP will be added as well
class Course:
    hknPage = request.urlopen(HKN_COURSES).read()
    tbpPage = request.urlopen(TBP_COURSES).read()

    hknSoup = BeautifulSoup(hknPage, "lxml")
    tbpSoup = BeautifulSoup(tbpPage, "lxml")

    # A course object takes in a courseName, that indicates which course
    # the user intends to find past tests for
    def __init__(self, courseName):
        courseName = courseName.lower()
        courseName = courseName.replace(" ", "")
        print(courseName)
        match = re.search("\d", courseName)
        start = match.start() # First index of a number
        self.department = courseName[:start]
        self.courseName = courseName[start:]

        hknCoursePage = request.urlopen(HKN + '/exams/course/{0}/{1}'.format(self.department, self.courseName)).read()
        tbpCoursePage = request.urlopen(TBP + '/courses/{0}/{1}'.format(self.department, self.courseName)).read()

        self.hknCourseSoup = BeautifulSoup(hknCoursePage, "lxml")
        self.tbpCourseSoup = BeautifulSoup(tbpCoursePage, "lxml")

        self.semesters = self.getHKNSemesters()
        TBPSemesters = self.getTBPSemesters()

        self.combineSemesters(TBPSemesters)

    def getAllCsClasses():
        hknClasses = Course.getHKNCsClasses()
        tbpClasses = Course.getTBPCsClasses()
        for name in tbpClasses:
            if (name not in hknClasses):
                hknClasses.append(name)
        hknClasses.sort()
        print(hknClasses)
        return hknClasses

    def getHKNCsClasses():
        tableDiv = Course.hknSoup.find("div", class_="exam_table")
        tbody = tableDiv.find("table").find("tbody")
        cells = tbody.find_all("td")
        classNames = [cell.string[:cell.string.index('-') - 1].upper() for cell in cells]
        return classNames

    def getTBPCsClasses():
        containerDiv = Course.tbpSoup.find("div", id="content")
        listItems = containerDiv.find_all("li")
        classNames = [listItem.find("a").string.upper() for listItem in listItems]
        return classNames

    def combineSemesters(self, TBPSemesters):
        for key in TBPSemesters:
            if key in self.semesters:
                Course.combineSemester(self.semesters[key], TBPSemesters[key])
            else:
                self.semesters[key] = TBPSemesters[key]

    def combineSemester(semester1, semester2):
        Course.combineTest(semester1.getMidterm_1(), semester2.getMidterm_1())
        Course.combineTest(semester1.getMidterm_2(), semester2.getMidterm_2())
        Course.combineTest(semester1.getMidterm_3(), semester2.getMidterm_3())
        Course.combineTest(semester1.getFinal(), semester2.getFinal())

    def combineTest(test1, test2):
        if (test1.test_link == "" and test2.test_link != ""):
            test1.test_link = test2.test_link
        if (test1.solution_link == "" and test2.solution_link != ""):
            test1.solution_link = test2.solution_link

    def getSemesterPair(semString):
        match = re.search("\d", semString)
        start = match.start()
        season = semString[:start-1]
        year = semString[start:]
        return season, year

    # Gets all the semesters available for this course from HKN, and
    # returns a dictionary of Semester objects
    def getHKNSemesters(self):
        table = self.hknCourseSoup.find("table", id="exams") # Gets the table element from the HKN page
        rows = table.find_all("tr")
        semesters = {} # Use dictionary so it is easy to look up a specific semester
        i = 0;
        for row in rows:
            if (i == 0):
                i = i + 1
                continue
            cells = row.find_all("td")
            semesterString = cells[0].string.strip()
            season, year = Course.getSemesterPair(semesterString)
            instructor = ""
            if (cells[1].find("a") != None) :
                instructor = cells[1].find("a").string.strip()

            sem = Semester(season, year, instructor)
            Course.addHKNTests(sem, cells)
            semesters['{0} {1}'.format(season, year).lower()] = sem
            i = i + 1

        return semesters

    # Gets all the semestes available for this course from TBP, and
    # returns a dictionary of Semester objects
    def getTBPSemesters(self):
        table = self.tbpCourseSoup.find("table").find("tbody")
        rows = table.find_all("tr")
        semesters = {}
        for row in rows:
            cells = row.find_all("td")
            aElement = cells[0].find("a")
            instructor = None
            if (aElement == None):
                instructor = ""
            else:
                instructor = aElement.string.strip()

            semesterString = cells[2].string.strip()
            season, year = Course.getSemesterPair(semesterString)
            sem = None
            if ('{0} {1}'.format(season, year) in semesters):
                sem = semesters.get('{0} {1}'.format(season, year))
            else:
                sem = Semester(season, year, instructor)
            Course.addTBPTest(sem, cells)
            semesters['{0} {1}'.format(season, year).lower()] = sem
        return semesters

    # Returns a specific semester object matched by SEM
    def getSemester(self, sem):
        if (sem.lower() in self.semesters):
            return self.semesters[sem.lower()]

    def getSemesters(self):
        return self.semesters

    # Adds all of tests available from HKN for this course, during the specified SEM
    def addHKNTests(sem, cells):
        pdf, solution = Course.getHKNPair(cells[2]) # Gets the midterm 1 cell
        sem.addMidterm_1(pdf, solution)

        pdf, solution = Course.getHKNPair(cells[3]) # Gets the midterm 2 cell
        sem.addMidterm_2(pdf, solution)

        pdf, solution = Course.getHKNPair(cells[4]) # Gets the midterm 2 cell
        sem.addMidterm_3(pdf, solution)

        pdf, solution = Course.getHKNPair(cells[5]) # Gets the final cell
        sem.addFinal(pdf, solution)

    # Adds the test contained in the current row for this course
    def addTBPTest(sem, cells):
        pdf = cells[3].find("a")
        if pdf != None:
            pdf = '{0}{1}'.format(TBP, pdf.get("href"))
        else:
            pdf = ""

        solution = cells[4].find("a")
        if solution != None:
            solution = '{0}{1}'.format(TBP, solution.get("href"))
        else:
            solution = ""

        test = cells[1].string.strip().lower()

        if (test == "midterm 1"):
            sem.addMidterm_1(pdf, solution)
        elif (test == "midterm 2"):
            sem.addMidterm_2(pdf, solution)
        elif (test == "midterm 3"):
            sem.addMidterm_3(pdf, solution)
        elif (test == "final"):
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
