from django.urls import path
from .views import index,contact_view

urlpatterns = [
    path("",index,name='index'),
    path("contact_view",contact_view,name="contact_view")
]