from __future__ import unicode_literals
from tabnanny import verbose

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.


from django.contrib.auth.base_user import BaseUserManager
#User Manager
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('The given email must be set')
        phone = self.normalize_email(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)

#User Model
class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=13, unique=True)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField( max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + "_" + self.last_name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

# Project Dependent Models 
class ProjectType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class LeadSource(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class ProjectStatus(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Project Status'

class Address(models.Model):
    name = models.CharField(max_length=30)
    addr1 = models.CharField(max_length=30, blank=True)
    addr2 = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    pincode = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Project(models.Model):
    proj_id= models.CharField(max_length=10)
    proj_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    proj_title= models.CharField(max_length=50)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    lead_source = models.ForeignKey(LeadSource, on_delete=models.CASCADE)
    project_status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE)
    shipping_address= models.ForeignKey(Address, on_delete=models.CASCADE)
    def __str__(self):
        return self.proj_title

class Session(models.Model):
    sess_id = models.CharField(max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=30)
    location = models.ForeignKey(Address, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return self.session_name

class ServiceGroup(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Service(models.Model):
    service_group = models.ForeignKey(ServiceGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    cost = models.FloatField()
    is_deliverable = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class SessionsServicesMap(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    qty = models.IntegerField()
    unit_cost = models.FloatField()
    total_cost = models.FloatField()
    def __str__(self):
        return self.service.name


class Product(models.Model):
    name = models.CharField(max_length=30)
    unit_cost = models.FloatField()
    def __str__(self):
        return self.name

class Deliverable(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty= models.IntegerField()
    unit_cost = models.FloatField()
    total_cost = models.FloatField()

class Transaction(models.Model):
    RECEIVED = 'CR'
    SPENT = 'DR'
    TYPE_CHOICES = [
        (RECEIVED, 'RECEIVED'),
        (SPENT, 'SPENT'),
    ]
    type = models.CharField(        
        max_length=10,
        choices=TYPE_CHOICES,
        default=SPENT,
        )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    UPI = 'upi'
    CARD = 'card'
    CASH = 'cash'
    NETBANKING = 'netbanking'
    PAYMENT_CHOICES = [
        (UPI, 'UPI'),
        (CARD, 'CARD'),
        (CASH, 'CASH'),
        (NETBANKING, 'NETBANKING'),
    ]
    payment_mode = models.CharField(        
        max_length=10,
        choices=PAYMENT_CHOICES,
        default=UPI,
        )
    refrece_number = models.CharField(max_length=50)
    comment = models.TextField(blank=True)
