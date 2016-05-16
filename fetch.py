#!/usr/bin/env python
import sys
from Course import *

# This file is purely used for testing purposes for the time being.
# It could become more developed so this becomes a dedicated terminal
# tool, but for now, the project will be built with the intention of
# being deployed to a web server

courseName = sys.argv[1].lower().strip()

course = Course(courseName)

for sem in course.semesters:
	print(sem)
	print(str(sem.getMidterm_1()) + '\n')