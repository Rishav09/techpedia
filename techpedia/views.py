from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	context_dict={}
	return render(request,'techpedia/index.html',context=context_dict)

def about(request):
	return 

