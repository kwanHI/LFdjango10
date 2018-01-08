from django.shortcuts import render, redirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login
#from django.contrib.auth.forms import UserCreationForm
from c1app.forms import (
RegistrationForm,
EditUProfileForm,
ClientForm,
SearchClientForm,
ContactForm
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import get_template
from c1app.models import Client10
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView, TemplateView
from django.db.models import Q
import operator
from django.utils import timezone


def display_meta(request):
    values = request.META.items()
    #values.sort()
    html = []
    for k, v in values :
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k,v))
        return HttpResponse('<table>%s</table>' % '\n'.join(html))




def clientafterlogin(request):
    context = RequestContext(request)
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  #return HttpResponseRedirect("c1app/client10Main.html")
                  cform = ClientForm()
                  sform = SearchClientForm()
                  context = {'cform':cform, 'sform':sform}
                  return render(request, 'c1app/client10Main.html',context)
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              print ("invalid login details " + username + " " + password)
              return render_to_response('c1app/login.html', {}, context)
    else:
        # the login is a  GET request, so just show the user the login form.
        return render_to_response('c1app/login.html', {}, context)

    if request.method=='GET' or request.method=='POST':
        if not request.user.is_active:
               cform = ClientForm()
               sform = SearchClientForm()
               context = {'cform':cform, 'sform':sform}
               return render(request, 'c1app/client10Main.html',context)

    #    else:
            #return redirect('/client/login')
    #return redirect('/client/login')



def register(request):
   if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/client/login')
        else:
           pass

   else:
          form = RegistrationForm()

          args = {'form': form}
          return render(request, 'c1app/reg_form.html', args)


@login_required
def view_uprofile(request):
       args = {'user': request.user}
       return render(request, 'c1app/uprofile.html', args)

@login_required
def edit_uprofile(request):
       if request.method == 'POST':
           form = EditUProfileForm(request.POST, instance=request.user)

           if form.is_valid():
              form.save()
              return redirect('/client/uprofile')
       else:
           form = EditUProfileForm(instance=request.user)
           args = {'form': form}
           return render(request, 'c1app/edit_uprofile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/client/uprofile')
        else:
            return redirect('/client/change_password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'c1app/change_password.html', args)

@login_required
def edit_cprofile(request):
      #args = {'client': request.client10}
      return render(request, 'c1app/edit_clientprofile.html', args)
      #pass

def search_client1(request):

    values = request.META
    html = []
    for k in sorted(values):
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, values[k]))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


class HomeClient(TemplateView):
    template_name = 'c1app/searchclient.html'

    def post(self, request, *args, **kwargs):
        searchclientform = SearchClientForm(self.request.GET or None or self.request.POST)
        newclientform = ClientForm(self.request.GET or None)

        context = self.get_context_data(**kwargs)
        context['searchclientform'] = searchclientform
        context['newclientform'] = newclientform

        return self.render_to_response(context)

class SearchClientView(TemplateView):
    form_class = SearchClientForm
    template_name = 'c1app/searchclient.html'
    success_url = 'client/'

    def post(self, request, *args, **kwargs):
        searchclientform = self.form_class(request.POST)
        listclientform = ListClientForm()

        if searchclientform.is_valid():
            searchclientform.save()
            return self.render_to_response(
               self.get_context_data(
               success = True
               )
        )
        else:
            return self.render_to_response(
               self.get_context_data(
                   searchclientform=searchclientform
               )
            )


class MultiRedirectMixin(object):
    """
     A mixin that supports submit-specific success redirection.
     Either specify one success_url, or provide dict with names of
     submit actions given in template as keys
     Example:
     In template:
     <input type="submit" name="create_new" value="Create"/>
     <input type="submit" name="delete" value="Delete"/>
     View:
     MyMultiSubmitView(MultiRedirectMixin, forms.FormView):
     success_urls = {"create_new": reverse_lazy('create'),
    "delete": reverse_lazy('delete')}
    """

    success_urls = {}

    def form_valid(self, form):
        """ Form is valid: Pick the url and redirect.
        """

        for name in self.success_urls:
            if name in form.data:
                self.success_url = self.success_urls[name]
                break

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):

        """
        Returns the supplied success URL.
        """
        if self.success_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                _("No URL to redirect to. Provide a success_url."))

        return url


class ListClientView(ListView):
    model = Client10

    def head(self, *args, **kwargs):
        last_client = self.get_queryset().latest('created')
        response = HttpResponse('')

        response['modified'] = last_client.created_strftime('%a, %d %b %Y %H:%M:%S HST')
        return response

class ClientActionMixin:
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

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(ClientActionMixin, self).form_valid(form)


class ClientCreateView(LoginRequiredMixin, ClientActionMixin, CreateView):
    success_msg = 'created'
    form_class = ClientForm

class ClientDetailView(DetailView):
    model = Client10

class ClientListView(ListView):
    model = Client10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self):
        queryset = super(ClientListView, self).get_queryset()

        fname = self.request.GET.get("fname")
        lname = self.request.GET.get("lname")

        if fname:
            return queryset.filter(fname__icontains=fname)

        return queryset
