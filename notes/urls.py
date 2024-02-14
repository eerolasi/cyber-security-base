from django.urls import path
from .views import home, signup, detail, delete

urlpatterns = [
    path('', home, name='home'),
    path('detail/<int:pk>/', detail, name='detail'),
    path('delete/<int:pk>/<str:title>/', delete, name='delete'),
    path('signup/', signup, name='signup'),
]