# -*- coding: utf-8 -*-

import django.utils.timezone as tz
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS, FieldError
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

from guardian.shortcuts import get_perms, assign_perm


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


class TagManager(models.Manager):
    def get_or_create(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            obj = self.create(**kwargs)
            obj.save()
            return obj


class TagModel(models.Model):
    name = models.CharField('Название', max_length=1000, blank=False, null=False)

    class Meta:
        abstract = True
        ordering = ['name']

    objects = TagManager()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class Organization(TagModel):
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Approach(TagModel):
    description = models.TextField('Описание', blank=False, null=False)

    class Meta:
        verbose_name = 'Методика'
        verbose_name_plural = 'Методики'


class Equipment(TagModel):
    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


class CompleteStatus(TagModel):
    class Meta:
        verbose_name = 'Статус завершения'
        verbose_name_plural = 'Статусы завершения'


class StageStatus(TagModel):
    COLOR_CHOICES = (
        ('#8AFF8A', 'Зеленый'),
        ('#FF0000', 'Красный'),
        ('#FFFFA0', 'Желтый'),
    )
    color = models.CharField(verbose_name=_(u'Цвет'), choices=COLOR_CHOICES,
                             default='#33СС00', max_length=7)
    class Meta:
        verbose_name = 'Статус принятия в работу'
        verbose_name_plural = 'Статусы принятия в работу'


class JournalStatus(TagModel):
    class Meta:
        verbose_name = 'Статус планируемого эксперимента'
        verbose_name_plural = 'Статусы планируемого эксперимента'


class EventsList(TagModel):
    COLOR_CHOICES = (
        ('#33СС00', 'Зеленый'),
        ('#0000FF', 'Синий'),
        ('#FF0000', 'Красный'),
        ('#33ССFF', 'Голубой'),
        ('#FF00FF', 'Розовый'),
        ('#660033', 'Коричневый'),
        ('#9900FF', 'Фиолетовый'),
        ('#СС0000', 'Темно-красный'),
    )
    color = models.CharField(verbose_name=_(u'Цвет'), choices=COLOR_CHOICES,
                             default='#33СС00', max_length=7)
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
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return User.objects.get(email=username)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), max_length=255, unique=True)

    name = models.CharField('Имя', max_length=100, blank=False)
    station = models.ManyToManyField("Station", related_name='users', blank=True, verbose_name='Станции')
    organization = models.ManyToManyField(Organization, related_name='users', blank=True, verbose_name='Организации')

    is_active = models.BooleanField("Активен", default=True)
    is_staff = models.BooleanField("Статус персонала", default=False)
    date_joined = models.DateTimeField("Дата регистрации", auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Station(TagModel):
    short_description = models.CharField('Префикс', max_length=100, blank=True, null=False)

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'
        permissions = (
            ('view_station_application', 'Может смотреть заявки станции'),
            ('edit_station_application', 'Может редактировать заявки станции'),
            ('return_station_application', 'Может возвращать заявки станции'),
            ('decline_station_application', 'Может отклонять заявки станции'),
            ('approve_station_application', 'Может принимать заявки станции'),
            ('approve_science_station_application', 'Может принимать ученым советом заявки станции'),
            ('comment_station_application', 'Может комментировать заявки станции'),
            ('view_plan_station_experiment', 'Может просматривать запланированный эксперимент на станции'),
            ('plan_station_experiment', 'Может планировать эксперимент на станции'),
            ('conduct_station_experiment', 'Может проводить эксперимент на станции'),
            ('view_station_experiment', 'Может просматривать эксперимент на станции'),
            ('view_station_stats', 'Может просматривать статистику станции'),
        )


class Application(TimeStampedModel):
    # TODO: add files and articles
    name = models.CharField('Название', max_length=200, blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applications_as_author', verbose_name='Автор')
    organizations = models.ManyToManyField(Organization, related_name='applications', verbose_name='Организации')
    serial = models.CharField('Номер', max_length=15, blank=False, null=False, unique=True)
    description = models.TextField('Описание', )
    time_needed = models.IntegerField('Необходимое время', default=0)
    start = models.DateTimeField('Старт', auto_now_add=False)
    end = models.DateTimeField('Окончание', auto_now_add=False)
    station = models.ForeignKey(Station, related_name='applications', verbose_name='Станция')
    approaches = models.ManyToManyField(Approach, related_name='applications', verbose_name='Методика')
    participants = models.ManyToManyField(User, related_name='applications_as_participant', verbose_name='Участники')
    equipment = models.ManyToManyField(Equipment, related_name='applications', verbose_name='Обрудование')
    complete_status = models.ForeignKey(CompleteStatus, related_name='applications', verbose_name='Статус завершения')
    stage_status = models.ForeignKey(StageStatus, related_name='applications', verbose_name='Статус принятия в работу')

    def __str__(self):
        return self.serial

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        permissions = (
            ('view_application', 'Может смотреть заявку'),
            ('view_all_applications', 'Может смотреть все заявки'),
            ('edit_applications', 'Может редактировать заявки'),
            ('approve_applications', 'Может принимать заявки на станцию'),
            ('approve_science_applications', 'Может принимать заявки ученым советом'),
            ('decline_applications', 'Может отклонять заявки'),
            ('return_applications', 'Может возвращать заявки'),
            ('comment_applications', 'Может комментировать заявки')
        )


@receiver(post_save, sender=Application)
def pre_application_save(sender, instance, **kwargs):
    errors = {}
    if not instance.end:
        errors['end'] = 'Не указана дата окончания'
    if errors:
        raise ValidationError(errors)


@receiver(post_save, sender=Application)
def post_application_save(sender, instance, **kwargs):
    # grant author a permission
    assign_perm('view_application', instance.author, instance)

    # grant participant a permission to view
    for user in instance.participants.all():
        assign_perm('view_application', user, instance)


class ExperimentPlan(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='planning_experiments', verbose_name='Автор')
    application = models.ForeignKey(Application, related_name='planning_experiments', verbose_name='Заявка')
    start = models.DateTimeField('Старт', auto_now_add=False)
    end = models.DateTimeField('Окончание', auto_now_add=False)
    status = models.ForeignKey(JournalStatus, related_name='planning_experiments', verbose_name='Статус')
    station = models.ForeignKey(Station, related_name='planning_experiments', verbose_name='Станция')

    def __str__(self):
        return '%s %s-%s' % (self.station.name,
                             self.start.strftime("%d.%m.%Y %H:%M"),
                             self.end.strftime("%d.%m.%Y %H:%M"))

    class Meta:
        verbose_name = 'Планируемый эксперимент'
        verbose_name_plural = 'Планируемые эксперименты'
        permissions = (
            ('view_plan_experiment', 'Может просматривать запланированный эксперимент'),
            ('plan_experiment', 'Может планировать эксперимент'),
        )


class Experiment(TimeStampedModel):
    application = models.ForeignKey(Application, related_name='experiments', verbose_name='Заявка')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='experiments_as_author', verbose_name='Автор')  # TODO: automatically fill from request
    start = models.DateTimeField('Старт',auto_now_add=False)
    end = models.DateTimeField('Окончание', auto_now_add=False)
    operator = models.ForeignKey(User, related_name='experiments_as_operator', verbose_name='Оператор')
    methods = models.ForeignKey(Approach, related_name='experiments', verbose_name='Методика')
    comment = models.TextField('Комментарий', blank=False, null=False)
    station = models.ForeignKey(Station, related_name='experiments', verbose_name='Станция')

    def __str__(self):
        return '%s %s-%s' % (self.station.name, str(self.start), str(self.end))

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Завершенный эксперимент'
        verbose_name_plural = 'Завершенные эксперименты'
        permissions = (
            ('conduct_experiment', 'Может проводить эксперимент'),
            ('view_experiment', 'Может просматривать эксперимент'),
        )


class Event(TimeStampedModel):
    name = models.ForeignKey(EventsList, related_name='events', verbose_name='Название')
    start = models.DateTimeField('Старт', auto_now_add=False)
    end = models.DateTimeField('Окончание', auto_now_add=False)

    def __str__(self):
        return '%s-%s' % (str(self.start), str(self.end))

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        permissions = (
            ('add_event_to_calendar', 'Может добавлять события в календарь'),
        )


class Comment(TimeStampedModel):
    application = models.ForeignKey(Application, related_name='comments', verbose_name='Заявка')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', verbose_name='Автор')
    text = models.TextField('Текст', blank=False, null=False)

    def __str__(self):
        return '%s %s %s' % (self.author.name, self.application.serial, str(self.created))

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class StationMark(models.Model):
    key = models.SlugField(max_length=255, verbose_name=_('key'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    station = models.ForeignKey(Station, verbose_name='станция', related_name='marks')
    format = models.CharField(max_length=255, verbose_name=_('format'), blank=True)
    unit = models.CharField(max_length=255, verbose_name=_('unit'), blank=True)
    description = models.TextField(verbose_name=_('description'), blank=True)
    visible = models.BooleanField(verbose_name=_('visible'), default=True)

    class Meta:
        verbose_name = 'Показатель'
        verbose_name_plural = 'Показатели'
        unique_together = ('key', 'station')

    def __str__(self):
        return '%s (%s)' % (self.name, self.station)

    def __unicode__(self):
        return self.__str__()


class StationMarkValue(models.Model):
    LIMIT_PER_MARK = 60 * 24 * 31  # 1 month of per-minute values

    mark = models.ForeignKey(StationMark, related_name='values')
    value = models.FloatField(verbose_name=_('value'))
    time = models.DateTimeField(default=tz.now, verbose_name=_('created'))

    @staticmethod
    def post_save(sender, instance, **kwargs):
        # delete values that exceeds the limit
        StationMarkValue.objects.filter(mark=instance.mark)[StationMarkValue.LIMIT_PER_MARK:].delete()

    class Meta:
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения'
        ordering = ['time']

    def __str__(self):
        return '%s (%s)' % (self.value, self.mark)

    def __unicode__(self):
        return self.__str__()


@receiver(post_save, sender=StationMarkValue)
def post_value_save(sender, instance, **kwargs):
    # remove values that exceeds the limit
    vals = list(StationMarkValue.objects.filter(mark=instance.mark)[StationMarkValue.LIMIT_PER_MARK:])
    StationMarkValue.objects.filter(pk__in=vals).delete()


class ApplicationCounter(models.Model):
    year = models.IntegerField("Год", default=0)
    number = models.IntegerField("Количество заявок в году", default=0)

    class Meta:
        verbose_name = 'Ежегодный счетчик'
        verbose_name_plural = 'Ежегодный счетчик'
    # TODO: add a new year new counter

    def __str__(self):
        return str(self.number)

    def __unicode__(self):
        return self.__str__()
