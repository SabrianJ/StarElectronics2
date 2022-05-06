from django.urls import path

from . import views
from .views import CreatePartView

urlpatterns = [
    path('', views.index, name='home'),
    path('part/create', CreatePartView.as_view(), name="create_part")
]