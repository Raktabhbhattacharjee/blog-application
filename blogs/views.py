from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def post_by_category(request,category_id):
    return HttpResponse('post_by_category')