from django.core.exceptions import ObjectDoesNotExist
import datetime
import json
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404
from myapp.forms import OrderForm, InterestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    browserClose = request.session.get_expire_at_browser_close()
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = 0
    return render(request, 'myapp/index.html', {'top_list': top_list,'last_login':last_login,'browserCLose':browserClose})


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
    response = HttpResponse()
    count = 1
    about_visits = request.COOKIES.get('about_visits')
    print(about_visits)
    if about_visits:
        count = int(about_visits) + 1
    else:
        count = 1

    response = render(request, 'myapp/about.html', {'count': count})
    response.set_cookie(key='about_visits', value=count, max_age=300)
    return response


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
                cour_id = int(form['course'].value())
                course = Course.objects.get(id=cour_id)
                if course.price > 150:
                    course.discount()
                    course.save()

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


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        request.session.set_test_cookie()
        now = datetime.datetime.now()
        json_str = json.dumps(now, default=str)
        request.session['last_login'] = json_str
        request.session.set_expiry(3600);
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            if user.is_active:
                login(request, user)
                print('authenticated')
                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    #del request.session['last_login']
    return HttpResponseRedirect(reverse(('myapp:login')))


# @login_required
def myaccount(request):
    if request.user.is_authenticated:
        user=request.user
        try:
            curr_student = Student.objects.get(id=user.id)
            if(curr_student):
                course_ordered = Order.objects.filter(student=curr_student)
                topic_interested = curr_student.interested_in.all()
                return render(request, 'myapp/myaccount.html', {'student':curr_student, 'orders':course_ordered, 'topics':topic_interested})
            else:
                return render(request, 'myapp/myaccount.html')
        except ObjectDoesNotExist:
            return render(request, 'myapp/myaccount.html')
    else:
        return HttpResponseRedirect(reverse(('myapp:login')))


def myorders(request):
    if(request.user.is_authenticated):
        user = request.user
        try:
            curr_student = Student.objects.get(id=user.id)
            if (curr_student):
                course_ordered = Order.objects.filter(student=curr_student)
                return render(request, 'myapp/myorders.html', {'student': curr_student, 'orders': course_ordered})
            else:
                return render(request, 'myapp/myorders.html')

        except ObjectDoesNotExist:
            return render(request, 'myapp/myorders.html')
    else:
        return HttpResponseRedirect(reverse(('myapp:login')))

