from datetime import datetime, time, timedelta
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from ecc_projects.users.models import User
import pytz
# Create your models here.




class Task(models.Model):
    LEVELS = (
        ('VE', 'Very Easy'),
        ('E', 'Easy'),
        ('M', 'Medum'),
        ('H', 'Hard'),
        ('VH', 'Very Hard'),
    )
    STATUS = (
        ('CR', 'Created'),
        ('AS', 'Assigned'),
        ('PG', 'In progress'),
        ('SP', 'Stoped'),
        ('RT', 'Ready to test'),
        ('TS', 'Testing...'),
        ('RV', 'To review'),
        ('RG', 'Revewing...'),
        ('DN', 'Done'),
        ('CN', 'Canceled'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_assigned = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="created_tasks")
    created_at = models.DateField(auto_now = True, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    estimated_durattion = models.DurationField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    estimated_end_time = models.DateTimeField(null=True, blank=True)
    time_left = models.DurationField(blank=True, null= True)
    is_finich_at_time = models.BooleanField(null=True, blank=True)
    difuculty_level = models.CharField(max_length=2, choices=LEVELS)
    status = models.CharField(max_length=2, choices=STATUS, default= "CR")
    stoped_at = models.DateTimeField(null= True, blank=True)
    marked_ready_to_test_at = models.DateTimeField(null= True, blank=True)
    start_test_at = models.DateTimeField(null= True, blank=True)
    marked_to_reveiw_at = models.DateTimeField(null= True, blank=True)
    start_reveiw_at = models.DateTimeField(null= True, blank=True)
    marked_done_at = models.DateTimeField(null= True, blank=True)
    unused_time = models.DurationField(default=timedelta(0))
    lost_in_ready_to_test = models.DurationField(default=timedelta(0))
    lost_in_to_reveiw = models.DurationField(default=timedelta(0))
    lost_in_stop = models.DurationField(default=timedelta(0))

    class Meta:
        ordering = ['-created_at']


    def __str__(self) :
        return self.title
    
    def assign_task(self, owner):
        self.owner = owner
        self.is_assigned = True
        self.status = "AS"
        self.save()
    
    def start_task(self, estimated_duration):
        self.estimated_durattion = estimated_duration
        self.start_time = pytz.utc.localize(datetime.now())
        self.status = "PG"
        self.save()
    
    def stop_task(self):
        self.stoped_at = pytz.utc.localize(datetime.now())
        self.status = "SP"
        self.save()
    
    def resume_task(self):
        if self.status == "SP":
            stoped_duration = pytz.utc.localize(datetime.now()) - self.stoped_at
            self.lost_in_stop =  self.lost_in_stop + stoped_duration
            self.status = "PG"
            self.save()
        
    
    def mark_as_ready_to_test(self):
        self.status = "RT"
        self.marked_ready_to_test_at = pytz.utc.localize(datetime.now())
        self.save()
    
    def start_testing(self):
        if self.status == "RT":
            self.status = "TS"
            self.lost_in_ready_to_test = pytz.utc.localize(datetime.now()) - self.marked_ready_to_test_at
            self.start_test_at = pytz.utc.localize(datetime.now())
            self.save()
    

    def mark_as_to_reveiw(self):
        self.status = "RV"
        self.marked_to_reveiw_at = pytz.utc.localize(datetime.now())
        self.save()
    
    def start_reveiwing(self):
        if self.status == "RV":
            self.status = "RG"
            self.start_reveiw_at = pytz.utc.localize(datetime.now())
            self.lost_in_to_reveiw = pytz.utc.localize(datetime.now()) - self.marked_to_reveiw_at
            self.save()
    
    def mark_as_done(self):
        self.marked_done_at = pytz.utc.localize(datetime.now())
        self.status = "DN"
        self.save()
    
    def update_time_left(self):
        if self.status == "PG":
            consumed_time =pytz.utc.localize(datetime.now())  - self.start_time 
            lost_time = self.lost_in_ready_to_test + self.lost_in_to_reveiw  + self.lost_in_stop  
            self.time_left = self.estimated_durattion - consumed_time - lost_time
            self.save()


class PersonModel(models.Model):
    class Genders(models.TextChoices):
        M = 'Male', _('Male')
        F = 'Female', _('Female')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(verbose_name=_("First name"), max_length=255)
    last_name = models.CharField(verbose_name=_("Last name"), max_length=255)
    gender = models.CharField(verbose_name=_("Gender"), max_length=10, choices=Genders.choices, default=Genders.M)
    phone = models.CharField(verbose_name=_("Phone"), max_length=20, blank=True)
    email = models.EmailField(verbose_name=_("Email"), blank=True)
    address = models.CharField(verbose_name=_("Address"), max_length=255, blank=True)


class EmployeeModel(models.Model):
    class Roles(models.TextChoices):
        E = 'Entreprener', _('Entreprener')
        D = 'Developer', _('Developer')
        V = 'Validator', _('Validator')
    
    person = models.ForeignKey(PersonModel, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices= Roles.choices, verbose_name="Role")

    def __str__(self):
        return self.person.first_name


class ProjectModel(models.Model):
    class Status(models.TextChoices):
        PG = 'In Progress', _('In Progress')
        SP = 'Stoped', _('Stoped')
        CL = 'Closed', _('Closed')
    

    name = models.CharField(max_length=200, verbose_name="Name")
    owner = models.ForeignKey(PersonModel, on_delete=models.DO_NOTHING)
    created_at = models.DateField()
    status = models.CharField(max_length=50, choices= Status.choices, default= Status.PG)
    developers = models.ManyToManyField(PersonModel, verbose_name="Developers", related_name="projectdev")
    validators = models.ManyToManyField(PersonModel, verbose_name="Validators", related_name="projectvalid")
    color = models.CharField(max_length=16, verbose_name="Color")


class EntrepriseModel(models.Model):
    owner = models.ForeignKey(PersonModel, on_delete=models.CASCADE, verbose_name="Owner", null=True)
    name = models.CharField(max_length=200, verbose_name="Name")
    projects = models.ManyToManyField(ProjectModel, verbose_name="Projects")
    employees = models.ManyToManyField(EmployeeModel, verbose_name="Employees")






