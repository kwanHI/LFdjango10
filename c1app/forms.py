from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from c1app.models import Client10
from django.forms import ModelForm



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
           'username',
           'first_name',
           'last_name',
           'email',
           'password1',
           'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditUProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = {
           'email',
           'first_name',
           'last_name',
           'password'
        }
        #exclude = {}


ETHINICITY_CHOICES = (
   ('nt', 'Native American'),
   ('hi', 'Hawaiian, Fijian, Maori, Samoan, Tahitian, Tongan'),
   ('af', 'African American/Black'),
   ('wt', 'Caucasian/White'),
   ('sa', 'Southeast Asian incld Laotian, Thai, Malaysian, Vietnamese, Chinese, Taiwanese, and Filipino'),
   ('jp', 'Japanese including Okinawan'),
   ('kr', 'Korean'),
   ('cb', 'Cuban'),
   ('mx', 'Mexican, Puerto Rican, Chamorrow, Chuukese, Guaanian, Kosraean, Marshallese'),
   ('ot', 'Other'),
   ('dk', 'Don''t know, Not sure, Refused'),
   ('na', 'Not Asked'),
)



class ContactForm(forms.Form):
    recipientname = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    source = forms.CharField(       # A hidden input for internal use
        max_length=50,              # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        recipientname = cleaned_data.get('recipientname')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not recipientname and not email and not message:
            raise forms.ValidationError('You have to write something!')


class ClientForm (forms.ModelForm):

    class Meta:
       model = Client10
       fields = [
        'lfcreateuser',
        'fname',
        'lname',
        'birthdate',
        'mname',
        'preffname',
        'preflname',
        'prefmname',
        'ssn',
        'clientNbr',
        'addr1',
        'addr2',
        'city',
        'state',
        'zipcode',
        'phone1',
        'phone2',
        'email',
        'emergencyname',
        'emergencyrelate',
        'emergencyphone',
        'genderbirth',
        'gendercurrent',
        'preferpronoun',
        'isuscitizen',
        'healthins',
        'ise2client',
        'ismanagedclient',
        'iskuannacompleted',
       ]

       STATECHOICES = (
       ('HI', 'Hawaii',), ('CA', 'California',))


       widgets = {
      'fname': forms.TextInput(attrs={'required':True, 'size': 20, 'title': 'first name',}),
      'lname': forms.TextInput(attrs={'required':True}),
      'birthdate': forms.TextInput(attrs={'class':'datePicker'}),
      'mname': forms.TextInput(attrs={'required': False}),
      'preffname': forms.TextInput(attrs={'required': False}),
      'preflname': forms.TextInput(attrs={'required': False}),
      'prefmname': forms.TextInput(attrs={'required': False}),
      'ssn': forms.TextInput(attrs={'required': False}),
      'clientNbr': forms.TextInput(attrs={'required': False}),
      'addr1': forms.TextInput(attrs={'required': False}),
      'addr2': forms.TextInput(attrs={'required': False}),
      'city': forms.TextInput(attrs={'required': False}),
      'state': forms.RadioSelect(choices=STATECHOICES),
      'zipcode': forms.TextInput(attrs={'required': False}),
      'phone1': forms.TextInput(attrs={'required': False}),
      'phone2': forms.TextInput(attrs={'required': False}),
      'email': forms.EmailInput(attrs={'required': False}),
      'emergencyname': forms.TextInput(attrs={'required': False}),
      'emergencyrelate': forms.TextInput(attrs={'required': False}),
      'emergencyphone': forms.TextInput(attrs={'required': False}),
      'genderbirth': forms.TextInput(attrs={'required': False}),
      'gendercurrent': forms.TextInput(attrs={'required': False}),
      'preferpronoun': forms.TextInput(attrs={'required': False}),
      'isuscitizen': forms.CheckboxInput(attrs={'required': True}),
      'healthins': forms.TextInput(attrs={'required': False}),
      'ise2client': forms.CheckboxInput(attrs={'required': True}),
      'ismanagedclient': forms.CheckboxInput(attrs={'required': True}),
      'iskuannacompleted': forms.CheckboxInput(attrs={'required': True}),
      'ethinicity': forms.RadioSelect(choices=ETHINICITY_CHOICES),

      }

    def __init__(self, *args, **kwargs):
          super(ClientForm, self).__init__(*args, **kwargs)




class SearchClientForm(forms.Form):
    first = forms.CharField(widget=forms.TextInput)
    last = forms.CharField(widget=forms.TextInput)
