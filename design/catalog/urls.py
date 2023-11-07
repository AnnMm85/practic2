from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.ApplicationListView.as_view(), name='index'),
    path('myapplications/', views.ApplicationByUserListView.as_view(), name='my-appli'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', BBLoginView.as_view(), name='login'),
    path('logout/', BBLogoutView.as_view(), name='logout'),
]

urlpatterns += [
    path('application/create/', views.ApplicationCreate.as_view(), name='application-create'),
    path('application/<int:pk>/delete/', views.ApplicationDelete.as_view(), name='application-delete'),
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('category/new/', CategoryCreateView.as_view(), name='category_new'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('request/<int:pk>/change_status/', ChangeApplicationStatusView.as_view(),
         name='change_application_status'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
