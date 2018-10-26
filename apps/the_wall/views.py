from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, MessagePost, Comment
import bcrypt

# Create your views here.

def index(request):
    if 'logged_in' in request.session:
        if request.session['logged_in'] == True:
            user = User.objects.get(id=request.session['id'])
            if user.email != request.session['email']:
                request.session.clear()
                request.session.modified = True
                return render(request, 'the_wall/index.html')
            else:
                context = {
                    "user": User.objects.get(id=user.id),
                    "message_post": MessagePost.objects.order_by("-created_at"),
                    "comment_post": Comment.objects.order_by("-created_at"),
                }
                return render(request, 'the_wall/index.html', context)
        else:
            return render(request, 'the_wall/index.html')
    else:
        return render(request, 'the_wall/index.html')

def user_create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create()
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user.save()
        request.session['new_registration'] = True
        request.session['id'] = user.id
        request.session['email'] = user.email
        return redirect("/users/login/success/")

def validate_login(request):
    users = User.objects.all()
    try:
        user = users.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['logged_in'] = True
            request.session['id'] = user.id
            request.session['email'] = user.email
            if 'new_registration' in request.session:
                del request.session['new_registration']
                request.session.modified = True
            return redirect('/users/login/success/')
        else:
            messages.error(request, "Invalid password!")
            return redirect('/')
    except User.DoesNotExist:
        messages.error(request, "Email does not exist! Please register to continue")
        return redirect('/')

def success(request):
    if 'new_registration' in request.session:
        request.session['logged_in'] = True
        user = User.objects.get(id=request.session['id'])        
        return redirect("/wall/")
    elif 'logged_in' in request.session:
        if request.session['logged_in'] == True:
            user = User.objects.get(id=request.session['id'])
            if user.email != request.session['email']:
                request.session.clear()
                return redirect("/wall/")
            else:
                return redirect("/wall/")
        else:
            return redirect("/wall/")
    else:
        return redirect("/wall/")

def logout(request):
    request.session.clear()
    request.session.modified = True
    return redirect("/")

def create_message(request):
    user = User.objects.get(id=request.session['id'])
    user.save()
    message_post = MessagePost.objects.create(message=request.POST['message'], message_poster=user)
    message_post.save()
    return redirect("/wall/")

def create_comment(request, number):
    user = User.objects.get(id=request.session['id'])
    user.save()
    message = MessagePost.objects.get(id=number)
    message.save()
    comment_post = Comment.objects.create(comment=request.POST['comment'], comment_poster=user, commented_on=message)
    comment_post.save()
    return redirect("/wall/")

def destroy_comment(request, number):
    comment = Comment.objects.get(id=number)
    comment.delete()
    return redirect("/wall/")


