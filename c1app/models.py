from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from datetime import datetime, timedelta


from enum import Enum


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.CharField(max_length=15, default='')


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        #or use TimeStampedModel
#######################################################


class Client10(TimeStampedModel):
    lfcreateuser = models.ForeignKey('auth.User')
    fname = models.CharField(db_index=True, max_length=200)
    lname = models.CharField(db_index=True, max_length=200)
    birthdate = models.DateField(db_index=True, default=datetime.today() + timedelta(days=-5000))
    mname = models.CharField(max_length=200, null=True, blank=True)
    preffname = models.CharField(max_length=200, null=True, blank=True)
    preflname = models.CharField(max_length=200, null=True, blank=True)
    prefmname = models.CharField(max_length=200, null=True, blank=True)

    ssn = models.CharField(max_length=11, null=True, blank=True)
    clientNbr = models.CharField(max_length=10, null=True, blank=True)
    addr1 = models.CharField(max_length=400, null=True, blank=True)
    addr2 = models.CharField(max_length=400, null=True, blank=True)
    city = models.CharField(max_length=400, null=True, blank=True)
    state = models.CharField(max_length=400, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    phone1 = models.CharField(max_length=20, null=True, blank=True)
    phone2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=400, null=True, blank=True)
    emergencyname = models.CharField(max_length=400, null=True, blank=True)
    emergencyrelate = models.CharField(max_length=400, null=True, blank=True)
    emergencyphone = models.CharField(max_length=20, null=True, blank=True)

    genderbirth = models.CharField(max_length=20)
    gendercurrent = models.CharField(max_length=20)

    preferpronoun = models.CharField(max_length=20, null=True, blank=True)
    isuscitizen = models.BooleanField(default=True)
    healthins = models.CharField(max_length=20)

    ise2client = models.BooleanField(default=False)
    ismanagedclient = models.BooleanField(default=False)
    iskuannacompleted = models.BooleanField(default=False)


    class Ethnicity(Enum):
       native = ('nt', 'Native American')
       hawaiian = ('hi', 'Hawaiian, Fijian, Maori, Samoan, Tahitian, Tongan')
       african = ('af', 'African American/Black')
       white = ('wt', 'Caucasian/White')
       seasian = ('sa', 'Southeast Asian including Laotian, Thai, Malaysian, Vietnamese, Chinese, Taiwanese, and Filipino')
       japanese = ('jp', 'Japanese including Okinawan')
       korean = ('kr', 'Korean')
       cuban = ('cb', 'Cuban')
       mexican = ('mx', 'Mexican, Puerto Rican, Chamorrow, Chuukese, Guaanian, Kosraean, Marshallese')
       other = ('ot', 'Other')
       dontknow = ('dk', 'Don''t know, Not sure, Refused')
       notasked = ('na', 'Not Asked')

       @classmethod
       def get_value(cls, member):
           return cls[member].value(0)

    ethnicity = models.CharField(max_length=2,
                                 choices=[x.value for x in Ethnicity] )

    # Metadata
    class Meta:
        ordering = ["fname", "-created"]

    def enroll(self):
          self.save()

    def __str__(self):
        return '%s %s' % (self.fname, self.lname)

    def get_absolute_url(self):
        return reverse('client_detail', kwargs={'pk': self.pk})
