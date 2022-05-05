from django.shortcuts import render


def index(request):
    return render(request, "welcome.html", {"title": "Welcome Page", "content": "My content"})

