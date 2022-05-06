from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from StarInventory.forms import PartForm
from StarInventory.models import Part


def index(request):
    return render(request, "welcome.html", {"title": "Welcome Page", "content": "My content"})


def list_parts(request):
    parts = Part.objects.all()
    context = {"parts" : parts}
    return render(request, "list_parts.html", context)


class CreatePartView(CreateView):
    model = Part
    form_class = PartForm
    template_name = "create_part.html"

    success_url = reverse_lazy("list_parts")


class UpdatePartView(UpdateView):
    model = Part
    form_class = PartForm
    template_name = "update_part.html"

    success_url = reverse_lazy("list_parts")
