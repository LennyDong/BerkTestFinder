#!/usr/bin/env python
import sys
from Course import *

# This file is purely used for testing purposes for the time being.
# It could become more developed so this becomes a dedicated terminal
# tool, but for now, the project will be built with the intention of
# being deployed to a web server

courseName = sys.argv[1].lower().strip()

course = Course(courseName)

semester = input('Which semester? Ex. Fall 2015\n')

test = input('Which test? Ex. Midterm 1\n')

print(course.download(semester, test))