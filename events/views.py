from django.http import HttpResponse

def home(request):
    return HttpResponse("Event Lifecycle System Running 🚀")