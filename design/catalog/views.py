from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from catalog.forms import RegisterUserForm

from .models import Application


# Create your views here.


class BBLoginView(LoginView):
    template_name = 'registration/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logout.html'


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')

    # Create your views here.


class ApplicationListView(generic.ListView):
    model = Application
    template_name = 'index.html'
    context_object_name = 'application_list'

    def get_queryset(self):
        return Application.objects.filter(status__exact='done').order_by('-date')[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_AcceptedForWork'] = Application.objects.filter(status__exact='accepted').count()
        return context
