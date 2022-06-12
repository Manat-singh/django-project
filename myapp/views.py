from django.shortcuts import render
from django.http import HttpResponse
from .models import Topic, Course, Student, Order
from django.shortcuts import  get_object_or_404


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


def about(request):
    response = HttpResponse()
    response.write("This is an E-learning Website! Search our Topics to find all available Courses.")
    return response


def detail(request, top_no):
    topic_detail = Topic.objects.filter(id=top_no).values()
    if not topic_detail:
        data = get_object_or_404(topic_detail)
    else:
        response = HttpResponse()
        para = '<p>Detail for Topic <br>ID: ' + str(topic_detail[0].get('id')) + '<br> Name: <b>' + str(topic_detail[0].get('name')) + '</b><br>Category: <b>' + str(topic_detail[0].get('category')) +'</b></p>'
        course_list = Course.objects.filter(topic=topic_detail[0].get('id'))
        print(course_list)
        heading = '<p>List of course for that topic are as below</p>'
        data = para + heading
        for course in course_list:
            data += '<li>' + str(course) + '</li>'
    response.write(data)
    return response
