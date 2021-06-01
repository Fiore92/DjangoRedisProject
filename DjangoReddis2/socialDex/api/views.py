import datetime
import socket
from django.shortcuts import render,redirect
from .forms import SignInForm,PostBachecaFrom,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import PostBacheca,CustomUser
from django.http import JsonResponse
from django.utils.timezone import utc
from django.core.cache import cache


# Create your views here.
def endPoint2(request):
    info=request.GET.get('q')
    posts=PostBacheca.objects.filter()
    count=0
    for post in posts:
        if info in post.text.split(" "):
            count +=1
    return JsonResponse({'the string '+ info +' appeared ' :count},safe=False)

def endPoint1(request):
    response=[]
    posts = PostBacheca.objects.filter()
    for post in posts:
        now=datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff= now - post.created_date
        if timediff.total_seconds()<3600:
            response.append(
                {
                    'author': post.author.username,
                    'datetime':post.created_date,
                    'text':post.text
                }
            )
    return JsonResponse(response,safe=False)

def userArea(request,pk):
    error=0
    user=""
    if cache.get(pk):
        print("DATA FROM CACHE")
        user=cache.get(pk)
    else:
        try:
            print("DATA FROM DB")
            user = CustomUser.objects.filter(id=pk)[0]
            cache.set(pk,user)
        except:
            error = 1

    if error==0:
        return render(request,'api/userArea.html',{'pk':pk,'error':error,'username':user.username})
    else:
        return render(request,'api/userArea.html',{'pk':pk,'error':error,'username':user})

def reservedArea(request):
    response = []
    if request.user.is_superuser:
        users=CustomUser.objects.filter()
        for user in users:
            name = user.username
            count=len(PostBacheca.objects.filter(author=user))
            response.append(
                {
                    'author':name,
                    'count':count
                }
            )

    return render(request,'api/reserved_area.html',{'response':response})

def home(request):
    form=PostBachecaFrom()
    if(request.method=='POST'):
        form = PostBachecaFrom(request.POST)
        text = str(request.POST['text'])
        if "hack" in text.lower():
            messages.error(request,"I cannot save posts with the word hack inside")
        else:
            post = form.save(commit=False)
            post.author= request.user
            post.text=request.POST['text']
            post.save()
            post.writeOnChain()
            messages.success(request,"post successfully saved")
    posts = PostBacheca.objects.filter().order_by('-created_date')
    response = []
    for post in posts:
        response.append(
            {
                'datetime':post.created_date,
                'text':post.text,
                'author':post.author,
                'linkOnChain':post.txId
            }
        )
    return render(request,'api/home.html', {'form': form,'response':response})

def loginAuth(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            me= CustomUser.objects.get(username=username)
            if me.ip!= socket.gethostbyname(socket.gethostname()):
                messages.error(request,"Security Issues The ip has changed")
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "wrong user or password")
    else:
        form = LoginForm()
    return render(request, 'api/login.html', {'form': form})

def LogOut(request):
    logout(request)
    return redirect('/')

def signIn(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        flag=False
        try:
            groups = request.POST['is_superuser']
            flag=True
        except:
            flag=False
        user = CustomUser.objects.filter(username=username).exists()
        if user :
            messages.error(request, 'Already registered user')
        else:
            CustomUser.objects.create_user(username=username, password=password,ip=socket.gethostbyname(socket.gethostname()),is_superuser=flag)
            #messages.success(request, "Registration successful")
            user = authenticate(request, username=username, password=password)
            login(request,user)
            return redirect('home')
    else:
        form = SignInForm()
    return render(request, 'api/signin.html', {'form': form})
