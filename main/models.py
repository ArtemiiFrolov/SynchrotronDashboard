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
    name = models.CharField('Название', max_length=1000, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Station(models.Model):
    name = models.CharField('Название', max_length=100, blank=False, null=False)
    short_description = models.CharField('Краткое описание', max_length=100, blank=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'


class Approach(models.Model):
    name = models.CharField('Название', max_length=100, blank=False, null=False)
    description = models.TextField('Описание', blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Методика'
        verbose_name_plural = 'Методики'


class Right(models.Model):
    name = models.CharField('Название', max_length=100, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Право'
        verbose_name_plural = 'Права'


class Role(models.Model):
    name = models.CharField('Название', max_length=100, blank=False, null=False)
    rights = models.ManyToManyField(Right, related_name='roles', verbose_name='Права')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class Equipment(models.Model):
    name = models.CharField('Название', max_length=150, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


class CompleteStatus(models.Model):
    name = models.CharField('Название', max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус завершения'
        verbose_name_plural = 'Статусы завершения'


class StageStatus(models.Model):
    name = models.CharField('Название', max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус принятия в работу'
        verbose_name_plural = 'Статусы принятия в работу'


class JournalStatus(models.Model):
    name = models.CharField('Название', max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус планируемого эксперимента'
        verbose_name_plural = 'Статусы планируемого эксперимента'


class EventsList(models.Model):
    name = models.CharField('Название', max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Словарь событий'
        verbose_name_plural = 'Словарь событий'


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

    name = models.CharField('Имя', max_length=100, blank=False)
    station = models.ManyToManyField(Station, related_name='users', blank=True, verbose_name='Станции')
    organization = models.ManyToManyField( Organization, related_name='users', blank=True, verbose_name='Организации')
    role = models.ForeignKey(Role, related_name='users', blank=True, null=True, verbose_name='Роль')
    special_rights = models.ManyToManyField( Right, related_name='users', verbose_name='Особые права')  # TODO: make it possible leave special_right blank

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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Application(models.Model):
    # TODO: add files and articles
    name = models.CharField('Название', max_length=200, blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applications_as_author', verbose_name='Автор')
    organizations = models.ManyToManyField(Organization, related_name='applications', verbose_name='Организации')
    serial = models.CharField('Номер', max_length=15, blank=False, null=False)
    description = models.TextField('Описание', )
    time_needed = models.IntegerField('Необходимое время', default=0)
    start = models.DateTimeField('Старт', auto_now_add=True)
    end = models.DateTimeField('Окончание', auto_now_add=True)
    station = models.ForeignKey(Station, related_name='applications', verbose_name='Станция')
    approaches = models.ManyToManyField(Approach, related_name='applications', verbose_name='Методика')
    participants = models.ManyToManyField(User, related_name='applications_as_participant', verbose_name='Участники')
    equipment = models.ManyToManyField(Equipment, related_name='applications', verbose_name='Обрудование')
    complete_status = models.ForeignKey(CompleteStatus, related_name='applications', verbose_name='Статус завершения')
    stage_status = models.ForeignKey(StageStatus, related_name='applications', verbose_name='Статус принятия в работу')

    def __str__(self):
        return self.serial

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class ExperimentPlan(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='planning_experiments', verbose_name='Автор')
    application = models.ForeignKey(Application, related_name='planning_experiments', verbose_name='Заявка')
    start = models.DateTimeField('Старт', auto_now_add=True)
    end = models.DateTimeField('Окончание', auto_now_add=True)
    status = models.ForeignKey(JournalStatus, related_name='planning_experiments', verbose_name='Статус')
    station = models.ForeignKey(Station, related_name='planning_experiments', verbose_name='Статус')

    def __str__(self):
        return '%s %s-%s' % (self.station.name,
                             self.start.strftime("%d.%m.%Y %H:%M"),
                             self.end.strftime("%d.%m.%Y %H:%M"))

    class Meta:
        verbose_name = 'Планируемый эксперимент'
        verbose_name_plural = 'Планируемые эксперименты'


class Experiment(models.Model):
    application = models.ForeignKey(Application, related_name='experiments', verbose_name='Заявка')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='experiments_as_author', verbose_name='Автор')  # TODO: automatically fill from request
    start = models.DateTimeField('Старт', auto_now_add=True)
    end = models.DateTimeField('Окончание', auto_now_add=True)
    operator = models.ForeignKey(User, related_name='experiments_as_operator', verbose_name='Оператор')
    methods = models.ForeignKey(Approach, related_name='experiments', verbose_name='Методика')
    comment = models.TextField('Комментарий', blank=False, null=False)
    station = models.ForeignKey(Station, related_name='experiments', verbose_name='Станция')

    def __str__(self):
        return '%s %s-%s' % (self.station.name, str(self.start), str(self.end))

    class Meta:
        verbose_name = 'Завершенный эксперимент'
        verbose_name_plural = 'Завершенные эксперименты'


class Event(models.Model):
    name = models.ForeignKey(EventsList, related_name='events', verbose_name='Название')
    start = models.DateTimeField('Старт', auto_now_add=True)
    end = models.DateTimeField('Окончание', auto_now_add=True)

    def __str__(self):
        return '%s-%s' % (str(self.start), str(self.end))

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Comment(TimeStampedModel):
    application = models.ForeignKey(Application, related_name='comments', verbose_name='Заявка')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', verbose_name='Автор')
    text = models.TextField('Текст', blank=False, null=False)

    def __str__(self):
        return '%s %s %s' % (self.author.name, self.application.serial, str(self.created))

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'