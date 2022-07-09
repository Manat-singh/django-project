from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404
from myapp.forms import OrderForm, InterestForm


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})


def index_old(request):
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
    return render(request, 'myapp/about.html')


def about_old(request):
    response = HttpResponse()
    response.write("This is an E-learning Website! Search our Topics to find all available Courses.")
    return response


def detail(request, top_no):
    response = HttpResponse()
    topic = Topic.objects.filter(id=top_no).first()
    return render(request, 'myapp/detail.html', {'topic': topic})


def detail_old(request, top_no):
    topic = Topic.objects.filter(id=top_no).values()
    if not topic:
        data = get_object_or_404(topic)
    else:
        response = HttpResponse()
        para = '<p>Detail for Topic <br>ID: ' + str(topic[0].get('id')) + '<br> Name: <b>' + str(topic[0].get('name')) + '</b><br>Category: <b>' + str(topic[0].get('category')) +'</b></p>'
        course_list = Course.objects.filter(topic=topic[0].get('id'))
        print(course_list)
        heading = '<p>List of course for that topic are as below</p>'
        data = para + heading
        for course in course_list:
            data += '<li>' + str(course) + '</li>'
    response.write(data)
    return response


def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form':form, 'msg':msg, 'courlist':courlist})


def coursedetail(request, cour_id):
    course = Course.objects.get(id=cour_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.cleaned_data['interested']
            print(interest)
            if int(interest) == 1:
                course.interested += 1
                course.save()
            return redirect('myapp:index')
    else:
        form = InterestForm()
    return render(request, 'myapp/coursedetail.html', {'form':form, 'course': course})
