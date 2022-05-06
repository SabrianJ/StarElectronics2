from django.shortcuts import render
from django.views.generic import CreateView

from StarInventory.forms import PartCreateForm
from StarInventory.models import Part


def index(request):
    return render(request, "welcome.html", {"title": "Welcome Page", "content": "My content"})


class CreatePartView(CreateView):
    model = Part
    form_class = PartCreateForm
    template_name = "create_part.html"
