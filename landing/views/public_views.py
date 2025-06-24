from django.shortcuts import render

# Create your views here.
def public_home_view(request):
    return render(request, 'landing/public_home.html')