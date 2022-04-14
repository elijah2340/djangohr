import random
from django.db import models
from unidecode import unidecode
from django.template.defaultfilters import slugify
from django.utils import timezone
from user.models import Account


class Department(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000, unique=True, null=False)
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
    emergency = models.IntegerField()
    gender = models.CharField(choices=GENDER, max_length=10)
    role = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    language = models.CharField(choices=LANGUAGE, max_length=10, default='english')
    nuban = models.CharField(max_length=10, blank=True)
    bank = models.CharField(max_length=255, blank=True)
    salary = models.CharField(max_length=16, blank=True)

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


class HOD(models.Model):
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    hod = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hod.first_name} | {self.department}'