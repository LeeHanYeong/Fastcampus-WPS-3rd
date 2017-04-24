from django.shortcuts import render

__all__ = [
    'index',
]


def index(request):
    return render(request, 'sns/index.html')
