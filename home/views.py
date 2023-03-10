from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# creating html pages

def home(request):
    # return HttpResponse("This is home!")
    # fetching the most viewed blog on the home page
    context = {}
    return render(request, "home/home.html", context)

def contact(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        content = request.POST["content"]
        
        if len(name)<2 or len(email)<3 or len(phone)<9 or len(content)<5:
            messages.error(request, "Please Fill The Correct Information!")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your Form has been Submitted successfully...")
    return render(request, "home/contact.html")

def about(request):
    messages.error(request, "Welcome to About page")
    return render(request, "home/about.html")

def search(request):

    query = request.GET["query"]
    if len(query) > 80:
        allPosts = Post.objects.none()
    else:
        # allPosts = Post.objects.filter(title__icontains = query)
        allPostsTitle = Post.objects.filter(title__icontains = query)
        allPostsContent = Post.objects.filter(content__icontains = query)
        allPostsAuthor = Post.objects.filter(author__icontains = query)
        allPosts = allPostsTitle.union(allPostsContent,allPostsAuthor)

    if allPosts.count() == 0:
        messages.error(request, "404! No search found")
    # allPosts = Post.objects.all()
    
    params = {"allPosts": allPosts, "query":query}

    return render(request, "home/search.html", params)

# authentication APIs

def handleSignup(request):
    # get post parameters
    if request.method == "POST":
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

    # check for error inputs
    # username must be under 10 charactors
    if len(username) > 10 :
        messages.error(request, "Username must be under 10 charactors")
        return redirect("home")

    # username should be alphanumaric
    if not username.isalnum():
        messages.error(request, "Username should contain only letters and numbers")
        return redirect("home")

    # both passwords need to match 
    if password1 != password2:
        messages.error(request, "Passwords does not match")
        return redirect("home")

    # creating the user
        myuser = User.objects.create_user(username,email,password1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, "Your account created successfuly..")
        return redirect("home")

    
    else:
        return HttpResponse("404! Not Found")

def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST["loginusername"]
        loginpassword = request.POST["loginpassword"]

    user = authenticate(username = loginusername, password = loginpassword)
    if user is not None:
        login(request, user)
        messages.success(request, "You successfully Loged in")
        return redirect("home")
    else:
        messages.error(request, "Invalid username or password")
        return redirect("home")
    return HttpResponse("404 - Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request, "You successfully Loged Out")
    return redirect("home")


    
        
   

