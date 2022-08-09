from django.contrib import admin
from .models import *    #Attendance,StudentExtra,TeacherExtra,Notice



# Register your models here. (by sumit.luv)
class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, StudentExtraAdmin)

class TeacherExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(TeacherExtra, TeacherExtraAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attendance, AttendanceAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)


# Code tự làm
admin.site.register(Nien_khoa)
admin.site.register(Khoi)
admin.site.register(Lop)
admin.site.register(Mon_hoc)
# admin.site.register(Tim_kiem)
