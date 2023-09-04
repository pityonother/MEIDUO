from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views import View
class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        print('hellp')

        return HttpResponse("Post request received.")