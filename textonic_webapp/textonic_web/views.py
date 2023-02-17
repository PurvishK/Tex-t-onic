from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
import temp
import image_to_text.main_code as image_code
import os
# Create your views here.
def index(request):
    if request.method == 'POST':
        form=ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            check(img_obj)
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
    else:
        form=ImageForm()
    return render(request, 'index.html', {'form':form})

def check(obj):
    # function to preprocess, detect and extract text from image
    print(obj.img.url)
    print("inside check:",temp.fun(obj))
    image_code.main(obj.img.url)