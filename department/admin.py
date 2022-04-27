from django.contrib import admin
from .models import Department, Employee, Attendance, Leave, NextOfKin, Director, DirectorNextOfKin


class LeaveAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'status')


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'first_in', 'status',)
    list_filter = ('status', 'date')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'department')


class DirectorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(NextOfKin)
admin.site.register(DirectorNextOfKin)
admin.site.register(Director, DirectorAdmin)
