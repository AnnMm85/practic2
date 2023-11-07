from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView
from catalog.forms import RegisterUserForm, ChangeApplicationStatusForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

from .models import Application, Category


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


class AdminDashboardView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        all_applications = Application.objects.all()
        categories = Category.objects.all()
        return render(request, 'admin_dashboard.html', {'applications': all_applications, 'categories': categories})


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_new.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_superuser


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_superuser


class ChangeApplicationStatusView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    form_class = ChangeApplicationStatusForm
    template_name = 'change_application_status.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        print(self.request.FILES)
        form = ChangeApplicationStatusForm(self.request.POST, self.request.FILES, instance=self.object)
        form.save()
        return super().form_valid(form)
