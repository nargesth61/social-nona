from django.shortcuts import render ,redirect 
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import Profile , Post , LikePost
from django.contrib.auth.decorators import login_required



@login_required(login_url='signin')
def index(request):
    user_object =User.objects.get(username =request.user.username)
    user_pro = Profile.objects.get(user = user_object)
     
    posts =Post.objects.all()

    return render(request,'index.html',{'user_pro':user_pro , 'posts':posts})

def signup(request):
    if request.method == 'POST' :
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']        

        if password == password2 :
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Duplicate email')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username has already been used')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()

                user_login=auth.authenticate(username=username, password=password)
                auth.login(request,user_login)
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('index')
        else:
            messages.info(request, 'Password Not Confirm')
            return redirect('signup')

    else :
        return render(request,'signup.html')



@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')





@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def upload(request):
    
    if request.method == 'POST':
        user = request.user.username
        image =request.FILES.get('image_upload')
        caption =request.POST['caption']

        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('index')
    else:
         return redirect('index')    

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else :
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    return render(request,'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')