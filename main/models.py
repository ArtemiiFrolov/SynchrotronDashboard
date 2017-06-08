# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-managed "created" and
    "modified" fields, borrowed from django_extensions.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))

    class Meta:
        ordering = ('-created',)
        abstract = True


# TODO: Add calendar and documents
class Organization(models.Model):
    name = models.CharField(max_length=1000, blank=False, null=False)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    short_description = models.CharField(max_length=100, blank=True, null=False)

    def __str__(self):
        return self.name


class Approach(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name


class Right(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, default="")
    rights = models.ManyToManyField(Right, related_name='roles')

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=150, default="")

    def __str__(self):
        return self.name


class CompleteStatus(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class StageStatus(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class JournalStatus(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class EventsList(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), name=name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, name=name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return User.objects.get(email=username)


class User(AbstractBaseUser):
    email = models.EmailField(_('Email address'), max_length=255, unique=True)

    name = models.CharField(max_length=100, blank=False)
    station = models.ManyToManyField(Station, related_name='users', blank=True)
    organization = models.ManyToManyField(Organization, related_name='users', blank=True)
    role = models.ForeignKey(Role, related_name='users', blank=True, null=True)
    special_rights = models.ManyToManyField(Right, related_name='users')

    is_active = models.BooleanField("Is active", default=True)
    is_admin = models.BooleanField("Is admin", default=False)
    is_staff = models.BooleanField("Is staff", default=False)
    date_joined = models.DateTimeField("Date joined", auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Application(models.Model):
    # TODO: add files and articles
    name = models.CharField(max_length=200, default="")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applications_as_author')
    organizations = models.ManyToManyField(Organization, related_name='requests')
    serial = models.CharField(max_length=15, default="")
    description = models.TextField()
    time_needed = models.IntegerField(default=0)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)
    station = models.ForeignKey(Station, related_name='applications')
    approaches = models.ManyToManyField(Approach, related_name='applications')
    participants = models.ManyToManyField(User, related_name='applications_as_participant')
    equipment = models.ManyToManyField(Equipment, related_name='requests')
    complete_status = models.ForeignKey(CompleteStatus, related_name='requests')
    stage_status = models.ForeignKey(StageStatus, related_name='requests')

    def __str__(self):
        return self.serial


class ExperimentPlan(models.Model):
    author = models.ForeignKey(User, related_name='planning_experiments')
    application = models.ForeignKey(Application, related_name='planning_experiments')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(JournalStatus, related_name='planning_experiments')
    station = models.ForeignKey(Station, related_name='planning_experiments')

    def __str__(self):
        return '%s %s-%s' % (self.station.name,
                             self.start.strftime("%d.%m.%Y %H:%M"),
                             self.end.strftime("%d.%m.%Y %H:%M"))


class Experiment(models.Model):
    request = models.ForeignKey(Application, related_name='experiments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='experiments_as_author')  # TODO: automatically fill from request
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(User, related_name='experiments_as_operator')
    methods = models.ForeignKey(Approach, related_name='experiments')
    comment = models.CharField(max_length=200, default="")
    station = models.ForeignKey(Station, related_name='experiments')

    def __str__(self):
        return '%s %s-%s' % (self.station.name, str(self.start), str(self.end))


class Event(models.Model):
    name = models.ForeignKey(EventsList, related_name='events')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s-%s' % (str(self.start), str(self.end))


class Comment(TimeStampedModel):
    request = models.ForeignKey(Application, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments')
    text = models.CharField(max_length=1000, default="")

    def __str__(self):
        return '%s %s %s' % (self.author.name, self.request.serial, str(self.created))
