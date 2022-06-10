from django.shortcuts import render
from django.http import HttpResponse
from .models import Topic, Course, Student, Order


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of topics: ' + '</p>'
    response.write(heading1)
    for topic in top_list:
        para = '<p>' + str(topic.id) + ': ' + str(topic) + '</p>'
        response.write(para)
        course_list = Course.objects.filter(topic=topic).order_by('-price')[:5]
        for course in course_list:
            course_para = '&nbsp;&nbsp;&nbsp;<span>' + str(course.name) + ': ' + str(course.price)
            if course.for_everyone is True:
                course_para += '&nbsp;&nbsp; This course is for everyone!'
            else:
                course_para += '&nbsp;&nbsp; This course is not for everyone!'
            course_para += '</span><br>'
            response.write(course_para)
    return response
