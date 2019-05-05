from django.shortcuts import render

def index(request):
    context = {'message': 'Hello!'}
    return render(request, 'myapp/index.html', context)
