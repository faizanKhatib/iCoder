from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages 
from django.contrib.auth.models import User
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    # Grabing all post content with the function .all()
    allPosts = Post.objects.all()
    context = {"allPosts": allPosts}
    return render(request, "blog/blogHome.html", context)

def blogPost(request,slug):
    # return HttpResponse(f"This is blogPost!:{slug}")
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None) #instead of using "parent != None"
    post.views = post.views + 1
    post.save()
    replyDict = {}
    for reply in replies:
        if reply.parent.sno  not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {"post": post, "comments": comments, "user": request.user, "replyDict": replyDict}
    return render(request, "blog/blogPost.html", context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request,"Your comment has been sent successfully..")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, parent=parent, user=user, post=post)
            comment.save()
            messages.success(request,"Your reply has been sent successfully..")



      
    return redirect(f"/blog/{post.slug}")
    
