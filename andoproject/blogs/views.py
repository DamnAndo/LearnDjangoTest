from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Blogs,Comment
from . import forms


# Custom 404 Not Working
def error_404(request, exception):
    return render(request,'errors/404.html', status=404)

def index(request):
    blogs = Blogs.objects.all()
    return render(request,'blogs/index.html',{'blogs':blogs})

# def single(request,id):
#     blog = Blogs.objects.get(pk=id)
#     return render(request,'blogs/single.htmlxy',{'blog':blog})


# GIve default error handler django 404
def single(request,id):
    blog = get_object_or_404(Blogs,pk=id)
    form = forms.CommentForm()
    return render(request,'blogs/single.html',{'blog':blog,'form':form})

def comment(request,id):
    blog = get_object_or_404(Blogs,pk=id)

    if request.method == 'POST':
        newDesc = request.POST['desc']
        form = forms.CommentForm(request.POST)

        if form.is_valid():
            blog.comment_set.create(desc=newDesc,user=request.user)
            messages.success(request, 'Berhasil Comment')
            return HttpResponseRedirect(reverse('blogs:index'))

        return render(request,'blogs/single.html',{
            'blog':blog,
            'form':form
        })
        # if len(newDesc) < 10:
        #     return render(request,'blogs/single.htmlxy',{
        #         'blog':blog,
        #         'errors':'Deskripsi kurang dari 10 karakter'
        #     })
        #
        # blog.comment_set.create(desc=newDesc)
        # return HttpResponseRedirect('/blogs/{}'.format(id))

def comment_edit(request,id):
    comment = get_object_or_404(Comment, pk=id)
    form = forms.CommentForm(instance=comment)

    if request.user.id != comment.user.id:
        return HttpResponse("Halaman Tidak Ditemukan")

    if request.method == 'POST':
        form = forms.CommentForm(instance=comment,data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Komentar Edit Success')
            return HttpResponseRedirect(reverse('blogs:index'))


    return render(request,'blogs/comment_edit.html',{
        'comment':comment,
        'form':form
    })



