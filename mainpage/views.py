from django.shortcuts import render
from django.http import HttpResponse
from .Course import Course
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def index(request):
    return render(request, 'mainpage/home.html', {'classes': Course.getAllCsClasses()})

@csrf_exempt
def search(request):
    if (request.method == 'GET'):
        course = Course(request.GET['course'])
        semesters = [course.getSemester(semester) for semester in request.GET.getlist('semesters')]
        tests = []
        for semester in semesters:
            for test in request.GET.getlist('tests'):
                tests.append({
                    'semester': "{0} {1}".format(semester.season, semester.year),
                    'instructor': semester.instructor,
                    'test': test,
                    'exam': semester.getTest(test).test_link,
                    'solution': semester.getTest(test).solution_link,
                    'empty': (semester.getTest(test).test_link == "") and (semester.getTest(test).solution_link == "")
                })
        response = {
            'list':[test for test in tests if not test['empty']]
        }
        return HttpResponse(json.dumps(response))
@csrf_exempt
def getSemesters(request):
    if request.method == 'GET':
        course = Course(request.GET['course'])
        semestersSortedByObjects = sorted([{"semester": sem, "semesterObject": course.getSemesters()[sem]} for sem in course.getSemesters().keys()], key=lambda k:k["semesterObject"], reverse=True)
        response = {
                'semesters': [{'semester': item["semester"]} for item in semestersSortedByObjects]
        }
        return HttpResponse(json.dumps(response))
