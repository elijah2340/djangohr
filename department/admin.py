from django.contrib import admin
from .models import Department, Employee, Attendance, HOD


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'status',)
    list_filter = ('status', 'date')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(HOD)