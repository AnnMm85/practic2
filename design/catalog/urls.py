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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
