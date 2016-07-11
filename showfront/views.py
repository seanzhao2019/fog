from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def Home(request):
    return render(request,'showfront/home.html')

@csrf_exempt
def Technology(request):
    return render(request,'showfront/technology.html')

@csrf_exempt
def Technology_single(request):
    return render(request,'showfront/blog-single.html')

@csrf_exempt
def About(request):
    return render(request,'showfront/about.html')



