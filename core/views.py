from django.conf import settings
from django.shortcuts import render, redirect, reverse


def page_not_found_view(request, exception):
    return render(request, 'errors/404.html')
