import datetime
import random
from django.db import models
from unidecode import unidecode
from django.template.defaultfilters import slugify
from django.utils import timezone
from user.models import Account


class Department(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000, unique=True, null=False)
    director = models.OneToOneField(Account, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(unidecode(value))
        super(Department, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Employee(models.Model):
    LANGUAGE = (('english','ENGLISH'),('yoruba','YORUBA'),('hausa','HAUSA'),('igbo','IGBO'))
    GENDER = (('male','MALE'), ('female', 'FEMALE'),('other', 'OTHER'))
    emp_id = models.CharField(max_length=70, default='emp'+str(random.randrange(100,999,1)))
    staff = models.OneToOneField(Account, on_delete=models.CASCADE)
    address = models.TextField(max_length=1000, default='')
    local_government = models.CharField(max_length=255)
    state_of_origin = models.CharField(max_length=255)
    date_of_first_appointment = models.DateField()
    date_of_present_appointment = models.DateField()
    date_of_birth = models.DateField()
    grade_level = models.IntegerField()
    emergency = models.IntegerField()
    gender = models.CharField(choices=GENDER, max_length=10)
    role = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    language = models.CharField(choices=LANGUAGE, max_length=10, default='english')
    nuban = models.CharField(max_length=10, blank=True)
    bank = models.CharField(max_length=255, blank=True)
    salary = models.CharField(max_length=16, blank=True)
    retirement_date_by_age = models.DateField()
    retirement_date_by_years_of_service = models.DateField()

    def __str__(self):
        return self.staff.first_name

    def full_name(self):
        return f'{self.staff.first_name} {self.staff.last_name}'


class Attendance(models.Model):
    STATUS = (('PRESENT', 'PRESENT'), ('ABSENT', 'ABSENT'), ('UNAVAILABLE', 'UNAVAILABLE'))
    date = models.DateField(auto_now_add=True)
    first_in = models.TimeField()
    last_out = models.TimeField(null=True)
    status = models.CharField(choices=STATUS, max_length=15)
    staff = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        self.first_in = timezone.localtime()
        super(Attendance, self).save(*args, **kwargs)

    def __str__(self):
        return 'Attendance on ' + str(self.date) + ' for' + str(self.staff)


class Leave(models.Model):
    STATUS = (('APPROVED', 'APPROVED'), ('PENDING', 'PENDING'), ('DECLINED', 'DECLINED'))
    purpose = (('ANNUAL', 'ANNUAL'), ('MEDICAL', 'MEDICAL'), ('OTHERS', 'OTHERS'))
    applicant = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    start_time = models.DateField()
    end_time = models.DateField()
    status = models.CharField(max_length=255, choices=STATUS, default='PENDING')
    leave_purpose = models.CharField(max_length=255, choices=purpose, default='ANNUAL')
    completed = models.BooleanField(default=False)


class NextOfKin(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    name1 = models.CharField(max_length=255)
    relationship1 = models.CharField(max_length=255)
    phone_number1 = models.IntegerField()
    name2 = models.CharField(max_length=255)
    relationship2 = models.CharField(max_length=255)
    phone_number2 = models.IntegerField()

    def __str__(self):
        return f'{self.employee.staff.first_name} {self.employee.staff.last_name}'


# class HOD(models.Model):
#     department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, unique=True)
#     hod = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.hod.first_name} | {self.department}'