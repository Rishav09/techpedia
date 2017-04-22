from django.shortcuts import render,redirect
from django.http import HttpResponse
from techpedia.models import Category,Page,UserProfile
from techpedia.forms import CategoryForm,PageForm,UserProfileForm
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
def index(request):
	category_list=Category.objects.order_by('name')
	page_list=Page.objects.order_by('-views')[:5]
	context_dict={'categories':category_list,'pages':page_list}
	return render(request,'techpedia/index.html',context=context_dict)

def add_category(request):
	form=CategoryForm()
	if request.method == 'POST':
		form=CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print(form.errors)
	return render(request,'techpedia/add_category.html',{'form':form})

def show_category(request,category_name_slug):
	context_dict={}
	try:
		category=Category.objects.get(slug=category_name_slug)
		pages=Page.objects.filter(category=category).order_by('-views')
		context_dict['pages']=pages
		context_dict['category']=category
	except Category.DoesNotExist:
		context_dict['category']=None
		context_dict['pages']=None
	return render(request,'techpedia/category.html',context_dict)
	
def add_page(request,category_name_slug):
	try:
		category=Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category=None

	form=PageForm()
	if request.method == 'POST':
		form=PageForm(request.POST)
		if form.is_valid():
			if category:
				page=form.save(commit=False)
				page.category=category
				page.views=0
				page.save()
				return show_category(request,category_name_slug)
		else:
			print(form.errors)
	context_dict={'form':form,'category':category}
	return render(request,'techpedia/add_page.html',context_dict)

def about(request):
	context_dict={}
	return render(request,'techpedia/about.html',context=context_dict)

@login_required
def register_profile(request):
	form=UserProfileForm()
	if request.method=='POST':
		form=UserProfileForm(request.POST,request.FILES)
		if form.is_valid():
			user_profile=form.save(commit=False)
			user_profile.user=request.user
			user_profile.save()
			return redirect('index')
		else:
			print(form.errors)
	context_dict={'form':form}
	return render(request,'techpedia/profile_registration.html',context_dict)

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    
    return render(request, 'techpedia/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})

@login_required
def list_profiles(request):
#    user_list = User.objects.all()
    userprofile_list = UserProfile.objects.all()
    return render(request, 'techpedia/list_profiles.html', { 'userprofile_list' : userprofile_list})


def track_url(request):
	page_id=None
	url='/techpedia/'
	if request.method == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']

			try:
				page=Page.objects.get(id=page_id)
				page.views=page.views+1
				page.save()
				url=page.url
			except:
				pass
	return redirect(url)

