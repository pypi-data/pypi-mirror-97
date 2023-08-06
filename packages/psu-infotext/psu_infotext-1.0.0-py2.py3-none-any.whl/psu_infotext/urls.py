from django.urls import path
from . import views

urlpatterns = [
    # A simple test page
    path('', views.infotext_index, name='index'),
    path('update', views.infotext_update, name='update'),
]
