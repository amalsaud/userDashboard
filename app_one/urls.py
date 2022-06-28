from django.urls import path
from . import views
#urlpatterns => static name
urlpatterns = [
# mapping '/' to index function in views file
path('', views.index),
path('register', views.register),
path('signin', views.signin),

]
