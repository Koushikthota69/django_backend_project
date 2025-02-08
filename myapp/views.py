from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,PostForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Post
from django.utils import timezone
from django.http import HttpResponse

# Create your views here.
def home(request):
    nums=[1,2,3,4,5]
    name='koushik_thota'
    context={"name":name,"nums":nums}
    return render(request,'home.html',context)

def user_register(request):
    forms=UserRegistrationForm()
    context={'forms':forms}
    if request.method == 'GET':
      return render(request,'register.html',context)
    if request.method == 'POST':
        # after form is submitted 
        #request.POST contains the form data 
        forms= UserRegistrationForm(request.POST) #it has valid data of user
        if forms.is_valid():
            forms.save()
            return redirect('login')
        else:
            context['error']="invalid form submission,try again!"
            return render(request,'register.html',context)
def user_login(request):
    if request.method=='GET':
     return render(request,'login.html')
    if request.method =='POST':
       username=request.POST.get('username')
       password=request.POST.get('password')
       user=authenticate(request,username=username,password=password)
       if user is not None:
          login(request,user)
          return redirect('home')
       else:
          error='invalid username or password'
          context={'error':error}
          return render(request,'login.html',context)
@login_required
  
def create_post(request):
   form=PostForm()
   context={'form':form}
   if request.method =='GET':
      return render(request,'create_post.html',context)
   if request.method=='POST':
      form=PostForm(request.POST)
      if form.is_valid:
         post=form.save(commit=False)
         post.author = request.user
         post.save()
         return redirect('home')
      else:
         context['error']='invalid from submission, try again!'
         return render(request,'create_post.html',context)
def view_post(request): # as we use to display the table in the mysql done by select * from tablename it is equal to the below line in django
   post_list=Post.objects.all().order_by('-published_on')
   context={'post_list':post_list}
   return render(request,'view_post.html',context)


def update_post(request,id):
   try:
    single_post=Post.objects.get(pk=id) #fetch single post
   except Post.DoesNotExist:
        return HttpResponse('not exist')
   if request.user != single_post.author:
      return HttpResponse('you are not allwed to modify the content<a href='/'>click here</a>') #as we not allowed the another user to update the post we done in the frontend that is in the template but here we done in the backend that if user is not the author
   form=PostForm(instance=single_post)
   context={'form':form}
   if request.method=='GET':
      return render(request,'update_post.html',context)
   if request.method =='POST':
      form = PostForm(request.POST,instance=single_post)
      if form.is_valid():
         post=form.save(commit=False)
         post.published_on=timezone.now()
         post.save()
         return redirect('view_post')
      else:
         context['error']='invalid form subission '
         return render(request,'update_post.html',context)
def delete_post(request,id):
   try:
      single_post=Post.objects.get(pk=id)
   except Post.DoesNotExist:
      return HttpResponse('doent exists')
   if request.user != single_post.author:
      return HttpResponse('your not allowed to delete the post')
   single_post.delete()
   return redirect('view_post')
def user_logout(request):
   logout(request)
   return redirect('login')

   
   

       
    