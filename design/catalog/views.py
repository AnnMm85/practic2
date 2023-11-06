from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from catalog.forms import RegisterUserForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Application


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


class ApplicationByUserListView(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'catalog/application_user.html'
    context_object_name = 'application_list'

    def get_queryset(self):
        status = self.request.GET.get('status')
        filter = Application.objects.filter(user=self.request.user).order_by('-date')
        if status:
            filter = filter.filter(status=status)
        return filter


class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = Application
    fields = ['title', 'description', 'category', 'photo_file']
    success_url = reverse_lazy('my-appli')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class ApplicationDelete(LoginRequiredMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('my-appli')

