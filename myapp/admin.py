import decimal

from django.contrib import admin
from .models import Topic, Course, Student, Order, Image

# Register your models here.
#admin.site.register(Topic)
#admin.site.register(Course)
#admin.site.register(Student)
admin.site.register(Order)
admin.site.register(Image)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','level','registered_courses')

    def level(self, obj):
        levels = Order.objects.filter(student=obj)
        count = 0
        levelList = ''
        for level in levels:
            return level.levels
            levelList += str(level.levels)
            count += 1
            if (count < len(levels)):
                levelList += ", "
        return levelList

    def registered_courses(self, obj):
        courses = Order.objects.filter(student=obj)
        courseList = ""
        count = 0
        for course in courses:
            courseList += course.course.name
            count +=1
            if(count < len(courses)):
                courseList += ", "
        return courseList


admin.site.register(Student, StudentAdmin)


class CourseInline(admin.TabularInline):
    model = Course


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (('name', 'length'))
    inlines = [
        CourseInline
    ]


def reduce_price(modeladmin, request, queryset):
    cs = Course()
    for co in queryset:
        cour = Course.objects.get(id=co.id)
        cour.price = decimal.Decimal(0.9) * cour.price
        cour.save()
    reduce_price.short_description = 'Reduce price'


class CourseAdmin(admin.ModelAdmin):

    actions = [reduce_price]


admin.site.register(Course, CourseAdmin)

